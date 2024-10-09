import pygame, os
# 2D Vector class used for positioning (0,0) as the middle of the grid
vec = pygame.math.Vector2


class colors:
# Colours
    CREAM = (254, 250, 224)
    LIGHT_CREAM = (254, 252, 235)
    GREEN = (2, 156, 84)
    ORANGE = (245, 91, 27)
    BLUE = (163, 230, 238)
    PURPLE = (217, 199, 249)
    YELLOW = (249, 251, 83)
    PINK = (255, 164, 208)
    GREY = (225, 225, 225)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    @classmethod
    def get_cell_colors(cls):
        return [cls.CREAM, cls.LIGHT_CREAM, cls.GREEN, cls.ORANGE, cls.BLUE, cls.PURPLE, cls.YELLOW, cls.PINK,cls.GREY,cls.BLACK,cls.WHITE]

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
DISPLAY_COLOUR = (colors.BLACK)
DISPLAY_BACKGROUND_COLOUR = (colors.LIGHT_CREAM)
TILE_BORDER_COLOUR = (colors.CREAM)
DISPLAY_WIDTH = 500
DISPLAY_HEIGHT = 620


#game settings
speed = 300  # Initial speed of the game (block movement down)
move_left_timer = 0
move_right_timer = 0
move_down_timer = 0
move_delay = 100  # Delay (in milliseconds) to prevent continuous movement when holding keys

# Debounce variables for mouse clicks in the pause menu
last_click_time = 0
click_delay = 300  # Delay between mouse clicks (in milliseconds)

# Default controls setting (DO NOT CHANGE)
default_controls = {
    'left': pygame.K_a,
    'right': pygame.K_d,
    'down': pygame.K_s,
    'rotate': pygame.K_w,
    'hard_drop': pygame.K_SPACE,
}

# Controls that can be changed
controls = default_controls.copy()