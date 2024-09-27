from colors import Colors
import pygame
from position import Position
from settings import *

class menu:
    def pause_menu():
        # Fonts and text surfaces for rendering on the screen
        menu_font = pygame.font.Font(None, 30)  # Font for the pause menu
        screen = pygame.display.set_mode((500, 620))
        # Function to display the pause menu
        screen.fill(Colors.dark_blue)  # Fill the screen with dark blue background
        
        # Render pause menu options (Resume, Quit, Speed adjustment)
        resume_surface = menu_font.render("Resume", True, Colors.white)
        quit_surface = menu_font.render("Quit", True, Colors.white)
        #drop down speed
        speed_surface = menu_font.render(f"Speed: {speed}", True, Colors.white)
        decrease_speed_surface = menu_font.render("slower", True, Colors.white)
        increase_speed_surface = menu_font.render("faster", True, Colors.white)
        #block moving speed
        move_surface = menu_font.render(f"Movement: {move_delay}", True, Colors.white)
        decrease_move_surface = menu_font.render("slower", True, Colors.white)
        increase_move_surface = menu_font.render("faster", True, Colors.white)
        
        # Position the menu options
        resume_rect = resume_surface.get_rect(center=(250, 200))
        quit_rect = quit_surface.get_rect(center=(250, 250))
        #drop down speed
        speed_rect = speed_surface.get_rect(center=(250, 300))
        decrease_speed_rect = decrease_speed_surface.get_rect(center=(300, 350))
        increase_speed_rect = increase_speed_surface.get_rect(center=(200, 350))
        #block moving speed
        move_rect = speed_surface.get_rect(center=(225, 400))
        decrease_move_rect = decrease_speed_surface.get_rect(center=(300, 450))
        increase_move_rect = increase_speed_surface.get_rect(center=(200, 450))
        
        # Display the menu options on the screen
        screen.blit(resume_surface, resume_rect)
        screen.blit(quit_surface, quit_rect)
        screen.blit(speed_surface, speed_rect)
        screen.blit(decrease_speed_surface, decrease_speed_rect)
        screen.blit(increase_speed_surface, increase_speed_rect)
        screen.blit(move_surface, move_rect )
        screen.blit(decrease_move_surface, decrease_move_rect)
        screen.blit(increase_move_surface, increase_move_rect)
        
        pygame.display.update()  # Update the display to show the pause menu
        
        # Return the rects for menu items to detect clicks
        return resume_rect, quit_rect, speed_rect, increase_speed_rect, decrease_speed_rect, move_rect, increase_move_rect, decrease_move_rect