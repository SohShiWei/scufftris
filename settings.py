import pygame
import os

# 2D Vector class used for positioning (0,0) as the middle of the grid
vec = pygame.math.Vector2

# Fonts and text surfaces for rendering on the screen
def get_font(size):
    return pygame.font.Font("Fonts/GAMEPLAY-1987.ttf", size)

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

# Display
FPS = 60
ANIMATION_TIME_INTERVAL = 400
DISPLAY_COLOUR = (colors.BLACK)
DISPLAY_BACKGROUND_COLOUR = (colors.LIGHT_CREAM)
TILE_BORDER_COLOUR = (colors.CREAM)
TILE_SIZE = 50
DISPLAY_H = 620
DISPLAY_W = 720

# game settings
paused = False # Flag to track if the game is paused
speed = 300  # Initial speed of the game (block movement down)
move_left_timer = 0
move_right_timer = 0
move_down_timer = 0
move_delay = 100  # Delay (in milliseconds) to prevent continuous movement when holding keys
clock = pygame.time.Clock() # A clock object to manage the game's frame rate