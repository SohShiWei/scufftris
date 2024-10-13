from settings import Colors, Position
import pygame

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
        self.positions = []

    def move(self, rows, columns):
        # Move the block by a specified number of rows and columns.
        self.row_offset += rows  # Update the vertical position
        self.column_offset += columns  # Update the horizontal position
        self.update_positions()

    def get_cell_positions(self):
        # Get the current positions of the block's cells based on its rotation state and offsets.
        tiles = self.cells[self.rotation_state]  # Get the tiles for the current rotation state
        moved_tiles = []  # Initialize a list to store the new positions

        for position in tiles:
            # Create a new Position object with updated offsets for each tile.
            new_position = Position(position.row + self.row_offset, position.column + self.column_offset)
            moved_tiles.append(new_position)  # Add the new position to the list

        return moved_tiles  # Return the list of updated positions

    def rotate(self):
        # Rotate the block clockwise
        self.rotation_state = (self.rotation_state + 1) % len(self.cells)
        self.update_positions()
        
    def rotate_counterclockwise(self):
        # Rotate block counter-clockwise
        self.rotation_state = (self.rotation_state - 1) % len(self.cells)
        self.update_positions()
        
    def update_positions(self):
        # Update the positions based on the current rotation state
        self.positions = [
            Position(p.row + self.row_offset, p.column + self.column_offset)
            for p in self.cells[self.rotation_state]
        ]
        
    def undo_rotation(self):
        # Revert the block's rotation to the previous state.
        self.rotation_state -= 1  # Decrement the rotation state
        if self.rotation_state == -1:
            # Set to the last defined state if rotation state goes below 0.
            self.rotation_state = len(self.cells) - 1
            
    def clone(self):
        # Clone a block to be used for shadows
        cloned_block = Block(self.id)
        cloned_block.cells = self.cells
        cloned_block.row_offset = self.row_offset
        cloned_block.column_offset = self.column_offset
        cloned_block.rotation_state = self.rotation_state
        return cloned_block

    def draw(self, screen, offset_x, offset_y, shadow=False):
        # Draw the block on the specified screen at a given offset.
        tiles = self.get_cell_positions()  # Get the current positions of the block's cells
        
        if shadow:
            # Create a transparent surface for the shadow block
            shadow_surface = pygame.Surface((self.cell_size * len(tiles), self.cell_size * len(tiles)), pygame.SRCALPHA)
            shadow_color = (self.colors[self.id][0], self.colors[self.id][1], self.colors[self.id][2], 75)  # Semi-transparent shadow

            for tile in tiles:
                # Create the rectangle for each tile
                tile_rect = pygame.Rect(
                    (tile.column - self.column_offset) * self.cell_size,  # Calculate x position relative to block
                    (tile.row - self.row_offset) * self.cell_size,  # Calculate y position relative to block
                    self.cell_size - 1,
                    self.cell_size - 1
                )
                # Draw the shadow rectangle on the shadow surface
                pygame.draw.rect(shadow_surface, shadow_color, tile_rect)

            # Blit the shadow surface onto the main screen with the given offset
            screen.blit(shadow_surface, (offset_x + self.column_offset * self.cell_size, offset_y + self.row_offset * self.cell_size))

        else:
            
            for tile in tiles:
                # Create a rectangle for each tile position to be drawn on the screen.
                tile_rect = pygame.Rect(
                    offset_x + tile.column * self.cell_size,  # Calculate x position
                    offset_y + tile.row * self.cell_size,  # Calculate y position
                    self.cell_size - 1,  # Width of the cell rectangle
                    self.cell_size - 1   # Height of the cell rectangle
                )
                pygame.draw.rect(screen, self.colors[self.id], tile_rect)  # Draw the rectangle on the screen