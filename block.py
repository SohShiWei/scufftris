from colors import Colors
import pygame
from position import Position

class Block:
    def __init__(self, id):
        # Initialize a Block object representing a Tetris block.
        self.id = id  # The unique identifier for the block (used for color and type)
        self.cells = {}  # Dictionary to hold cell positions for different rotation states
        self.cell_size = 30  # Size of each cell in pixels
        self.row_offset = 0  # Vertical offset for positioning the block in the grid
        self.column_offset = 0  # Horizontal offset for positioning the block in the grid
        self.rotation_state = 0  # Current rotation state of the block
        self.colors = Colors.get_cell_colors()  # Get the colors for the block from the Colors class

    def move(self, rows, columns):
        # Move the block by a specified number of rows and columns.
        self.row_offset += rows  # Update the vertical position
        self.column_offset += columns  # Update the horizontal position

    def get_cell_positions(self):
        # Get the current positions of the block's cells based on its rotation state and offsets.
        tiles = self.cells[self.rotation_state]  # Get the tiles for the current rotation state
        moved_tiles = []  # Initialize a list to store the new positions

        for position in tiles:
            # Create a new Position object with updated offsets for each tile.
            position = Position(position.row + self.row_offset, position.column + self.column_offset)
            moved_tiles.append(position)  # Add the new position to the list

        return moved_tiles  # Return the list of updated positions

    def rotate(self):
        # Rotate the block to the next state.
        self.rotation_state += 1  # Increment the rotation state
        if self.rotation_state == len(self.cells):
            # Reset to 0 if the rotation state exceeds the number of defined states.
            self.rotation_state = 0

    def undo_rotation(self):
        # Revert the block's rotation to the previous state.
        self.rotation_state -= 1  # Decrement the rotation state
        if self.rotation_state == -1:
            # Set to the last defined state if rotation state goes below 0.
            self.rotation_state = len(self.cells) - 1

    def draw(self, screen, offset_x, offset_y):
        # Draw the block on the specified screen at a given offset.
        tiles = self.get_cell_positions()  # Get the current positions of the block's cells
        for tile in tiles:
            # Create a rectangle for each tile position to be drawn on the screen.
            tile_rect = pygame.Rect(
                offset_x + tile.column * self.cell_size,  # Calculate x position
                offset_y + tile.row * self.cell_size,  # Calculate y position
                self.cell_size - 1,  # Width of the cell rectangle
                self.cell_size - 1   # Height of the cell rectangle
            )
            pygame.draw.rect(screen, self.colors[self.id], tile_rect)  # Draw the rectangle on the screen