from grid import Grid 
from blocks import *  # Importing different tetromino (block) shapes
import random  
from setting import *
from colors import Colors

class Game:
    def __init__(self):
        # Initializes the game with an empty grid, block queue, and starting block
        self.grid = Grid()
        # List of all block shapes (tetrominoes)
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        self.current_block = self.get_random_block() # The block currently falling
        self.next_block = [self.get_random_block() for b in range(4)] # The block to appear after the current one
        self.game_over = False  # A flag to track if the game is over
        self.paused = False # Track if the game state is pauses
        self.score = 0  # Keeps track of the player's score
        
        # Load sounds
        sounds = ["Sounds/Piano1.ogg", "Sounds/Piano2.ogg", "Sounds/Piano3.ogg", "Sounds/Piano4.ogg", "Sounds/Piano5.ogg", 
                  "Sounds/Piano6.ogg", "Sounds/Piano7.ogg", "Sounds/Piano8.ogg", "Sounds/Piano9.ogg", "Sounds/Piano10.ogg"]
        self.rotate_sound = pygame.mixer.Sound("Sounds/button-28.wav")
        self.clear_sound = pygame.mixer.Sound(random.choice(sounds))
        pygame.mixer.music.load("Sounds/神っぽいな.flac") # Load and play background music on loop
        pygame.mixer.music.play(-1) # -1 means the music loops indefinitely
        pygame.mixer.music.set_volume(0.3) # Set the volume of the background music
        
    def play(self, screen, next_rect, score_rect):
        # Main game loop (runs continuously)
        clock = pygame.time.Clock()
        clock.tick(90)
        speed = 300 # Initial speed of the game (block movement down)
        paused = False  # Flag to track if the game is paused
        
        # Custom user event for updating the game every few milliseconds
        GAME_UPDATE = pygame.USEREVENT
        pygame.time.set_timer(GAME_UPDATE, speed) # Set the event to trigger every `speed` milliseconds
        # Initialize timers for controlling movement (left, right, down)
        move_left_timer, move_right_timer, move_down_timer = 0, 0, 0
        move_delay = 100 # Delay (in milliseconds) to prevent continuous movement when holding keys
        
        while True:
            current_time = pygame.time.get_ticks()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.paused = not self.paused
                    if not self.paused and not self.game_over:
                        if event.key in [pygame.K_UP, pygame.K_SPACE]:
                            self.rotate()
                if event.type == GAME_UPDATE and not self.paused and not self.game_over:
                    self.move_down()

            if not self.paused and not self.game_over:
                keys = pygame.key.get_pressed()
                if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and current_time - move_left_timer > move_delay:
                    self.move_left()
                    move_left_timer = current_time
                if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and current_time - move_right_timer > move_delay:
                    self.move_right()
                    move_right_timer = current_time
                if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and current_time - move_down_timer > move_delay:
                    self.move_down()
                    self.update_score(0, 1)
                    move_down_timer = current_time

            # Draw game state
            screen.fill(Colors.dark_blue)
            self.grid.draw(screen)
            self.draw(screen, next_rect, score_rect)
            
            # Blit game_screen onto the main screen
            main_screen = pygame.display.get_surface()
            main_screen.blit(screen, (0, 0))

            pygame.display.update()

    def update_score(self, lines_cleared, move_down_points):
        # Updates the score based on the number of lines cleared and points for moving blocks down
        if lines_cleared == 1:
            self.score += 100
        elif lines_cleared == 2:
            self.score += 300
        elif lines_cleared == 3:
            self.score += 600
        elif lines_cleared == 4:
            self.score += 1000      
        self.score += move_down_points  # Add points for moving blocks down
        
    def get_random_block(self):
        # Selects a random block from the block list, ensuring no duplicates
        if len(self.blocks) == 0:  # Reset the list if all blocks have been used
            self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        block = random.choice(self.blocks)  # Choose a random block
        self.blocks.remove(block)  # Remove it from the list to avoid immediate repetition
        return block

    def move_left(self):
        # Moves the current block left and checks if it remains inside and fits
        self.current_block.move(0, -1)
        if not self.block_inside() or not self.block_fits():
            self.current_block.move(0, 1)  # Undo the move if invalid

    def move_right(self):
        # Moves the current block right and checks if it remains inside and fits
        self.current_block.move(0, 1)
        if not self.block_inside() or not self.block_fits():
            self.current_block.move(0, -1)  # Undo the move if invalid

    def move_down(self):
        # Moves the current block down and locks it if it can't move further
        self.current_block.move(1, 0)
        if not self.block_inside() or not self.block_fits():
            self.current_block.move(-1, 0)  # Undo the move if invalid
            self.lock_block()  # Lock the block in place if it can't move down further

    def lock_block(self):
        # Locks the current block in the grid and prepares the next block
        tiles = self.current_block.get_cell_positions()  # Get the block's current positions
        for position in tiles:
            if 0 <= position.row < self.grid.num_rows and 0 <= position.column < self.grid.num_cols:
                self.grid.grid[position.row][position.column] = self.current_block.id
        self.current_block = self.next_block.pop(0)  # Move to the next block
        self.next_block.append(self.get_random_block()) # Prepare a new block
        rows_cleared = self.grid.clear_full_rows()  # Check if any rows were completed

        # Move to the next block and add a new random block to the next_blocks list
        self.current_block = self.next_block.pop(0)
        self.next_block.append(self.get_random_block())

        if rows_cleared > 0:
            self.clear_sound.play()  # Play sound if rows were cleared
            self.update_score(rows_cleared, 0)  # Update score based on cleared rows
        if self.block_fits() == False:
            self.game_over = True  # End the game if a new block can't fit

    def reset(self):
        # Resets the game to the initial state (empty grid, new blocks, reset score)
        self.grid.reset()  # Reset the grid
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]  # Reset block list
        self.current_block = self.get_random_block()  # Start with a new block
        self.next_block = self.get_random_block()  # Prepare the next block
        self.score = 0  # Reset score

    def block_fits(self):
        # Checks if the current block fits in its current position
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if not self.grid.is_inside(tile.row, tile.column) or not self.grid.is_empty(tile.row, tile.column): 
                return False
        return True

    def rotate(self):
        # Rotates the current block and checks if it fits
        self.current_block.rotate()
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.undo_rotation()  # Undo the rotation if it doesn't fit
        else:
            self.rotate_sound.play()  # Play the rotate sound if the rotation was successful

    def block_inside(self):
        # Checks if the current block is completely within the grid boundaries
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if not (0 <= tile.row < self.grid.num_rows and 0 <= tile.column < self.grid.num_cols):
                return False
        return True
    
    def draw(self, screen, next_rect, score_rect):
        # Draw the grid and the current block
        self.grid.draw(screen)
        self.current_block.draw(screen, game_screen_rect.x, game_screen_rect.y)

        # Draw rectangles for score and next block areas
        pygame.draw.rect(screen, Colors.light_blue, next_rect, 0, 10)
        pygame.draw.rect(screen, Colors.light_blue, score_rect, 0, 10)

        # Display the "Score" title and actual score
        score_title_surface = pygame.font.Font("assets/AvenirNextLTPro-HeavyCondItalic.otf", 40).render("Score", True, Colors.white)
        screen.blit(score_title_surface, (score_rect.x + 20, score_rect.y + 10))

        score_value_surface = pygame.font.Font("assets/AvenirNextLTPro-HeavyCondItalic.otf", 40).render(str(self.score), True, Colors.white)
        screen.blit(score_value_surface, score_value_surface.get_rect(centerx=score_rect.centerx, centery=score_rect.centery + 20))

        # Draw the next 4 blocks in the preview area, stacked vertically
        for i, block in enumerate(self.next_block):
            # Calculate the vertical position for each block in the preview area
            preview_x = next_rect.x - 40 # Center each block in the preview area
            preview_y = next_rect.y + i * (20 * 4) + 20  # Stack each block vertically
            block.draw(screen, preview_x, preview_y)

