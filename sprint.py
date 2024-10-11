import pygame
import sys
from game import Game
from settings import *
from menu import *
from blocks import *

class Sprint(Game):
    def __init__(self, time_limit):
        super().__init__()
        self.time_limit = time_limit
        self.start_time = pygame.time.get_ticks()  # Store the starting time
        self.speed = speed  # Initial speed (can be modified)
        self.speed_increment_threshold= speed_increment_threshold
        self.current_speed = self.speed  # Track current speed based on score
        self.game_ended = False
        
    def reset(self):
        # Resets the game to the initial state (empty grid, new blocks, reset score)
        self.grid.reset()  # Reset the grid
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]  # Reset block list
        self.current_block = self.get_random_block()  # Start with a new block
        self.next_block = self.get_random_block()  # Prepare the next block
        self.score = 0  # Reset score
        self.starting = pygame.time.get_ticks()
        self.game_ended = False  # Reset the end game state
        self.paused = False  # Unpause the game
        self.time_limit = time_limit
        
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
        self.score += move_down_points  # Add points for moving blocks down  
        
    def increase_speed(self, score):
        # Every 500 points, increase the block falling speed
        new_speed = max(50, self.speed - (score // self.speed_increment_threshold) * 50)  # Reduce speed
        if new_speed != self.current_speed:
            self.current_speed = new_speed
            pygame.time.set_timer(pygame.USEREVENT, self.current_speed)

    def end_game(self, screen):  
        font = pygame.font.Font(FONT_PATH, 50)
        game_over_text = font.render("TIME'S UP!", True, Colors.RED)
        score_text = font.render(f"FINAL SCORE: {self.score}", True, Colors.ORANGE)
        
        # Get the width and height of the texts
        game_over_text_rect = game_over_text.get_rect(center=(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2 - 50))
        score_text_rect = score_text.get_rect(center=(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2 + 10))
        
        # Display the game over messages
        screen.blit(game_over_text, game_over_text_rect)
        screen.blit(score_text, score_text_rect)
        
        pygame.display.update()
        pygame.time.wait(3500)  # Wait before returning to the menu    
        
    def play(self, screen):
        
        global speed, click_delay, move_delay, move_left_timer, move_right_timer, move_down_timer, last_click_time, controls, speed_increment_threshold
        
        clock = pygame.time.Clock()
        
        # Custom event for game update every few milliseconds
        GAME_UPDATE = pygame.USEREVENT
        pygame.time.set_timer(GAME_UPDATE, self.speed)  # Set the event to trigger every `speed` milliseconds
        
        # Score and Preview surface and rect and font
        title_font = pygame.font.Font(FONT_PATH, 30)  # Font for titles (e.g., "Score", "Next")

        score_surface = title_font.render("SCORE", True, Colors.BLACK)
        next_surface = title_font.render("NEXT", True, Colors.BLACK)
        
        score_rect = pygame.Rect(320, 55, 170, 60)
        next_rect = pygame.Rect(320, 215, 170, 180)
        
        while not self.game_over and not self.game_ended:
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - self.start_time  # Time since the game started
            
            if elapsed_time >= self.time_limit:
                self.game_ended = True  # End the game after 2 minutes

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.paused = not self.paused
                    if not self.paused and not self.game_over:
                        if event.key == controls['hard_drop']:
                            self.hard_drop()
                        if event.key == controls['rotate']:
                            self.rotate()
                            
                if event.type == GAME_UPDATE and not self.paused and not self.game_over:
                    self.move_down()

            if not self.paused and not self.game_over:
                keys = pygame.key.get_pressed()
                if (keys[controls['left']]) and current_time - move_left_timer > move_delay:
                    self.move_left()
                    move_left_timer = current_time
                if (keys[controls['right']]) and current_time - move_right_timer > move_delay:
                    self.move_right()
                    move_right_timer = current_time
                if (keys[controls['down']]) and current_time - move_down_timer > move_delay:
                    self.move_down()
                    self.update_score(0, 1)

            # Adjust speed based on score
            if self.score // self.speed_increment_threshold > 0:
                self.increase_speed(self.score)     
            
            if self.paused:
                #Display pause menu and handle interations
                menu_action = Menus().pause_menu(screen, speed, move_delay, DISPLAY_WIDTH, DISPLAY_HEIGHT)
                
                # Handle the returned action from the pause menu
                if menu_action == "resume":
                    pygame.event.clear()
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
            screen.blit(score_surface, (365, 20, 50, 50))
            screen.blit(next_surface, (375, 180, 50, 50))
            
            pygame.draw.rect(screen, Colors.LIGHT_BLUE, score_rect, 0, 10)
            screen.blit(score_value_surface, score_value_surface.get_rect(centerx=score_rect.centerx, centery=score_rect.centery))
            pygame.draw.rect(screen, Colors.LIGHT_BLUE, next_rect, 0, 10)
            self.draw(screen)
            
            # Display the countdown timer
            time_left = max(0, self.time_limit - elapsed_time) // 1000  # Convert to seconds
            font = pygame.font.Font(FONT_PATH, 15)
            timer_text = font.render(f"TIME LEFT: {time_left} S", True, Colors.WHITE)
            screen.blit(timer_text, (350, 590))  # Display timer at the bottom-right

            pygame.display.update()
            clock.tick(FPS)

        self.end_game(screen)  # Call a function to handle end-game (e.g., showing score)