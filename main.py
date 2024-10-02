import pygame, sys  # Importing pygame for game rendering and sys for system exit
from game import Game  # Import the Game class which contains the Tetris game logic
from settings import *  # Import a custom colors class that stores various color values
from menu import Menus

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


game = Game()  # Initialize the game (an instance of the Game class)
menus = Menus() # Initialize the menu (an instance of the menu class)

# Game loop control
current_page = "menu" # Start in the Main menu

while True:
    if current_page == "menu":
        current_page = menus.main_menu(screen, DISPLAY_WIDTH, DISPLAY_HEIGHT)
    elif current_page == "play":
        game.play(screen)  # Start the game
    elif current_page == "settings":
        menus.show_settings_menu(screen, controls, DISPLAY_WIDTH, DISPLAY_HEIGHT) 
        current_page = "menu"
    elif current_page == "quit":
        pygame.quit()
        sys.exit()
             
    pygame.display.update()
    
# def pause_menu():
#     # Function to display the pause menu
#     screen.fill(colors.BLUE)  # Fill the screen with dark blue background
    
#     # Render pause menu options (Resume, Quit, Speed adjustment)
#     resume_surface = menu_font.render("RESUME", True, colors.BLACK)
#     back_to_menu_surface = menu_font.render("BACK TO MENU", True, colors.BLACK)
#     quit_surface = menu_font.render("QUIT", True, colors.BLACK)
#     #drop down speed
#     speed_surface = menu_font.render(f"SPEED: {speed}", True, colors.BLACK)
#     decrease_speed_surface = menu_font.render("SLOWER", True, colors.BLACK)
#     increase_speed_surface = menu_font.render("FASTER", True, colors.BLACK)
#     #block moving speed
#     move_surface = menu_font.render(f"MOVEMENT: {move_delay}", True, colors.BLACK)
#     decrease_move_surface = menu_font.render("SLOWER", True, colors.BLACK)
#     increase_move_surface = menu_font.render("FASTER", True, colors.BLACK)
    
#     # Position the menu options
#     resume_rect = resume_surface.get_rect(center=(250, 200))
#     back_to_menu_rect = back_to_menu_surface.get_rect(center=(250, 500))
#     quit_rect = quit_surface.get_rect(center=(250, 250))
#     #drop down speed
#     speed_rect = speed_surface.get_rect(center=(250, 300))
#     decrease_speed_rect = decrease_speed_surface.get_rect(center=(150, 350))
#     increase_speed_rect = increase_speed_surface.get_rect(center=(350, 350))
#     #block moving speed
#     move_rect = speed_surface.get_rect(center=(225, 400))
#     decrease_move_rect = decrease_speed_surface.get_rect(center=(150, 450))
#     increase_move_rect = increase_speed_surface.get_rect(center=(350, 450))
    
#     # Display the menu options on the screen
#     screen.blit(resume_surface, resume_rect)
#     screen.blit(back_to_menu_surface, back_to_menu_rect)
#     screen.blit(quit_surface, quit_rect)
#     screen.blit(speed_surface, speed_rect)
#     screen.blit(decrease_speed_surface, decrease_speed_rect)
#     screen.blit(increase_speed_surface, increase_speed_rect)
#     screen.blit(move_surface, move_rect )
#     screen.blit(decrease_move_surface, decrease_move_rect)
#     screen.blit(increase_move_surface, increase_move_rect)
    
#     pygame.display.update()  # Update the display to show the pause menu
    
#     # Return the rects for menu items to detect clicks
#     return resume_rect, quit_rect, speed_rect, increase_speed_rect, decrease_speed_rect, move_rect, increase_move_rect, decrease_move_rect, back_to_menu_rect