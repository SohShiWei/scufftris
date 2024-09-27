
import pygame, sys

# Set up the game window with dimensions (720x620) and background image
screen_width = 720
screen_height = 620
screen = pygame.display.set_mode((screen_width, screen_height))

# Rectangles for positioning the game play section
game_screen_width = screen_width * 0.8
game_screen_height = screen_height
game_screen = pygame.Surface((screen_width, screen_height))

# Calculate dimensions for the play area and the sidebars
left_sidebar_width = screen_width * 0.2  # 20% width for the left sidebar
game_screen_width = screen_width * 0.6  # 60% width for the game area
right_sidebar_width = screen_width * 0.2  # 20% width for the right sidebar
right_sidebar_height = screen_height # 100% of the height for the right sidebar

# Rectangles for the game area and the sidebars
left_sidebar_rect = pygame.Rect(0, 0, left_sidebar_width, screen_height)  # Left sidebar for the score
game_screen_rect = pygame.Rect(left_sidebar_width, 0, game_screen_width, screen_height)  # Main game screen
right_sidebar_rect = pygame.Rect(left_sidebar_width + game_screen_width, 0, right_sidebar_width, screen_height)  # Right sidebar for the next block

# Set up rectangles for the Next Block preview and Score within the right sidebar
next_rect = pygame.Rect(right_sidebar_rect.x, 0, right_sidebar_width, right_sidebar_height * 0.7)  # Next block occupies 70% of the height
score_rect = pygame.Rect(right_sidebar_rect.x, right_sidebar_height * 0.7, right_sidebar_width, right_sidebar_height * 0.3)  # Score occupies bottom 30%

background_img = pygame.image.load("assets/cover.png")