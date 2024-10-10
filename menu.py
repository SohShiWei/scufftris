import sys
from settings import *

class Menus:
    def main_menu(self, screen, screen_width, screen_height):
        pygame.display.set_caption("Python Tetris Menu")
        
        while True:
            screen.fill(Colors.CYAN)

            menu_mouse_pos = pygame.mouse.get_pos()
            
            menu_text = pygame.font.Font(FONT_PATH, 100).render("PYTRIS", True, "black")
            menu_rect = menu_text.get_rect(center=(screen_width * 0.5, screen_height * 0.35))
            
            # Menu buttons
            play_button = Button(image=None, pos=(screen_width * 0.5, screen_height * 0.5), text_input="PLAY", font = pygame.font.Font(FONT_PATH, 50), base_color="black", hovering_color="red")
            settings_button = Button(image=None, pos=(screen_width * 0.5, screen_height * 0.6), text_input="SETTINGS", font = pygame.font.Font(FONT_PATH, 50), base_color="black", hovering_color="red")
            quit_button = Button(image=None, pos=(screen_width * 0.5, screen_height * 0.7), text_input="QUIT", font = pygame.font.Font(FONT_PATH, 50), base_color="black", hovering_color="red")
            
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
                        return "play"
                    if settings_button.checkForInput(menu_mouse_pos):
                        return "settings"
                    if quit_button.checkForInput(menu_mouse_pos):
                        pygame.quit()
                        sys.exit()
            
            pygame.display.update()

    def gameover(self, screen, screen_width, screen_height,score):
        pygame.display.set_caption("Game Over")
        print(score)
        game_over = False
        
        while True:
            screen.fill(Colors.CYAN)

            menu_mouse_pos = pygame.mouse.get_pos()
            
            menu_text = pygame.font.Font(FONT_PATH, 80).render("GAME OVER", True, "black")
            menu_text = pygame.font.Font(FONT_PATH, 80).render(str(score), True, "black")
            menu_rect = menu_text.get_rect(center=(screen_width * 0.5, screen_height * 0.35))
            
            # Menu buttons
            TryAgain_button = Button(image=None, pos=(screen_width * 0.5, screen_height * 0.5), text_input="TRY AGAIN?", font = pygame.font.Font(FONT_PATH, 50), base_color="black", hovering_color="red")
            Back_button = Button(image=None, pos=(screen_width * 0.5, screen_height * 0.6), text_input="BACK TO MENU", font = pygame.font.Font(FONT_PATH, 50), base_color="black", hovering_color="red")
            Quit_button = Button(image=None, pos=(screen_width * 0.5, screen_height * 0.7), text_input="QUIT", font = pygame.font.Font(FONT_PATH, 50), base_color="black", hovering_color="red")
            
            screen.blit(menu_text, menu_rect)
            
            for button in [TryAgain_button, Back_button, Quit_button]:
                button.changeColor(menu_mouse_pos)
                button.update(screen)
            
            for event in pygame.event.get():
                if event.type ==  pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if TryAgain_button.checkForInput(menu_mouse_pos):
                        return game_over
                    if Back_button.checkForInput(menu_mouse_pos):
                        self.main_menu(screen, DISPLAY_WIDTH, DISPLAY_HEIGHT)
                        return game_over
                    if Quit_button.checkForInput(menu_mouse_pos):
                        pygame.quit()
                        sys.exit()
            
            pygame.display.update()
        
    def pause_menu(self, screen,speed,move_delay):
        # Function to display the pause menu
        screen.fill(Colors.CYAN)  # Fill the screen with Cyan background
        
        # Render pause menu options (Resume, Quit, Speed adjustment)
        resume_surface = pygame.font.Font(FONT_PATH, 30).render("RESUME", True, "black")
        restart_surface = pygame.font.Font(FONT_PATH, 30).render("RESTART", True, "black")
        back_to_menu_surface = pygame.font.Font(FONT_PATH, 30).render("BACK TO MENU", True, Colors.BLACK)
        quit_surface = pygame.font.Font(FONT_PATH, 30).render("QUIT", True, Colors.BLACK)
        #drop down speed
        speed_surface = pygame.font.Font(FONT_PATH, 30).render(f"SPEED: {speed}", True, Colors.BLACK)
        decrease_speed_surface = pygame.font.Font(FONT_PATH, 20).render("SLOWER", True, Colors.BLACK)
        increase_speed_surface = pygame.font.Font(FONT_PATH, 20).render("FASTER", True, Colors.BLACK)
        #block moving speed
        move_surface = pygame.font.Font(FONT_PATH, 30).render(f"MOVEMENT: {move_delay}", True, Colors.BLACK)
        decrease_move_surface = pygame.font.Font(FONT_PATH, 20).render("SLOWER", True, Colors.BLACK)
        increase_move_surface = pygame.font.Font(FONT_PATH, 20).render("FASTER", True, Colors.BLACK)
        
        # Position the menu options
        resume_rect = resume_surface.get_rect(center=(250, 100))
        restart_rect = restart_surface.get_rect(center=(250, 150))
        back_to_menu_rect = back_to_menu_surface.get_rect(center=(250, 200))
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
        screen.blit(restart_surface, restart_rect)
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
        return resume_rect, restart_rect, quit_rect, increase_speed_rect, decrease_speed_rect, increase_move_rect, decrease_move_rect, back_to_menu_rect
    
    def show_settings_menu(self, screen, controls, screen_width, screen_height):
        # Display caption for settings
        pygame.display.set_caption("Settings Menu")
        
        def draw_buttons():
            # Define buttons for each control setting (Left, Right, Down, Rotate)
            left_button = Button(image=None, pos=(screen_width * 0.5, screen_height * 0.1), text_input=f'LEFT: {pygame.key.name(controls["left"]).upper()}', 
                                font=pygame.font.Font(FONT_PATH, 40), base_color="black", hovering_color="red")
            right_button = Button(image=None, pos=(screen_width * 0.5, screen_height * 0.2), text_input=f'RIGHT: {pygame.key.name(controls["right"]).upper()}', 
                                font=pygame.font.Font(FONT_PATH, 40), base_color="black", hovering_color="red")
            down_button = Button(image=None, pos=(screen_width * 0.5, screen_height * 0.3), text_input=f'DOWN: {pygame.key.name(controls["down"]).upper()}', 
                                font=pygame.font.Font(FONT_PATH, 40), base_color="black", hovering_color="red")
            rotate_button = Button(image=None, pos=(screen_width * 0.5, screen_height * 0.4), text_input=f'ROTATE: {pygame.key.name(controls["rotate"]).upper()}', 
                                font=pygame.font.Font(FONT_PATH, 40), base_color="black", hovering_color="red")
            hard_button = Button(image=None, pos=(screen_width * 0.5, screen_height * 0.5), text_input=f'HARD DROP: {pygame.key.name(controls["hard_drop"]).upper()}', 
                                font=pygame.font.Font(FONT_PATH, 40), base_color="black", hovering_color="red")
            default_button = Button(image=None, pos=(screen_width * 0.5, screen_height * 0.8), text_input=f'RETURN TO DEFAULT', 
                                font=pygame.font.Font(FONT_PATH, 35), base_color="black", hovering_color="red")
            back_button = Button(image=None, pos=(screen_width * 0.5, screen_height * 0.9), text_input='BACK TO MENU', 
                                font=pygame.font.Font(FONT_PATH, 50), base_color="black", hovering_color="red")          
            return left_button, right_button, down_button, rotate_button, hard_button, default_button, back_button
        
        # Draw the initial buttons
        left_button, right_button, down_button, rotate_button, hard_button, default_button, back_button = draw_buttons()
        
        while True:
            screen.fill(Colors.CYAN)  # Background color for settings menu
            mouse_pos = pygame.mouse.get_pos()

            # Display buttons and update color if hovered
            for button in [left_button, right_button, down_button, rotate_button, hard_button, back_button, default_button]:
                button.changeColor(mouse_pos)
                button.update(screen)

            button_remapped = False  # Flag to check if remap occurred

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                # Handle mouse click events
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if left_button.checkForInput(mouse_pos):
                        self.remap_control(screen, 'left', controls)
                        button_remapped = True
                    if right_button.checkForInput(mouse_pos):
                        self.remap_control(screen, 'right', controls)
                        button_remapped = True
                    if down_button.checkForInput(mouse_pos):
                        self.remap_control(screen, 'down', controls)
                        button_remapped = True
                    if rotate_button.checkForInput(mouse_pos):
                        self.remap_control(screen, 'rotate', controls)
                        button_remapped = True
                    if hard_button.checkForInput(mouse_pos):
                        self.remap_control(screen, 'hard_drop', controls)
                        button_remapped = True          
                    if default_button.checkForInput(mouse_pos):
                        controls = default_controls.copy()
                        button_remapped = True
                        print("Returned settings to default!")
                    if back_button.checkForInput(mouse_pos):
                        return  # Exit the settings menu and go back to the main menu

            if button_remapped:
                left_button, right_button, down_button, rotate_button, hard_button, default_button, back_button = draw_buttons()
                
            pygame.display.update()  # Ensure the display updates each frame
    
    def remap_control(self, screen, key_name, controls):
        prompt_font = pygame.font.Font(None, 40)
        prompt_text = f'PRESS NEW KEY FOR {key_name.upper()}'
        prompt_surface = prompt_font.render(prompt_text, True, Colors.BLACK)

        screen.fill((Colors.RED))  # Fill screen with dark background
        screen.blit(prompt_surface, (100, 100))  # Display prompt text
        pygame.display.flip()  # Update the display

        waiting_for_key = True
        while waiting_for_key:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    controls[key_name] = event.key  # Update the control with the new key
                    return  # Return back to the settings menu
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
