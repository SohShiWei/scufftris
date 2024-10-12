from grid import Grid 
from blocks import *  # Importing different tetromino (block) shapes
from settings import *
import random, sys
from menu import Menus


class Game:
     
    def __init__(self):
        # Initializes the game with an empty grid, block queue, and starting block
        self.grid = Grid()
        # List of all block shapes (tetrominoes)
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        self.current_block = self.get_random_block()  # The block currently falling
        self.next_block = self.get_random_block()  # The block to appear after the current one
        self.game_over = False  # A flag to track if the game is over
        self.score = 0  # Keeps track of the player's score
        self.paused = False # Flag to track if the game is paused
        # hold tetromino function
        self.hold_block = None
        self.hold_used = False
        # lock delay function
        self.lock_delay = 0  # Time in milliseconds before the block locks
        self.lock_timer = 500  # Timer to track how long the block has been at the bottom
        
        # Load sounds for rotating blocks and clearing rows
        self.rotate_sound = pygame.mixer.Sound("Sounds/rotate.wav")
        self.clear_sound = pygame.mixer.Sound("Sounds/clear.ogg")
        self.hard_drop_sound = pygame.mixer.Sound("Sounds/harddrop.mp3")
    
        # Load and play background music on loop
        pygame.mixer.music.load("Sounds/OriginalTetristheme.mp3")
        pygame.mixer.music.play(-1)  # -1 means the music loops indefinitely
        pygame.mixer.music.set_volume(0.3) # Set the volume of the background music
        
    def play(self, screen):
        global speed, click_delay, move_delay, move_left_timer, move_right_timer, move_down_timer, last_click_time, controls
        # Main game loop (runs continuously)
        clock = pygame.time.Clock()
      
        # Custom user event for updating the game every few milliseconds
        GAME_UPDATE = pygame.USEREVENT
        pygame.time.set_timer(GAME_UPDATE, speed) # Set the event to trigger every `speed` milliseconds
        
         # Fonts and text surfaces for rendering on the screen
        title_font = pygame.font.Font(FONT_PATH, 30)  # Font for titles (e.g., "Score", "Next")

        # Render static text surfaces for "Score", "Next", and "GAME OVER"
        score_surface = title_font.render("SCORE", True, Colors.BLACK)
        next_surface = title_font.render("NEXT", True, Colors.BLACK)
        
        # Rectangles for positioning the score and next block sections
        score_rect = pygame.Rect(320, 55, 170, 60)  # Score box on the right of the screen
        next_rect = pygame.Rect(320, 150, 170, 180)  # Next block preview box
        
        while True:
            
            current_time = pygame.time.get_ticks()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == GAME_UPDATE and not self.paused and not self.game_over:
                    self.move_down()
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.paused = not self.paused
                    if not self.paused and not self.game_over:
                        if event.key == controls['hard_drop']:
                            self.hard_drop()
                        if event.key == controls['rotate']:
                            self.rotate()
                        if event.key == controls['rotate_ccw']:
                            self.rotate_counterclockwise()   
                        if event.key == controls['hold']:
                            self.hold()
                    if self.game_over == True:  # Reset the game if it's over
                            self.game_over = False
                            self.reset()

            if not self.paused and not self.game_over:
                keys = pygame.key.get_pressed()
                if (keys[controls['left']]) and current_time - move_left_timer > move_delay:
                    # print(current_time , move_left_timer , move_delay)
                    self.move_left()
                    move_left_timer = current_time
                    # print(self.score)
                if (keys[controls['right']]) and current_time - move_right_timer > move_delay:
                    # print(current_time , move_right_timer , move_delay)
                    self.move_right()
                    move_right_timer = current_time
                    # print(self.score)
                if (keys[controls['down']]) and current_time - move_down_timer > move_delay:
                    if self.block_fits(self.current_block, row_offset=1):
                        # print(current_time , move_down_timer , move_delay)
                        self.move_down()
                        self.update_score(0, 2)
                        move_down_timer = pygame.time.get_ticks()
                    else:
                        if self.lock_timer == 0:
                            self.lock_timer = pygame.time.get_ticks()# Start the lock timer if not already started

                        if pygame.time.get_ticks() - self.lock_timer > self.lock_delay:
                            self.lock_block()  # Lock the block in place if the delay has passed**
                            move_down_timer = current_time

            if self.game_over:  # If the game is over, display the "GAME OVER" text
                self.game_over = Menus().gameover(screen, DISPLAY_WIDTH, DISPLAY_HEIGHT,self.score)
                self.reset()
                self.game_over = False
                return

            if self.paused:
                # Display pause menu and handle interations
                menu_action = Menus().pause_menu(screen, speed, move_delay, DISPLAY_WIDTH, DISPLAY_HEIGHT)
                
                # Handle the returned action from the pause menu
                if menu_action == "resume":
                    pygame.event.clear()
                    self.paused = False  # Unpause the game
                elif menu_action == "restart":
                    self.reset()  # Reset the game state
                    pygame.event.clear()
                    self.paused = False  # Resume after restarting
                elif menu_action == "controls":
                    Menus().controls_menu(screen, controls, DISPLAY_WIDTH, DISPLAY_HEIGHT)
                    pygame.event.clear()
                    self.reset()  # Reset game state when returning to the main menu
                    self.paused = False  # Ensure the game is unpaused when coming back   
                elif menu_action == "main_menu":
                    pygame.event.clear()
                    Menus().main_menu(screen, DISPLAY_WIDTH, DISPLAY_HEIGHT)
                    self.reset()  # Reset game state when returning to the main menu
                    self.paused = False  # Ensure the game is unpaused when coming back
                    return
                
            # Draw game state
            score_value_surface = title_font.render(str(self.score), True, Colors.WHITE)  # Render current score
            screen.fill(Colors.DARK_BLUE)
            self.draw(screen)
            screen.blit(score_surface, (365, 20, 50, 50))  # Draw the "Score" title
            screen.blit(next_surface, (375, 120, 50, 50))  # Draw the "Next" title for the next block preview
             # Draw rectangles for score and next block areas
            pygame.draw.rect(screen, Colors.LIGHT_BLUE, score_rect, 0, 10)
            # Display the score inside the score rectangle
            screen.blit(score_value_surface, score_value_surface.get_rect(centerx=score_rect.centerx, centery=score_rect.centery))
            pygame.draw.rect(screen, Colors.LIGHT_BLUE, next_rect, 0, 10)  # Draw the rectangle for the next block preview
            self.draw(screen)  # Draw the current state of the game (grid and blocks)
            # Blit game_screen onto the main screen
            main_screen = pygame.display.get_surface()
            main_screen.blit(screen, (0, 0))

            pygame.display.update()
            clock.tick(FPS)
    
    def update_score(self, lines_cleared, move_down_points):
        # Updates the score based on the number of lines cleared and points for moving blocks down
        if lines_cleared == 1:
            self.score += 100
        elif lines_cleared == 2:
            self.score += 300
        elif lines_cleared == 3:
            self.score += 600
        elif lines_cleared == 4:
            self.score += 1200
        self.score += move_down_points  # Add points for moving blocks down

    def get_random_block(self):
        # Selects a random block from the block list, ensuring no duplicates
        if len(self.blocks) == 0:  # Reset the list if all blocks have been used
            self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        block = random.choice(self.blocks)  # Choose a random block
        self.blocks.remove(block)  # Remove it from the list to avoid immediate repetition
        
        # Set the block's initial position at the top center
        block.row_offset = 0  # Start at the top row
        block.column_offset = 3  # Start in the center of the grid (adjust this based on your grid width)
        
        # Check if the block can fit in the grid
        if not self.block_fits(block):
            self.game_over = True  # End the game if the new block can't fit
        else:
            self.lock_timer = 0 # Reset lock timer on new block
            
        return block

    def move_left(self):
        # Moves the current block left and checks if it remains inside and fits
        self.current_block.move(0, -1)
        if not self.block_fits(self.current_block):
        #if self.block_inside(self.current_block) == False or self.block_fits(self.current_block) == False:
            self.current_block.move(0, 1)  # Undo the move if invalid

    def move_right(self):
        # Moves the current block right and checks if it remains inside and fits
        self.current_block.move(0, 1)
        if not self.block_fits(self.current_block):
        #if self.block_inside(self.current_block) == False or self.block_fits(self.current_block) == False:
            self.current_block.move(0, -1)  # Undo the move if invalid
            
    def move_down(self):
        # Check if the block can move down by one row
        if self.block_fits(self.current_block, row_offset=1):
            # Move the block down by one row
            self.current_block.row_offset += 1
            self.lock_timer = 0  # Reset lock timer if the block successfully moves down
        else:
            # Start the lock timer if the block is colliding
            if self.lock_timer == 0:
                self.lock_timer = pygame.time.get_ticks()  # Start the lock timer if not already started

            # If the lock delay time has passed, lock the block in place
            if pygame.time.get_ticks() - self.lock_timer > self.lock_delay:
                self.lock_block()  # Lock the block in place
                self.lock_timer = 0  # Reset the lock timer for the next block           

    def hard_drop(self):
        # Move the block down until it no longer fits
        while self.block_inside(self.current_block) and self.block_fits(self.current_block, row_offset=1):
            self.current_block.move(1, 0)  # Move down by 1 row
        
        # Once the block can no longer move down, lock it in place
        self.lock_block()
        
        # Play the hard drop sound and update the score
        self.hard_drop_sound.play()
        self.update_score(0, 10)  # Add score for the hard drop
            
    def lock_block(self):
        # Lock the current block into the grid
        tiles = self.current_block.get_cell_positions()
        for position in tiles:
            if self.grid.is_inside(position.row, position.column):
                self.grid.grid[position.row][position.column] = self.current_block.id
            # if 0 <= popositionssition.row < len(self.grid.grid) and 0 <= position.column < len(self.grid.grid[0]):
            #     self.grid.grid[position.row][position.column] = self.current_block.id
                    
        # Prepare the next block and reset necessary variables
        self.current_block = self.next_block
        self.next_block = self.get_random_block()
        self.lock_timer = 0
        self.hold_used = False
        
        # Clear full rows and update score
        rows_cleared = self.grid.clear_full_rows()
        if rows_cleared > 0:
            self.clear_sound.play()
            self.update_score(rows_cleared, 0)

        # Check if the new block fits; if not, the game is over
        if not self.block_fits(self.current_block):
            self.game_over = True

    def reset(self):
        # Resets the game to the initial state (empty grid, new blocks, reset score)
        self.grid.reset()  # Reset the grid
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]  # Reset block list
        self.current_block = self.get_random_block()  # Start with a new block
        self.next_block = self.get_random_block()  # Prepare the next block
        self.score = 0  # Reset score

    def rotate(self):
        # Rotates the current block
        self.current_block.rotate()
        # Check if the rotated block fits
        if not self.block_fits(self.current_block) or not self.block_inside(self.current_block):
            # Attempt to use wall kicks to adjust the block's position
            if not self.try_wall_kick(self.current_block):
                # If wall kicks fail, revert the rotation
                self.current_block.rotate_counterclockwise()
            else:
                self.rotate_sound.play()
                self.lock_timer = 0  # Reset lock timer on successful wall kick
        else:
            self.rotate_sound.play()
            self.lock_timer = 0  # Reset lock timer on successful wall kick
            
    def rotate_counterclockwise(self):
        # Rotates the current block
        self.current_block.rotate_counterclockwise()
        # Check if the rotated block fits
        if not self.block_fits(self.current_block) or not self.block_inside(self.current_block):
            # Attempt to use wall kicks to adjust the block's position
            if not self.try_wall_kick(self.current_block):
                # If wall kicks fail, revert the rotation
                self.current_block.rotate()
            else:
                self.rotate_sound.play()
                self.lock_timer = 0  # Reset lock timer on successful wall kick
        else:
            self.rotate_sound.play()       
            self.lock_timer = 0  # Reset lock timer on successful wall kick
                
    def try_wall_kick(self, block):
        # Define possible offsets to try for wall kicks (right, left, up)
        wall_kick_offsets = [(0, 1), (0, -1), (-1, 0), (0, 2), (0, -2)]
        
        for row_offset, col_offset in wall_kick_offsets:
            # Apply the offset to the block's position
            block.move(row_offset, col_offset)
            # Check if the adjusted block now fits
            if self.block_fits(block) and self.block_inside(block):
                return True  # Found a valid position
            
            # If it doesn't fit, move it back to its original position
            block.move(-row_offset, -col_offset)
            
        return False  # No valid position found with wall kicks
    
    def block_fits(self, block, row_offset=0, column_offset=0):
        for position in block.get_cell_positions():
            row = position.row + row_offset
            column = position.column + column_offset
            
            # Ensure the block is inside the grid bounds
            if row < 0 or row >= len(self.grid.grid) or column < 0 or column >= len(self.grid.grid[0]):
                print(f"Block out of bounds at row {row}, column {column}")
                return False

            # Ensure the block does not overlap with filled cells in the grid
            if not self.grid.is_empty(row, column):
                print(f"Block collided with filled cell at row {row}, column {column}")
                return False
            
        return True

    def block_inside(self, block):
        # Checks if the current block is completely within the grid boundaries
        for position in block.get_cell_positions():
            if position.row < 0 or position.row >= len(self.grid.grid) or position.column < 0 or position.column >= len(self.grid.grid[0]):
                return False
        return True
    
    def get_shadow_block(self):
        # Create a shadow block to preview where the block will land
        shadow_block = self.current_block.clone()
        while self.block_inside(shadow_block) and self.block_fits(shadow_block):
            shadow_block.move(1, 0) # Shadow block is placed at the bottom
        shadow_block.move(-1, 0) # Place shadow block 1 row up if it does not fit
        return shadow_block
    
    def hold(self):
        global move_left_timer, move_right_timer, move_down_timer
        if self.hold_used:
            return # Allow holding only once per drop
        
        if self.hold_block is None:
            # If no block is held, move current block to hold and generate next block
            self.hold_block = self.current_block
            self.current_block = self.next_block
            self.next_block = self.get_random_block()
        else:
            # Swap the current block
            self.hold_block, self.current_block = self.current_block, self.hold_block
            
        # Reset rotation state of block to default (0)
        self.hold_block.rotation_state = 0 
        self.hold_block.update_positions() # Update positions to reflect the default rotation state

            
        # Reset position of the block    
        self.hold_block.row_offset = 0  # Reset the position of the block when it comes out of hold
        self.hold_block.column_offset = 3  # Center it horizontally
            
        # reset position of the movement timer
        move_left_timer = pygame.time.get_ticks()
        move_right_timer = pygame.time.get_ticks()
        move_down_timer = pygame.time.get_ticks()
        
        self.hold_used = True #Preven hold until next block is locked

    def draw(self, screen):
         # Draws the grid and the current and next blocks on the screen
        self.grid.draw(screen)  # Draw the grid
        
        self.get_shadow_block().draw(screen, 11, 11, shadow=True)  # Draw a shadow block on the grid
        self.current_block.draw(screen, 11, 11)  # Draw the current block on the grid

        # Draw the next block in a preview box (with slight adjustment for size)
        if self.next_block.id == 3:  # For OBlock, adjust the position slightly
            self.next_block.draw(screen, 255, 210)
        elif self.next_block.id == 4:  # For TBlock, adjust the position slightly
            self.next_block.draw(screen, 280, 220)
        else:
            self.next_block.draw(screen, 270, 200)  # For all other blocks
            
        # Display Hold rectangle
        title_font = pygame.font.Font(FONT_PATH, 30)
        hold_surface = title_font.render("HOLD", True, Colors.BLACK)
        hold_rect = pygame.Rect(320, 360, 170, 180)  # Define a rectangle for the "hold" box
        screen.blit(hold_surface, (375, 330, 50, 50))  # Draw the "Hold" label
        pygame.draw.rect(screen, Colors.LIGHT_BLUE, hold_rect, 0, 10)  # Draw the rectangle for the hold block preview   
        # Draw the hold blocks
        if self.hold_block:
            if self.hold_block.id == 3:  # Adjust the position for the I Block
                self.hold_block.draw(screen, 255, 410)
            elif self.hold_block.id == 4:  # Adjust the position for the O Block
                self.hold_block.draw(screen, 280, 410)
            else:
                self.hold_block.draw(screen, 270, 410)
