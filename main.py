import pygame, sys  # Importing pygame for game rendering and sys for system exit
from game import Game  # Import the Game class which contains the Tetris game logic
from settings import *  # Import a custom colors class that stores various color values
from menu import Menus
from clear40 import clear40

pygame.init()  # Initialize the pygame module

# Set up the game window with dimensions (500x620)
screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption("Python Tetris")  # Window title


game = Game()  # Initialize the game (an instance of the Game class)
menus = Menus() # Initialize the menu (an instance of the menu class)
clear40 = clear40(4)
# Game loop control
current_page = "menu" # Start in the Main menu

while True:
    pygame.event.clear()
    
    if current_page == "menu":
        pygame.event.clear()
        current_page = menus.main_menu(screen, DISPLAY_WIDTH, DISPLAY_HEIGHT)
    elif current_page == "play":
        game.play(screen)  # Start the game
        current_page = "menu" 
    elif current_page == "clear40":  
        clear40.play(screen) # Start the game
        current_page = "menu"
    elif current_page == "settings":
        pygame.event.clear()
        menus.show_settings_menu(screen, controls, DISPLAY_WIDTH, DISPLAY_HEIGHT) 
        current_page = "menu"
    elif current_page == "quit":
        pygame.quit()
        sys.exit()
    
             
    pygame.display.update()