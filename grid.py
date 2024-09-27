from setting import *
from colors import Colors

class Grid:
    def __init__(self):
        # Initialize the grid with a set number of rows, columns, and cell size.
        self.num_rows = 20
        self.num_cols = 10
        self.cell_size = 30
        # Create a 2D list representing the grid, initialized with 0 (empty cells).
        self.grid = [[0 for j in range(self.num_cols)] for i in range(self.num_rows)]
        # Get the colors for the cells from an external Colors class.
        self.colors = Colors.get_cell_colors()

    def print_grid(self):
        # Prints the current state of the grid to the console for debugging.
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                print(self.grid[row][column], end=" ")
            print()  # New line after each row

    def is_inside(self, row, column):
        # Checks if the given row and column are within the boundaries of the grid.
        return 0 <= row < self.num_rows and 0 <= column < self.num_cols

    def is_empty(self, row, column):
        # Returns True if the cell at the given row and column is empty (value 0).
        return self.grid[row][column] == 0

    def is_row_full(self, row):
        # Checks if a row is full (i.e., contains no empty cells).
        for column in range(self.num_cols):
            if self.grid[row][column] == 0:
                return False
        return True

    def clear_row(self, row):
        # Clears a specific row by setting all its values to 0.
        for column in range(self.num_cols):
            self.grid[row][column] = 0

    def move_row_down(self, row, num_rows):
        # Moves a row down by 'num_rows' number of rows.
        # This is useful when clearing a row and shifting the rows above it downward.
        for column in range(self.num_cols):
            self.grid[row + num_rows][column] = self.grid[row][column]
            self.grid[row][column] = 0

    def clear_full_rows(self):
        # Clears all full rows in the grid and shifts rows above downwards.
        # Returns the number of cleared rows.
        completed = 0
        for row in range(self.num_rows - 1, 0, -1):  # Start checking from the bottom row
            if self.is_row_full(row):
                self.clear_row(row)
                completed += 1
            elif completed > 0:
                self.move_row_down(row, completed)
        return completed  # Return the number of rows that were cleared

    def reset(self):
        # Resets the grid by setting all cells to 0 (empty).
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                self.grid[row][column] = 0
                
    def draw(self, screen):
        # Use the top-left corner of game_screen_rect as the starting point for drawing the grid
        x_offset = game_screen_rect.x  # Align to the left of the game area
        y_offset = game_screen_rect.y  # Align to the top of the game area

        # Iterate over each cell and draw it at its new, aligned position
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                cell_value = self.grid[row][column]
                # Define the rectangle for the current cell
                cell_rect = pygame.Rect(
                    x_offset + column * self.cell_size,  # Shift horizontally by x_offset
                    y_offset + row * self.cell_size,     # Shift vertically by y_offset
                    self.cell_size - 1, 
                    self.cell_size - 1
                )
                # Draw the rectangle on the screen with the appropriate color
                pygame.draw.rect(screen, self.colors[cell_value], cell_rect)
