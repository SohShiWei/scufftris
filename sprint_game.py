import pygame
import sys
from game import Game
from blocks import *
from settings import *
from colors import Colors

class SprintGame(Game):
    def __init__(self):
        super().__init__()
        self.start_time = pygame.time.get_ticks()  # Store the starting time
        self.time_limit = 120000  # 2 minutes in milliseconds (120,000ms)
        self.speed_increment_threshold = 500  # Increase speed every 500 score points
        self.speed = 300  # Initial speed (can be modified)
        self.current_speed = self.speed  # Track current speed based on score
        self.game_ended = False

    def play(self, screen):
        clock = pygame.time.Clock()
        self.paused = False
        self.last_click_time = 0
        self.click_delay = 300
        
        # Custom event for game update every few milliseconds
        GAME_UPDATE = pygame.USEREVENT
        pygame.time.set_timer(GAME_UPDATE, self.speed)  # Set the event to trigger every `speed` milliseconds

        move_left_timer, move_right_timer, move_down_timer = 0, 0, 0
        move_delay = 100
        
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

            # Draw game state
            screen.fill(Colors.dark_blue)
            self.draw(screen)
            
            if self.paused:
                # Implement the pause menu as in the original game logic
                pass
            
            # Display the countdown timer
            time_left = max(0, self.time_limit - elapsed_time) // 1000  # Convert to seconds
            font = pygame.font.Font(FONT_PATH, 15)
            timer_text = font.render(f"TIME LEFT: {time_left}S", True, Colors.white)
            screen.blit(timer_text, (350, 50))  # Display timer at the top-left

            pygame.display.update()
            clock.tick(FPS)

        self.end_game(screen)  # Call a function to handle end-game (e.g., showing score)

    def increase_speed(self, score):
        # Every 500 points, increase the block falling speed
        new_speed = max(50, self.speed - (score // self.speed_increment_threshold) * 50)  # Reduce speed
        if new_speed != self.current_speed:
            self.current_speed = new_speed
            pygame.time.set_timer(pygame.USEREVENT, self.current_speed)


    def end_game(self, screen):  
        font = pygame.font.Font(FONT_PATH, 50)
        game_over_text = font.render("TIME'S UP!", True, Colors.red)
        score_text = font.render(f"FINAL SCORE: {self.score}", True, Colors.orange)
        
        # Get the width and height of the texts
        game_over_text_rect = game_over_text.get_rect(center=(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2 - 50))
        score_text_rect = score_text.get_rect(center=(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2 + 10))
        
        # Display the game over messages
        screen.blit(game_over_text, game_over_text_rect)
        screen.blit(score_text, score_text_rect)
        
        pygame.display.update()
        pygame.time.wait(3500)  # Wait before returning to the menu
