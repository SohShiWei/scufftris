import pygame
import sys
from game import Game
from settings import *
from menu import *
from blocks import *

class clear40(Game):
    
    def __init__(self, target_lines):
        super().__init__()  # Call the initializer of the Game class
        self.target_lines = target_lines  # Number of lines to clear
        self.elapsed_time = 0  # Timer starts at 0
        self.game_over = False  # Initialize game over status
        self.win = False  # Initialize win status
        self.lines_cleared = 0  # Track the number of lines cleared

    def update_score(self, lines_cleared, move_down_points):
        # Updates the score based on the number of lines cleared and points for moving blocks down
        if lines_cleared == 1:
            self.line_clear_channel.play(self.clear_sound)
            self.score += 100
        elif lines_cleared == 2:
            self.line_clear_channel.play(self.clear_sound)
            self.score += 300
        elif lines_cleared == 3:
            self.line_clear_channel.play(self.clear_sound)
            self.score += 600
        elif lines_cleared == 4:
            self.line_clear_channel.play(self.tetris_sound)
            self.score += 1200
        self.lines_cleared += lines_cleared  # Update lines cleared count
        self.score += move_down_points  # Add points for moving blocks down
    
    def reset(self):
        # Resets the game to the initial state (empty grid, new blocks, reset score)
        self.grid.reset()  # Reset the grid
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]  # Reset block list
        self.current_block = self.get_random_block()  # Start with a new block
        self.next_block = self.get_random_block()  # Prepare the next block
        self.win = False
        self.score = 0  # Reset score
        self.elapsed_time = 0
        self.starting = pygame.time.get_ticks()
        self.lines_cleared = 0

    def display_win(self, screen):  # Display the win screen 
        font = pygame.font.Font(None, 74)
        win_text = font.render("You Win!", True, Colors.GREEN)
        screen.blit(win_text, (DISPLAY_WIDTH // 2 - 105, DISPLAY_HEIGHT // 2 - 50))

        font = pygame.font.Font(None, 36)
        restart_text = font.render("Press R to Retry | Q to Main Menu", True, Colors.WHITE)
        screen.blit(restart_text, (DISPLAY_WIDTH // 2 - 195, DISPLAY_HEIGHT // 2 + 20))
        
    def play(self, screen):     # Main game loop (runs continuously)
        global speed, click_delay, move_delay, move_left_timer, move_right_timer, move_down_timer, last_click_time, controls
        clock = pygame.time.Clock() 

        GAME_UPDATE = pygame.USEREVENT
        pygame.time.set_timer(GAME_UPDATE, speed)

        # Score and Preview surface and rect and font
        title_font = pygame.font.Font(FONT_PATH, 30)  # Font for titles (e.g., "Score", "Next")

        # Render static text surfaces for "Score", "Next", and "GAME OVER"
        score_surface = title_font.render("SCORE", True, Colors.ORANGE)
        next_surface = title_font.render("NEXT", True, Colors.ORANGE)
        
        # Rectangles for positioning the score and next block sections
        score_rect = pygame.Rect(320, 55, 170, 60)  # Score box on the right of the screen
        next_rect = pygame.Rect(320, 150, 170, 170)  # Next block preview box

        self.starting = pygame.time.get_ticks()   # Start timer only when the game loop begins
        self.pause_time = 0  # Track how long the game is paused

        while True:
            current_time = pygame.time.get_ticks()

            # Calculate elapsed time
            if not self.paused and not self.game_over and not self.win:
                self.elapsed_time = (current_time - self.starting - self.pause_time) // 1000  # Subtract pause duration

            if self.lines_cleared >= self.target_lines:  
                self.win = True  # Set win condition
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        if not self.paused:
                            # Pausing the game
                            self.paused = True
                            self.pause_start_time = pygame.time.get_ticks()
                        else:
                            # Unpausing the game
                            self.paused = False
                            self.pause_time += pygame.time.get_ticks() - self.pause_start_time  # Add pause duration to pause_time
                    if event.key == pygame.K_r and self.win:  # Restart game if 'R' is pressed on win screen
                        self.reset()
                        self.win = False    # Reset the win condition
                        self.starting = pygame.time.get_ticks()    # Restart the timer
                        self.pause_time = 0     #Reset pause time
                    if event.key == pygame.K_q and self.win:  # Return to main menu on 'Q'
                        pygame.event.clear()
                        self.reset()
                        self.win = False
                        return
                    if not self.paused and not self.game_over and not self.win:
                        if event.key == controls['hard_drop']:
                            self.hard_drop()
                        if event.key == controls['rotate']:
                            self.rotate()
                        if event.key == controls['rotate_ccw']:
                            self.rotate_counterclockwise()   
                        if event.key == controls['hold']:
                            self.hold()

                if event.type == GAME_UPDATE and not self.paused and not self.game_over and not self.win:
                    self.move_down()

            if not self.paused and not self.game_over and not self.win:
                keys = pygame.key.get_pressed()
                if keys[controls['left']] and current_time - move_left_timer > move_delay:
                    self.move_left()
                    move_left_timer = current_time
                if keys[controls['right']] and current_time - move_right_timer > move_delay:
                    self.move_right()
                    move_right_timer = current_time
                if keys[controls['down']] and current_time - move_down_timer > move_delay:
                    self.move_down()
                    self.update_score(0, 2)
                    move_down_timer = current_time

            if self.game_over:      # If the game is over, display the "GAME OVER" text
                back = Menus().gameover(screen, DISPLAY_WIDTH, DISPLAY_HEIGHT,self.score)
                self.reset()
                self.game_over = False
                if back == True:
                    return
                
            
            if self.win:    # If the game is over, display the "YOU WIN" text
                self.display_win(screen)
                pygame.display.update()
                clock.tick(FPS)
                continue  

            if self.paused:
                # Display pause menu and handle interactions
                menu_action = Menus().pause_menu(screen, speed, move_delay, DISPLAY_WIDTH, DISPLAY_HEIGHT)

                # Handle the returned action from the pause menu
                if menu_action == "resume":
                    pygame.event.clear()
                    self.pause_time += pygame.time.get_ticks() - self.pause_start_time # Add pause duration
                    self.paused = False  # Unpause the game
                elif menu_action == "restart":
                    self.reset()  # Reset the game state
                    pygame.event.clear()
                    self.paused = False  # Resume after restarting
                elif menu_action == "controls":
                    Menus().controls_menu(screen, controls, DISPLAY_WIDTH, DISPLAY_HEIGHT)
                    pygame.event.clear()
                    self.reset()  # Reset game state when returning to the main menu
                    self.paused = False  # Ensure the game is unpaused when coming back   
                elif menu_action == "main_menu":
                    pygame.event.clear()
                    Menus().main_menu(screen, DISPLAY_WIDTH, DISPLAY_HEIGHT)
                    self.reset()  # Reset game state when returning to the main menu
                    self.paused = False  # Ensure the game is unpaused when coming back
                    return

            # Draw the game state
            screen.fill(Colors.BLUE)
            score_value_surface = title_font.render(str(self.score), True, Colors.ORANGE)
            self.draw(screen)
            screen.blit(score_surface, (350, 20, 50, 50))
            screen.blit(next_surface, (360, 115, 50, 50))  # Draw the "Next" title for the next block preview

            time_rect = pygame.Rect(320, 550, 170, 65)  # Define a rectangle for the "hold" box
            pygame.draw.rect(screen, Colors.DARK_GREY, time_rect, 0, 10)

            pygame.draw.rect(screen, Colors.DARK_GREY, score_rect, 0, 10)
            screen.blit(score_value_surface, score_value_surface.get_rect(centerx=score_rect.centerx, centery=score_rect.centery))
            pygame.draw.rect(screen, Colors.DARK_GREY, next_rect, 0, 10)
            self.draw(screen)

            time_font = pygame.font.Font(None, 30)
            time_text = time_font.render(f"Time: {self.elapsed_time} s", True, Colors.ORANGE)
            screen.blit(time_text, (330, 555))

            lines_font = pygame.font.Font(None, 30)
            lines_cleared_text = lines_font.render(f"Lines: {self.lines_cleared}/{target_lines}", True, Colors.ORANGE)    # Use the lines_cleared variable
            screen.blit(lines_cleared_text, (330, 590))

            pygame.display.update()
            clock.tick(FPS)