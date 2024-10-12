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
            self.score += 100
        elif lines_cleared == 2:
            self.score += 300
        elif lines_cleared == 3:
            self.score += 600
        elif lines_cleared == 4:
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
        screen.blit(win_text, (DISPLAY_WIDTH // 2 - 120, DISPLAY_HEIGHT // 2 - 50))

        font = pygame.font.Font(None, 36)
        restart_text = font.render("Press R to Retry Q to Main Menu", True, Colors.WHITE)
        screen.blit(restart_text, (DISPLAY_WIDTH // 2 - 200, DISPLAY_HEIGHT // 2 + 20))
        
    def play(self, screen):
        global speed, click_delay, move_delay, move_left_timer, move_right_timer, move_down_timer, last_click_time, controls
        # Main game loop (runs continuously)
        clock = pygame.time.Clock()

        GAME_UPDATE = pygame.USEREVENT
        pygame.time.set_timer(GAME_UPDATE, speed)
        
        # Score and Preview surface and rect and font
        title_font = pygame.font.Font(FONT_PATH, 30)  # Font for titles (e.g., "Score", "Next")

        score_surface = title_font.render("SCORE", True, Colors.BLACK)
        next_surface = title_font.render("NEXT", True, Colors.BLACK)
        
        score_rect = pygame.Rect(320, 55, 170, 60)
        next_rect = pygame.Rect(320, 215, 170, 180)

        self.starting = pygame.time.get_ticks()   # Start timer only when the game loop begins
        self.pause_time = 0  # Track how long the game is paused

        while True:
            current_time = pygame.time.get_ticks()

            # Calculate elapsed time
            if not self.paused and not self.game_over and not self.win:
                self.elapsed_time = (current_time - self.starting - self.pause_time) // 1000  # Subtract pause duration

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        if not self.paused:
                            # Pausing the game
                            self.paused = True
                            self.pause_start_time = pygame.time.get_ticks()  # Record when the pause starts
                        else:
                            # Unpausing the game
                            self.paused = False
                            self.pause_time += pygame.time.get_ticks() - self.pause_start_time  # Add pause duration to pause_time
                     
                    if event.key == pygame.K_r and self.win:  # Restart game if 'R' is pressed on win screen
                        self.reset()
                        self.win = False  # Reset the win condition
                        self.starting = pygame.time.get_ticks()  # Restart the timer
                        self.pause_time = 0 #reset pause time
                    if event.key == pygame.K_q and self.win:  # return to main menu on Q
                        pygame.event.clear()
                        self.reset()
                        self.win = False  # Reset the win condition
                        return
                    if not self.paused and not self.game_over and not self.win:
                        if event.key == controls['hard_drop']:
                            self.hard_drop()
                        if event.key == controls['rotate']:
                            self.rotate()
                        if event.key == controls['hold']:
                            self.hold()
                            
                if event.type == GAME_UPDATE and not self.paused and not self.game_over and not self.win:
                    self.move_down()

            if not self.paused and not self.game_over and not self.win:
                keys = pygame.key.get_pressed()
                if (keys[controls['left']]) and current_time - move_left_timer > move_delay:
                    self.move_left()
                    move_left_timer = current_time
                if (keys[controls['right']]) and current_time - move_right_timer > move_delay:
                    self.move_right()
                    move_right_timer = current_time
                if (keys[controls['down']]) and current_time - move_down_timer > move_delay:
                    self.move_down()
                    self.update_score(0, 2)
                    move_down_timer = current_time

            if self.game_over:  # If the game is over, display the "GAME OVER" text
                self.game_over = Menus().gameover(screen, DISPLAY_WIDTH, DISPLAY_HEIGHT,self.score)
                self.reset()
                self.game_over = False
                return

            elif self.win:  # If the game is over, display the "YOU WIN" text
                self.display_win(screen)
 
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
                
             # Draw game state
            score_value_surface = title_font.render(str(self.score), True, Colors.WHITE)
            screen.fill(Colors.DARK_BLUE)
            self.draw(screen)
            title_font.render("GAME OVER", True, Colors.WHITE)
            screen.blit(score_surface, (365, 20, 50, 50))
            screen.blit(next_surface, (375, 180, 50, 50))
            
            pygame.draw.rect(screen, Colors.LIGHT_BLUE, score_rect, 0, 10)
            screen.blit(score_value_surface, score_value_surface.get_rect(centerx=score_rect.centerx, centery=score_rect.centery))
            pygame.draw.rect(screen, Colors.LIGHT_BLUE, next_rect, 0, 10)
            self.draw(screen)

            time_font = pygame.font.Font(None, 30)
            time_text = time_font.render(f"Time: {self.elapsed_time}", True, Colors.WHITE)
            screen.blit(time_text, (320, 555))

            lines_font = pygame.font.Font(None, 30)
            lines_cleared_text = lines_font.render(f"Lines cleared: {self.lines_cleared}", True, Colors.WHITE)  # Use the lines_cleared variable
            screen.blit(lines_cleared_text, (320, 590))
               
            pygame.display.update()
            clock.tick(FPS)