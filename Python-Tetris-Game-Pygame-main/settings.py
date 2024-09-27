import pygame as pg
import os

# 2D Vector class used for positioning (0,0) as the middle of the grid
vec = pg.math.Vector2

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

# Fonts
# find current directory
current_dir = os.path.dirname(__file__)
#load font path
FONT_PATH = os.path.join(current_dir,'Fonts', 'GAMEPLAY-1987.ttf')

# Display
FPS = 60
ANIMATION_TIME_INTERVAL = 400
DISPLAY_COLOUR = (BLACK)
DISPLAY_BACKGROUND_COLOUR = (LIGHT_CREAM)
TILE_BORDER_COLOUR = (CREAM)
TILE_SIZE = 50
DISPLAY_SIZE = DISPLAY_W, DISPLAY_H = 10,20
DISPLAY_RES = DISPLAY_W * TILE_SIZE, DISPLAY_H * TILE_SIZE

# Scale factor for Window (extended from original grid size)
DISPLAY_SCALE_W, DISPLAY_SCALE_H = 3.0, 1.0
WINDOW_RES = WINDOW_W, WINDOW_H = DISPLAY_RES[0] * DISPLAY_SCALE_W, DISPLAY_RES[1] * DISPLAY_SCALE_H

#game settings
speed = 300  # Initial speed of the game (block movement down)
move_left_timer = 0
move_right_timer = 0
move_down_timer = 0
move_delay = 100  # Delay (in milliseconds) to prevent continuous movement when holding keys
