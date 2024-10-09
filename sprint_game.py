import pygame
import sys
from game import Game
from settings import *
from colors import Colors

class SprintGame(Game):
    def __init__(self, target_lines):
        super().__init__()  # Call the initializer of the Game class
        self.target_lines = target_lines  # Number of lines to clear
        self.elapsed_time = 0  # Timer starts at 0
        self.game_over = False  # Initialize game over status
        self.win = False  # Initialize win status

    def play(self, screen):
        clock = pygame.time.Clock()
        self.paused = False
        speed = 300
        GAME_UPDATE = pygame.USEREVENT
        pygame.time.set_timer(GAME_UPDATE, speed)

        move_left_timer, move_right_timer, move_down_timer = 0, 0, 0
        move_delay = 100


        self.starting = pygame.time.get_ticks()   # Start timer only when the game loop begins
        
        while True:
            current_time = pygame.time.get_ticks()  # Get current time in milliseconds

            if not self.game_over and not self.win:
                self.elapsed_time = (current_time - self.starting) // 1000  # Convert to seconds

            if self.score // 100 >= self.target_lines:  # Check lines are cleared
                self.win = True  # Win condition

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.paused = not self.paused
                    if not self.paused and not self.game_over and not self.win:
                        if event.key == controls['hard_drop']:
                            self.hard_drop()
                        if event.key == controls['rotate']:
                            self.rotate()
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
                    self.update_score(0, 1)

            screen.fill(Colors.dark_blue)
            self.draw(screen)

            time_font = pygame.font.Font(None, 30)  # Display elapsed time
            time_text = time_font.render(f"Time: {self.elapsed_time}", True, colors.WHITE)
            screen.blit(time_text, (320, 555))

            lines_font = pygame.font.Font(None, 30)  # Display lines cleared
            lines_cleared_text = lines_font.render(f"Lines cleared: {self.score // 100}", True, colors.WHITE)
            screen.blit(lines_cleared_text, (320, 590))

            if self.game_over:
                self.display_game_over(screen)
            elif self.win:  
                self.display_win(screen)  # Display win screen

            pygame.display.update()
            clock.tick(FPS)

    def display_game_over(self, screen): # Display the game over
        font = pygame.font.Font(None, 74)
        game_over_text = font.render("Game Over!", True, colors.YELLOW)
        screen.blit(game_over_text, (DISPLAY_WIDTH // 2 - 150, DISPLAY_HEIGHT // 2 - 50))

        font = pygame.font.Font(None, 36)
        restart_text = font.render("Press R to Restart or Q to Quit", True, colors.WHITE)
        screen.blit(restart_text, (DISPLAY_WIDTH // 2 - 180, DISPLAY_HEIGHT // 2 + 20))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            self.reset()
            self.play(screen)
        elif keys[pygame.K_q]:
            pygame.quit()
            sys.exit()

    def display_win(self, screen):  # Display the win screen 
        font = pygame.font.Font(None, 74)
        win_text = font.render("You Win!", True, colors.GREEN)
        screen.blit(win_text, (DISPLAY_WIDTH // 2 - 150, DISPLAY_HEIGHT // 2 - 50))

        font = pygame.font.Font(None, 36)
        restart_text = font.render("Press R to Restart or Q to Quit", True, colors.WHITE)
        screen.blit(restart_text, (DISPLAY_WIDTH // 2 - 180, DISPLAY_HEIGHT // 2 + 20))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            self.reset()
            self.play(screen)
        elif keys[pygame.K_q]:
            pygame.quit()
            sys.exit()
