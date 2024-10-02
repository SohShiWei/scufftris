import pygame, sys  # Importing pygame for game rendering and sys for system exit
from game import Game  # Import the Game class which contains the Tetris game logic
from settings import *  # Import a custom colors class that stores various color values
import settings
pygame.init()  # Initialize the pygame module

# Fonts and text surfaces for rendering on the screen
title_font = pygame.font.Font(FONT_PATH, 30)  # Font for titles (e.g., "Score", "Next")
menu_font = pygame.font.Font(FONT_PATH, 30)  # Font for the pause menu

controls = {
    'left': pygame.K_LEFT,
    'right': pygame.K_RIGHT,
    'down': pygame.K_DOWN,
    'rotate': pygame.K_UP
}

# Render static text surfaces for "Score", "Next", and "GAME OVER"
score_surface = title_font.render("SCORE", True, colors.BLACK)
next_surface = title_font.render("NEXT", True, colors.BLACK)
game_over_surface = title_font.render("GAME OVER", True, colors.BLACK)

# Rectangles for positioning the score and next block sections
score_rect = pygame.Rect(320, 55, 170, 60)  # Score box on the right of the screen
next_rect = pygame.Rect(320, 215, 170, 180)  # Next block preview box

# Set up the game window with dimensions (500x620)
screen = pygame.display.set_mode((500, 620))
pygame.display.set_caption("Python Tetris")  # Window title

clock = pygame.time.Clock()  # A clock object to manage the game's frame rate

game = Game()  # Initialize the game (an instance of the Game class)

paused = False  # Flag to track if the game is paused
speed = 300  # Initial speed of the game (block movement down)

# Custom user event for updating the game every few milliseconds
GAME_UPDATE = pygame.USEREVENT
pygame.time.set_timer(GAME_UPDATE, speed)  # Set the event to trigger every `speed` milliseconds

# Initialize timers for controlling movement (left, right, down)
move_left_timer = 0
move_right_timer = 0
move_down_timer = 0
move_delay = 100  # Delay (in milliseconds) to prevent continuous movement when holding keys

# Debounce variables for mouse clicks in the pause menu
last_click_time = 0
click_delay = 300  # Delay between mouse clicks (in milliseconds)

def pause_menu():
    # Function to display the pause menu
    screen.fill(colors.BLUE)  # Fill the screen with dark blue background
    
    # Render pause menu options (Resume, Quit, Speed adjustment)
    resume_surface = menu_font.render("RESUME", True, colors.BLACK)
    back_to_menu_surface = menu_font.render("BACK TO MENU", True, colors.BLACK)
    quit_surface = menu_font.render("QUIT", True, colors.BLACK)
    #drop down speed
    speed_surface = menu_font.render(f"SPEED: {speed}", True, colors.BLACK)
    decrease_speed_surface = menu_font.render("SLOWER", True, colors.BLACK)
    increase_speed_surface = menu_font.render("FASTER", True, colors.BLACK)
    #block moving speed
    move_surface = menu_font.render(f"MOVEMENT: {move_delay}", True, colors.BLACK)
    decrease_move_surface = menu_font.render("SLOWER", True, colors.BLACK)
    increase_move_surface = menu_font.render("FASTER", True, colors.BLACK)
    
    # Position the menu options
    resume_rect = resume_surface.get_rect(center=(250, 200))
    back_to_menu_rect = back_to_menu_surface.get_rect(center=(250, 500))
    quit_rect = quit_surface.get_rect(center=(250, 250))
    #drop down speed
    speed_rect = speed_surface.get_rect(center=(250, 300))
    decrease_speed_rect = decrease_speed_surface.get_rect(center=(150, 350))
    increase_speed_rect = increase_speed_surface.get_rect(center=(350, 350))
    #block moving speed
    move_rect = speed_surface.get_rect(center=(225, 400))
    decrease_move_rect = decrease_speed_surface.get_rect(center=(150, 450))
    increase_move_rect = increase_speed_surface.get_rect(center=(350, 450))
    
    # Display the menu options on the screen
    screen.blit(resume_surface, resume_rect)
    screen.blit(back_to_menu_surface, back_to_menu_rect)
    screen.blit(quit_surface, quit_rect)
    screen.blit(speed_surface, speed_rect)
    screen.blit(decrease_speed_surface, decrease_speed_rect)
    screen.blit(increase_speed_surface, increase_speed_rect)
    screen.blit(move_surface, move_rect )
    screen.blit(decrease_move_surface, decrease_move_rect)
    screen.blit(increase_move_surface, increase_move_rect)
    
    pygame.display.update()  # Update the display to show the pause menu
    
    # Return the rects for menu items to detect clicks
    return resume_rect, quit_rect, speed_rect, increase_speed_rect, decrease_speed_rect, move_rect, increase_move_rect, decrease_move_rect, back_to_menu_rect

