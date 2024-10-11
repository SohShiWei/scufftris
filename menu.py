import sys
#import pygame_menu
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
            play_button = Button(image=None, pos=(screen_width * 0.5, screen_height * 0.5), text_input="PLAY", font=pygame.font.Font(FONT_PATH, 50), base_color="black", hovering_color="red")
            sprint_button = Button(image=None, pos=(screen_width * 0.5, screen_height * 0.60), text_input="SPRINT MODE", font=pygame.font.Font(FONT_PATH, 50), base_color="black", hovering_color="red")
            settings_button = Button(image=None, pos=(screen_width * 0.5, screen_height * 0.70), text_input="SETTINGS", font=pygame.font.Font(FONT_PATH, 50), base_color="black", hovering_color="red")
            quit_button = Button(image=None, pos=(screen_width * 0.5, screen_height * 0.80), text_input="QUIT", font=pygame.font.Font(FONT_PATH, 50), base_color="black", hovering_color="red")
            
            screen.blit(menu_text, menu_rect)
            
            for button in [play_button, settings_button, quit_button, sprint_button]:
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
                    if sprint_button.checkForInput(menu_mouse_pos): 
                        return "sprint"
                    if quit_button.checkForInput(menu_mouse_pos):
                        pygame.quit()
                        sys.exit()
            
            pygame.display.update()

    def gameover(self, screen, screen_width, screen_height,score):
        pygame.display.set_caption("Game Over!")
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
        
    def pause_menu(self, screen, speed, move_delay, screen_width, screen_height):
        
        pygame.display.set_caption("Game Paused!")
        
        def draw_buttons():
            # Define buttons for each control setting (Left, Right, Down, Rotate)
            
            # Menu buttons
            resume_button = Button(image=None, pos=(screen_width * 0.5, screen_height * 0.1), text_input="RESUME", font = pygame.font.Font(FONT_PATH, 50), base_color="black", hovering_color="red")
            restart_button = Button(image=None, pos=(screen_width * 0.5, screen_height * 0.3), text_input="RESTART", font = pygame.font.Font(FONT_PATH, 50), base_color="black", hovering_color="red")
            controls_button = Button(image=None, pos=(screen_width * 0.5, screen_height * 0.5), text_input="CONTROLS", font = pygame.font.Font(FONT_PATH, 50), base_color="black", hovering_color="red")
            main_menu_button = Button(image=None, pos=(screen_width * 0.5, screen_height * 0.7), text_input="MAIN MENU", font = pygame.font.Font(FONT_PATH, 50), base_color="black", hovering_color="red")
            quit_button = Button(image=None, pos=(screen_width * 0.5, screen_height * 0.9), text_input="QUIT", font = pygame.font.Font(FONT_PATH, 50), base_color="black", hovering_color="red")
            
            return resume_button, restart_button, controls_button, main_menu_button, quit_button
        
        # Draw the initial buttons
        resume_button, restart_button, controls_button, main_menu_button, quit_button = draw_buttons()
        
        while True:
            screen.fill(Colors.CYAN)  # Background color for settings menu
            mouse_pos = pygame.mouse.get_pos()
            
            for button in [resume_button, restart_button, controls_button, main_menu_button, quit_button]:
                    button.changeColor(mouse_pos)
                    button.update(screen)  
                    
            for event in pygame.event.get():
                if event.type ==  pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if resume_button.checkForInput(mouse_pos):
                        return"resume"
                    if restart_button.checkForInput(mouse_pos):
                        return "restart"
                    if controls_button.checkForInput(mouse_pos):
                        return "controls"
                    if main_menu_button.checkForInput(mouse_pos):
                        return "main_menu"
                    if quit_button.checkForInput(mouse_pos):
                        pygame.quit()
                        sys.exit()
            
            pygame.display.update()
    
    def show_settings_menu(self, screen, controls, screen_width, screen_height):
        pygame.display.set_caption("Settings Menu")
        
        def draw_buttons():
            # Define buttons for each control setting (Left, Right, Down, Rotate)
            
            # Menu buttons
            controls_button = Button(image=None, pos=(screen_width * 0.5, screen_height * 0.5), text_input="CONTROLS", font = pygame.font.Font(FONT_PATH, 50), base_color="black", hovering_color="red")
            handling_button = Button(image=None, pos=(screen_width * 0.5, screen_height * 0.6), text_input="HANDLING", font = pygame.font.Font(FONT_PATH, 50), base_color="black", hovering_color="red")
            back_button = Button(image=None, pos=(screen_width * 0.5, screen_height * 0.7), text_input="BACK", font = pygame.font.Font(FONT_PATH, 50), base_color="black", hovering_color="red")
            return controls_button, handling_button, back_button
        
        # Draw the initial buttons
        controls_button, handling_button, back_button = draw_buttons()
        while True:
            screen.fill(Colors.CYAN)  # Background color for settings menu
            mouse_pos = pygame.mouse.get_pos()
            
            for button in [controls_button, handling_button, back_button]:
                    button.changeColor(mouse_pos)
                    button.update(screen)  
                    
            for event in pygame.event.get():
                if event.type ==  pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if controls_button.checkForInput(mouse_pos):
                        self.controls_menu(screen, controls, screen_width, screen_height)
                    if handling_button.checkForInput(mouse_pos):
                        self.handling_menu(screen, screen_width, screen_height)
                    if back_button.checkForInput(mouse_pos):
                        return
            
            pygame.display.update()
            
    def controls_menu(self, screen, controls, screen_width, screen_height):
        # Display caption for settings
        pygame.display.set_caption("Controls Menu")
        
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
            back_button = Button(image=None, pos=(screen_width * 0.5, screen_height * 0.9), text_input='BACK', 
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
                        self.remap_control(screen, 'left', controls, screen_height, screen_width)
                        button_remapped = True
                    if right_button.checkForInput(mouse_pos):
                        self.remap_control(screen, 'right', controls, screen_height, screen_width)
                        button_remapped = True
                    if down_button.checkForInput(mouse_pos):
                        self.remap_control(screen, 'down', controls, screen_height, screen_width)
                        button_remapped = True
                    if rotate_button.checkForInput(mouse_pos):
                        self.remap_control(screen, 'rotate', controls, screen_height, screen_width)
                        button_remapped = True
                    if hard_button.checkForInput(mouse_pos):
                        self.remap_control(screen, 'hard_drop', controls, screen_height, screen_width)
                        button_remapped = True          
                    if default_button.checkForInput(mouse_pos):
                        controls = default_controls.copy()
                        button_remapped = True
                        print("Returned settings to default!")
                    if back_button.checkForInput(mouse_pos):
                        return 

            if button_remapped:
                left_button, right_button, down_button, rotate_button, hard_button, default_button, back_button = draw_buttons()
                
            pygame.display.update()  # Ensure the display updates each frame
    
    def remap_control(self, screen, key_name, controls, screen_height, screen_width):
        prompt_font = pygame.font.Font(None, 40)
        prompt_text = f'PRESS NEW KEY FOR {key_name.upper()}'
        prompt_surface = prompt_font.render(prompt_text, True, Colors.BLACK)

        screen.fill((Colors.CYAN))  # Fill screen with dark background
        prompt_rect = prompt_surface.get_rect(center=(screen_width * 0.5, screen_height * 0.5))
        screen.blit(prompt_surface, prompt_rect)  # Display prompt text
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
    
    def handling_menu(self, screen, screen_width, screen_height):
        pygame.display.set_caption("Game Configuration")
        
        global speed, move_delay
        
        speed_surface = pygame.font.Font(FONT_PATH, 30).render(f"SPEED: {speed}", True, Colors.BLACK)
        move_surface = pygame.font.Font(FONT_PATH, 30).render(f"MOVEMENT: {move_delay}", True, Colors.BLACK)
        decrease_speed_button = Button(image=None, pos=(screen_width * 0.25, screen_height * 0.15), text_input="SLOWER", font=pygame.font.Font(FONT_PATH, 20), base_color="black", hovering_color="red")
        increase_speed_button = Button(image=None, pos=(screen_width * 0.75, screen_height * 0.15), text_input="FASTER", font=pygame.font.Font(FONT_PATH, 20), base_color="black", hovering_color="red")
        decrease_move_button = Button(image=None, pos=(screen_width * 0.25, screen_height * 0.35), text_input="SLOWER", font=pygame.font.Font(FONT_PATH, 20), base_color="black", hovering_color="red")
        increase_move_button = Button(image=None, pos=(screen_width * 0.75, screen_height * 0.35), text_input="FASTER", font=pygame.font.Font(FONT_PATH, 20), base_color="black", hovering_color="red")
        back_button = Button(image=None, pos=(screen_width * 0.5, screen_height * 0.9), text_input='BACK', font=pygame.font.Font(FONT_PATH, 50), base_color="black", hovering_color="red")
        
        while True:
            screen.fill(Colors.CYAN)
            mouse_pos = pygame.mouse.get_pos()

            for button in [decrease_speed_button, increase_speed_button, decrease_move_button, increase_move_button, back_button]:
                button.changeColor(mouse_pos)
                button.update(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if decrease_speed_button.checkForInput(mouse_pos):
                        speed = min(speed + 50, 1000)
                    if increase_speed_button.checkForInput(mouse_pos):
                        speed = max(speed - 50, 50)
                    if decrease_move_button.checkForInput(mouse_pos):
                        move_delay = min(move_delay + 10, 500)
                    if increase_move_button.checkForInput(mouse_pos):
                        move_delay = max(move_delay - 10, 50)
                    if back_button.checkForInput(mouse_pos):
                        return
                        
            # Update the text surfaces for speed and movement delay
            speed_surface = pygame.font.Font(FONT_PATH, 30).render(f"SPEED: {speed}", True, Colors.BLACK)
            move_surface = pygame.font.Font(FONT_PATH, 30).render(f"MOVEMENT: {move_delay}", True, Colors.BLACK)
            screen.blit(speed_surface, (screen_width * 0.25, screen_height * 0.05))
            screen.blit(move_surface, (screen_width * 0.25, screen_height * 0.25))
            pygame.display.update() 
        
        
        
