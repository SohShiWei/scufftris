import pygame, os
# 2D Vector class used for positioning (0,0) as the middle of the grid
vec = pygame.math.Vector2

class Colors:
    # Original Colors
    DARK_GREY = (26, 31, 40)
    GREEN = (2, 156, 84)
    ORANGE = (245, 91, 27)
    BLUE = (163, 230, 238)
    PURPLE = (217, 199, 249)
    YELLOW = (249, 251, 83)
    PINK = (255, 164, 208)
    GREY = (225, 225, 225)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    # Additional Colors
    CREAM = (254, 250, 224)
    LIGHT_CREAM = (254, 252, 235)
    GREY = (225, 225, 225)
    BLACK = (0, 0, 0)
    LIGHT_RED = (255, 102, 102)
    TLIGHT_BLUE = (59, 85, 162,128)

    @classmethod
    def get_cell_colors(cls):
        # Accessed by block.py and grid.py to return board and tetromino colors
        return [cls.DARK_GREY, cls.GREEN, cls.ORANGE, cls.YELLOW, cls.PURPLE, cls.YELLOW, cls.PINK, cls.LIGHT_RED]

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
target_lines = 40
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
    'left': pygame.K_j,
    'right': pygame.K_l,
    'down': pygame.K_k,
    'rotate': pygame.K_f,
    'rotate_ccw': pygame.K_d,
    'hard_drop': pygame.K_i,
    'hold': pygame.K_e
}

# Controls that can be changed
controls = default_controls.copy()