def main_menu():
    while True:
        screen.fill(colors.BLUE)  # Fill the background color
        title_font = pygame.font.Font(FONT_PATH, 74)  # Set up a font for the menu title
        menu_font = pygame.font.Font(FONT_PATH, 50)  # Set up a font for the menu options
        
        title_surface = title_font.render("TETRIS", True, colors.BLACK)
        start_surface = menu_font.render("1. START GAME", True, colors.BLACK)
        settings_surface = menu_font.render("2. SETTINGS",True,colors.BLACK)
        quit_surface = menu_font.render("3. QUIT", True, colors.BLACK)
        
        screen.blit(title_surface, (100, 200))  # Draw the title
        screen.blit(start_surface, (50, 300))  # Draw the "Start Game" option
        screen.blit(settings_surface, (50, 350))
        screen.blit(quit_surface, (50, 400))  # Draw the "Quit" option

        pygame.display.update()  # Update the display

        # Handle events for the main menu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If user clicks close
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:  # Start game on pressing '1'
                    return  # Exit the menu loop and start the game
                if event.key == pygame.K_2:
                    settings.handle_settings(screen,controls)
                    return
                if event.key == pygame.K_2:  # Quit game on pressing '2'
                    pygame.quit()
                    sys.exit()

main_menu()
# Main game loop (runs continuously)
while True:
    current_time = pygame.time.get_ticks()  # Get the current time in milliseconds (used for timers)

    # Event handling loop (listens for user input and system events)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If the user clicks the close button, exit the game
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:  # If a key is pressed
            if event.key == pygame.K_p:  # If 'P' is pressed, toggle pause
                paused = not paused
            if not paused:  # If the game isn't paused
                if game.game_over:  # Reset the game if it's over
                    game.game_over = False
                    game.reset()
                if event.key == controls['rotate']:  # Rotate the block with UP or SPACE
                    game.rotate()
        if event.type == GAME_UPDATE and not game.game_over and not paused:
            game.move_down()  # Automatically move the block down on the GAME_UPDATE event

    # Key handling for movement (left, right, down)
    if not paused:
        keys = pygame.key.get_pressed()  # Get the state of all keyboard keys
        if not game.game_over:  # Only allow movement if the game is not over
            # Move block left (left arrow key or 'A') with debounce
            if (keys[controls['left']]) and current_time - move_left_timer > move_delay:
                game.move_left()
                move_left_timer = current_time
            # Move block right (right arrow key or 'D') with debounce
            if (keys[controls['right']]) and current_time - move_right_timer > move_delay:
                game.move_right()
                move_right_timer = current_time
            # Move block down (down arrow key or 'S') with debounce
            if (keys[controls['down']]) and current_time - move_down_timer > move_delay:
                game.move_down()
                game.update_score(0, 1)  # Update score when moving down
                move_down_timer = current_time

        # Drawing the game state
        score_value_surface = title_font.render(str(game.score), True, colors.WHITE)  # Render current score
        
        screen.fill(colors.CREAM)  # Clear the screen with the background color
        screen.blit(score_surface, (365, 20, 50, 50))  # Draw the "Score" title
        screen.blit(next_surface, (375, 180, 50, 50))  # Draw the "Next" title for the next block preview

        if game.game_over:  # If the game is over, display the "GAME OVER" text
            screen.blit(game_over_surface, (320, 450, 50, 50))

        # Draw rectangles for score and next block areas
        pygame.draw.rect(screen, colors.BLACK, score_rect, 0, 10)
        # Display the score inside the score rectangle
        screen.blit(score_value_surface, score_value_surface.get_rect(centerx=score_rect.centerx, centery=score_rect.centery))
        pygame.draw.rect(screen, colors.BLACK, next_rect, 0, 10)  # Draw the rectangle for the next block preview
        game.draw(screen)  # Draw the current state of the game (grid and blocks)

        pygame.display.update()  # Update the display

    else:  # If the game is paused, display the pause menu
        resume_rect, quit_rect, speed_rect, increase_speed_rect, decrease_speed_rect, move_rect, increase_move_rect, decrease_move_rect, back_to_menu_rect = pause_menu()
        
        # Handle mouse input for the pause menu
        mouse_pos = pygame.mouse.get_pos()  # Get the current mouse position
        mouse_click = pygame.mouse.get_pressed()  # Get the state of mouse buttons
        
        # Handle mouse clicks with a debounce delay
        if mouse_click[0] and current_time - last_click_time > click_delay:  # Left-click
            last_click_time = current_time
            if resume_rect.collidepoint(mouse_pos):  # Resume button clicked
                paused = False
            elif quit_rect.collidepoint(mouse_pos):  # Quit button clicked
                pygame.quit()
                sys.exit()
            elif back_to_menu_rect.collidepoint(mouse_pos):  # Quit button clicked
                main_menu()
                paused = False
                game.reset()
            elif increase_speed_rect.collidepoint(mouse_pos):  # Increase speed clicked
                if speed > 50:  # Limit the speed increase
                    speed -= 50
                    pygame.time.set_timer(GAME_UPDATE, speed)  # Update the game speed
            elif decrease_speed_rect.collidepoint(mouse_pos):  # Decrease speed clicked
                if speed < 1000:  # Limit the speed decrease
                    speed += 50
                    pygame.time.set_timer(GAME_UPDATE, speed)  # Update the game speed
            elif increase_move_rect.collidepoint(mouse_pos):  # Increase move clicked
                if move_delay > 0:  # Limit the move increase
                    move_delay -= 50
                    pygame.time.set_timer(GAME_UPDATE, speed)  # Update the move speed
            elif decrease_move_rect.collidepoint(mouse_pos):  # Decrease speed clicked
                if move_delay < 1000:  # Limit the move decrease
                    move_delay += 50
                    pygame.time.set_timer(GAME_UPDATE, speed)  # Update the move speed

    clock.tick(80)  # Limit the game to 80 frames per second (FPS)
