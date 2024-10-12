import pygame, os
# 2D Vector class used for positioning (0,0) as the middle of the grid
vec = pygame.math.Vector2

class Colors:
    # Original Colors
    DARK_GREY = (26, 31, 40)
    GREEN = (0, 255, 107)
    RED = (251, 50, 40)
    ORANGE = (255, 152, 0)
    YELLOW = (255, 245, 2)
    PURPLE = (159, 46, 255)
    CYAN = (0, 255, 233)
    BLUE = (0, 83, 255)
    WHITE = (255, 255, 255)
    DARK_BLUE = (44, 44, 127)
    LIGHT_BLUE = (59, 85, 162)
    # Additional Colors
    CREAM = (254, 250, 224)
    LIGHT_CREAM = (254, 252, 235)
    PINK = (255, 164, 208)
    GREY = (225, 225, 225)
    BLACK = (0, 0, 0)

    @classmethod
    def get_cell_colors(cls):
        # Accessed by block.py and grid.py to return board and tetromino colors
        return [cls.DARK_GREY, cls.BLUE, cls.ORANGE, cls.CYAN, cls.YELLOW, cls.GREEN, cls.PURPLE, cls.RED]

class Position:
    def __init__(self, row, column):
        # Initialize a Position object with row and column attributes.
        # This class is used to represent the position of a block in the grid.
        
        self.row = row  # The row index of the position (vertical axis)
        self.column = column  # The column index of the position (horizontal axis)
        
class Button():
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)

# Fonts
# find current directory
current_dir = os.path.dirname(__file__)
#load font path
FONT_PATH = os.path.join(current_dir,'Fonts', 'GAMEPLAY-1987.ttf')
#load background image
# BACKGROUND_IMG = os.path.join(current_dir,'Assets', 'bg.png')

# Display
FPS = 90
ANIMATION_TIME_INTERVAL = 400
DISPLAY_COLOUR = (Colors.BLACK)
DISPLAY_BACKGROUND_COLOUR = (Colors.LIGHT_CREAM)
TILE_BORDER_COLOUR = (Colors.CREAM)
DISPLAY_WIDTH = 500
DISPLAY_HEIGHT = 620


#game settings
speed = 600  # Initial speed of the game (block movement down)
move_delay = 100  # Delay (in milliseconds) to prevent continuous movement when holding keys
game_over = False
target_lines = 4
time_limit = 120000
speed_increment_threshold = 500
# Initialize timers for controlling movement (left, right, down)
move_left_timer = 0
move_right_timer = 0
move_down_timer = 0

# Debounce variables for mouse clicks in the pause menu
last_click_time = 0
click_delay = 300  # Delay between mouse clicks (in milliseconds)


# Default controls setting (DO NOT CHANGE)
default_controls = {
    'left': pygame.K_a,
    'right': pygame.K_d,
    'down': pygame.K_s,
    'rotate': pygame.K_w,
    'rotate_ccw': pygame.K_q,
    'hard_drop': pygame.K_SPACE,
    'hold': pygame.K_e
}

# Controls that can be changed
controls = default_controls.copy()