from grid import Grid 
from blocks import *  # Importing different tetromino (block) shapes
import random  
import pygame  

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
        
        # Load sounds for rotating blocks and clearing rows
        self.rotate_sound = pygame.mixer.Sound("Sounds/rotate.wav")
        self.clear_sound = pygame.mixer.Sound("Sounds/clear.ogg")

        # Load and play background music on loop
        pygame.mixer.music.load("Sounds/music.ogg")
        pygame.mixer.music.play(-1)  # -1 means the music loops indefinitely

    def update_score(self, lines_cleared, move_down_points):
        # Updates the score based on the number of lines cleared and points for moving blocks down
        if lines_cleared == 1:
            self.score += 100
        elif lines_cleared == 2:
            self.score += 300
        elif lines_cleared == 3:
            self.score += 500
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
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(0, 1)  # Undo the move if invalid

    def move_right(self):
        # Moves the current block right and checks if it remains inside and fits
        self.current_block.move(0, 1)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(0, -1)  # Undo the move if invalid

    def move_down(self):
        # Moves the current block down and locks it if it can't move further
        self.current_block.move(1, 0)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(-1, 0)  # Undo the move if invalid
            self.lock_block()  # Lock the block in place if it can't move down further

    def lock_block(self):
        # Locks the current block in the grid and prepares the next block
        tiles = self.current_block.get_cell_positions()  # Get the block's current positions
        for position in tiles:
            # Set the block's id in the grid to lock its position
            self.grid.grid[position.row][position.column] = self.current_block.id
        self.current_block = self.next_block  # Move to the next block
        self.next_block = self.get_random_block()  # Prepare a new block
        rows_cleared = self.grid.clear_full_rows()  # Check if any rows were completed
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
            if self.grid.is_empty(tile.row, tile.column) == False:  # Check if tile is in an empty cell
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
            if self.grid.is_inside(tile.row, tile.column) == False:  # Check if the tile is inside the grid
                return False
        return True

    def draw(self, screen):
        # Draws the grid and the current and next blocks on the screen
        self.grid.draw(screen)  # Draw the grid
        self.current_block.draw(screen, 11, 11)  # Draw the current block on the grid

        # Draw the next block in a preview box (with slight adjustment for size)
        if self.next_block.id == 3:  # For OBlock, adjust the position slightly
            self.next_block.draw(screen, 255, 290)
        elif self.next_block.id == 4:  # For TBlock, adjust the position slightly
            self.next_block.draw(screen, 255, 280)
        else:
            self.next_block.draw(screen, 270, 270)  # For all other blocks