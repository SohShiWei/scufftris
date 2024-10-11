import pygame, sys  # Importing pygame for game rendering and sys for system exit
from game import Game  # Import the Game class which contains the Tetris game logic
from settings import *  # Import a custom colors class that stores various color values
from menu import Menus
from sprint_game import *

pygame.init()  # Initialize the pygame module

# Set up the game window with dimensions (500x620)
screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption("Python Tetris")  # Window title


game = Game()  # Initialize the game (an instance of the Game class)
menus = Menus() # Initialize the menu (an instance of the menu class)

# Game loop control
current_page = "menu" # Start in the Main menu

while True:
    if current_page == "menu":
        current_page = menus.main_menu(screen, DISPLAY_WIDTH, DISPLAY_HEIGHT)
    elif current_page == "play":
        game.play(screen)  # Start the game
    elif current_page == "sprint":  
        sprint_game = SprintGame(target_lines=5)  # Target number of lines 
        sprint_game.play(screen)
        current_page = "menu"
    elif current_page == "settings":
        menus.show_settings_menu(screen, controls, DISPLAY_WIDTH, DISPLAY_HEIGHT) 
        current_page = "menu"
    # elif current_page == "gameover":
        # menus.gameover(screen, DISPLAY_WIDTH, DISPLAY_HEIGHT,Game.score)
    elif current_page == "quit":
        pygame.quit()
        sys.exit()
    
             
    pygame.display.update()