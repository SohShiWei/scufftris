from game import Game  # Import the Game class which contains the Tetris game logic
from colors import Colors  # Import a custom Colors class that stores various color values
from button import Button
from setting import *

pygame.init()  # Initialize the pygame module

game = Game()  # Initialize the game (an instance of the Game class)

# Fonts and text surfaces for rendering on the screen
def get_font(size):
    return pygame.font.Font("assets/AvenirNextLTPro-HeavyCondItalic.otf", size)

title_font = get_font(40)  # Ftitles (e.g., "Score", "Next")
menu_font = get_font(30)  # Font for the pause menu

# Render static text surfaces for "Score", "Next", and "GAME OVER"
score_surface = title_font.render("Score", True, Colors.white)
next_surface = title_font.render("Next", True, Colors.white)
game_over_surface = title_font.render("GAME OVER", True, Colors.white)

def main_menu():
    pygame.display.set_caption("Python Tetris Menu")
    
    while True:
        # Draw the sidebars and game area on the screen
        pygame.draw.rect(screen, Colors.light_blue, left_sidebar_rect)  # Left sidebar
        pygame.draw.rect(screen, Colors.dark_blue, game_screen_rect)  # Center game screen
        pygame.draw.rect(screen, Colors.light_blue, right_sidebar_rect)  # Right sidebar

        screen.blit(background_img, (0, 0))

        menu_mouse_pos = pygame.mouse.get_pos()
        
        menu_text = get_font(100).render("PYTRIS", True, "black")
        menu_rect = menu_text.get_rect(center=(screen_width * 0.5, screen_height * 0.35))
        
        # Menu buttons
        play_button = Button(image=None, pos=(screen_width * 0.5, screen_height * 0.5), text_input="PLAY", font=get_font(50), base_color="black", hovering_color="red")
        settings_button = Button(image=None, pos=(screen_width * 0.5, screen_height * 0.6), text_input="SETTINGS", font=get_font(50), base_color="black", hovering_color="red")
        quit_button = Button(image=None, pos=(screen_width * 0.5, screen_height * 0.7), text_input="QUIT", font=get_font(50), base_color="black", hovering_color="red")
        
        screen.blit(menu_text, menu_rect)
        
        for button in [play_button, settings_button, quit_button]:
            button.changeColor(menu_mouse_pos)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type ==  pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.checkForInput(menu_mouse_pos):
                    game.play(game_screen, next_rect, score_rect)
                if settings_button.checkForInput(menu_mouse_pos):
                    settings()
                if quit_button.checkForInput(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()
        
        pygame.display.update()
        
def settings():
    print("Setting pressed")

main_menu()