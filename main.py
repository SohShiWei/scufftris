import pygame, sys  # Importing pygame for game rendering and sys for system exit
from game import Game  # Import the Game class which contains the Tetris game logic
from settings import *  # Import a custom colors class that stores various color values
from menu import Menus
from sprint_game import SprintGame
 
pygame.init()  # Initialize the pygame module

# Fonts and text surfaces for rendering on the screen
title_font = pygame.font.Font(FONT_PATH, 30)  # Font for titles (e.g., "Score", "Next")
menu_font = pygame.font.Font(FONT_PATH, 30)  # Font for the pause menu

# Render static text surfaces for "Score", "Next", and "GAME OVER"
score_surface = title_font.render("SCORE", True, colors.BLACK)
next_surface = title_font.render("NEXT", True, colors.BLACK)
game_over_surface = title_font.render("GAME OVER", True, colors.BLACK)

# Rectangles for positioning the score and next block sections
score_rect = pygame.Rect(320, 55, 170, 60)  # Score box on the right of the screen
next_rect = pygame.Rect(320, 215, 170, 180)  # Next block preview box

# Set up the game window with dimensions (500x620)
screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption("Python Tetris")  # Window title


game = Game()  # Initialize the game
menus = Menus() # Initialize the menu 

# Game loop control
current_page = "menu" # Start in the Main menu

while True:
    if current_page == "menu":
        current_page = menus.main_menu(screen, DISPLAY_WIDTH, DISPLAY_HEIGHT)
    elif current_page == "play": 
        game.play(screen)  # Start the game
    elif current_page == "sprint":
        sprint_game = SprintGame() # Initialize the PowerUpGame class
        sprint_game.play(screen)  
        current_page = "menu"
    elif current_page == "settings":
        menus.show_settings_menu(screen, controls, DISPLAY_WIDTH, DISPLAY_HEIGHT) 
        current_page = "menu"
    elif current_page == "quit":
        pygame.quit()
        sys.exit()
             
    pygame.display.update()