import pygame as pg
import os
import pygame
# 2D Vector class used for positioning (0,0) as the middle of the grid
vec = pg.math.Vector2


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

# Display
FPS = 60
ANIMATION_TIME_INTERVAL = 400
DISPLAY_COLOUR = (colors.BLACK)
DISPLAY_BACKGROUND_COLOUR = (colors.LIGHT_CREAM)
TILE_BORDER_COLOUR = (colors.CREAM)
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

def show_settings_menu(sc, controls):
    sc.fill((50, 50, 50))  # Background color for settings menu
    settings_font = pygame.font.Font(None, 50)

    options = ['Left', 'Right', 'Down', 'Rotate']
    instructions = 'Remap using ARROW keys'
    esc = 'ESC to go back to MENU'
    
    # Render and display the instructions
    instructions_text = settings_font.render(instructions, True, pygame.Color('white'))
    sc.blit(instructions_text, (100, 50))  # Position above the control options
    
    esc_text = settings_font.render(esc, True, pygame.Color('white'))
    sc.blit(esc_text, (100, 90))  

    for i, option in enumerate(options):  # Render and display the control options
        text = settings_font.render(f'{option}: {pygame.key.name(controls[option.lower()])}', True, pygame.Color('white'))
        sc.blit(text, (100, 200 + i * 60))
    
    pygame.display.flip()

def remap_control(sc, key_name, controls):
    prompt_text = f'Press new key for {key_name}'
    prompt_font = pygame.font.Font(None, 50)
    prompt_surface = prompt_font.render(prompt_text, True, pygame.Color('white'))

    sc.fill((50, 50, 50))
    sc.blit(prompt_surface, (100, 100))
    pygame.display.flip()

    waiting_for_key = True
    while waiting_for_key:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                controls[key_name.lower()] = event.key
                waiting_for_key = False
                show_settings_menu(sc, controls)  # Refresh menu to show updated controls
                return
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

def handle_settings(sc, controls):
    show_settings_menu(sc, controls)
    
    settings_running = True
    while settings_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Press 'ESC' to exit settings
                    settings_running = False
                    return
                elif event.key == pygame.K_LEFT:
                    remap_control(sc, 'left', controls)
                elif event.key == pygame.K_RIGHT:
                    remap_control(sc, 'right', controls)
                elif event.key == pygame.K_DOWN:
                    remap_control(sc, 'down', controls)
                elif event.key == pygame.K_UP:
                    remap_control(sc, 'rotate', controls)
