import sys
#import pygame_menu
from settings import *
        
class Menus:
    def main_menu(self, screen, screen_width, screen_height):
        pygame.event.clear()
        pygame.display.set_caption("Python Tetris Menu")

        screen.fill(Colors.BLUE)
        
        while True:

            # Render title with outline or shadow for a more appealing look
            title_font = pygame.font.Font(FONT_PATH, 120)

            # Create shadow effect by rendering the title slightly offset
            title_shadow = title_font.render("PYTRIS", True, Colors.BLACK)
            titleshadow_rect = title_shadow.get_rect(center=(screen_width * 0.5+5, screen_height * 0.1+5))
            screen.blit(title_shadow, titleshadow_rect)

            menu_mouse_pos = pygame.mouse.get_pos()
            
             # Render the title
            title_text = title_font.render("PYTRIS", True, Colors.ORANGE)
            title_rect = title_text.get_rect(center=(screen_width * 0.5, screen_height * 0.1))
            screen.blit(title_text, title_rect)
            
            # Menu buttons
            play_button = Button(image=None, pos=(screen_width * 0.5, screen_height * 0.35), text_input="SURVIVAL", font=pygame.font.Font(FONT_PATH, 50), base_color=Colors.GREEN, hovering_color="red")
            clear40_button = Button(image=None, pos=(screen_width * 0.5, screen_height * 0.45), text_input="40 LINES", font=pygame.font.Font(FONT_PATH, 50), base_color=Colors.GREEN, hovering_color="red")
            sprint_button = Button(image=None, pos=(screen_width * 0.5, screen_height * 0.55), text_input="SPRINT", font=pygame.font.Font(FONT_PATH, 50), base_color=Colors.GREEN, hovering_color="red")
            settings_button = Button(image=None, pos=(screen_width * 0.5, screen_height * 0.80), text_input="SETTINGS", font=pygame.font.Font(FONT_PATH, 50), base_color=Colors.PINK, hovering_color="red")
            quit_button = Button(image=None, pos=(screen_width * 0.5, screen_height * 0.90), text_input="QUIT", font=pygame.font.Font(FONT_PATH, 50), base_color=Colors.YELLOW, hovering_color="red")
            
            for button in [play_button, settings_button, quit_button, clear40_button, sprint_button]:
                button.changeColor(menu_mouse_pos)
                button.update(screen)
            
            for event in pygame.event.get():
                if event.type ==  pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.checkForInput(menu_mouse_pos):
                        pygame.event.clear()
                        return "play"
                    if clear40_button.checkForInput(menu_mouse_pos): 
                        pygame.event.clear()
                        return "clear40"
                    if sprint_button.checkForInput(menu_mouse_pos): 
                        pygame.event.clear()
                        return "sprint"
                    if settings_button.checkForInput(menu_mouse_pos):
                        pygame.event.clear()
                        return "settings"
                    if quit_button.checkForInput(menu_mouse_pos):
                        pygame.quit()
                        sys.exit()
            
            pygame.display.update()

    def gameover(self, screen, screen_width, screen_height, score):
        pygame.display.set_caption("Game Over!")
        game_over = False

        pygame.mixer.music.pause()

         # Load the game over sound (ensure the file exists)
        gameover_sound = pygame.mixer.Sound("Sounds/gameover.mp3")
        gameover_sound.set_volume(0)  # Set volume if needed
        gameover_sound.play()  # Play the sound

        fade_in_duration = 2000  # 2 seconds fade-in
        start_time = pygame.time.get_ticks()

        while True:
            # screen.fill(Colors.DARK_PURPLE)

            # Semi-transparent overlay
            overlay = pygame.Surface((screen_width, screen_height))
            overlay.set_alpha(150)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))

            elapsed_time = pygame.time.get_ticks() - start_time

            # Fade-in effect for the "Game Over" text
            if elapsed_time < fade_in_duration:
                alpha_value = min(255, int((elapsed_time / fade_in_duration) * 255))  # Calculate alpha based on time
            else:
                alpha_value = 255  # Full opacity after fade-in

            # Game Over text with outline
            gameover_font = pygame.font.Font(FONT_PATH, 75)

            # Create the main text surface
            gameover_text = gameover_font.render("GAME OVER", True, Colors.LIGHT_RED)
            gameover_text.set_alpha(alpha_value)
            gameover_rect = gameover_text.get_rect(center=(screen_width * 0.5, screen_height * 0.2))

            # Outline color
            outline_color = Colors.WHITE

            # Create outline by rendering the text slightly offset in different directions
            outline_offsets = [(-2, -2), (-2, 2), (2, -2), (2, 2)]  # Corners for the outline

            for offset in outline_offsets:
                outline_text = gameover_font.render("GAME OVER", True, outline_color)
                outline_text.set_alpha(alpha_value)  # Apply the same alpha value for the fade-in effect
                screen.blit(outline_text, outline_text.get_rect(center=(gameover_rect.centerx + offset[0], gameover_rect.centery + offset[1])))

            # Finally, blit the main text on top of the outline
            screen.blit(gameover_text, gameover_rect)

            # Score text
            score_font = pygame.font.Font(FONT_PATH, 50)
            score_text = score_font.render(f"SCORE: {score}", True, Colors.WHITE)
            score_rect = score_text.get_rect(center=(screen_width * 0.5, screen_height * 0.35))
            screen.blit(score_text, score_rect)

            # Menu buttons
            try_again_button = Button(
                image=None,pos=(screen_width * 0.5, screen_height * 0.55),text_input="TRY AGAIN?",font=pygame.font.Font(FONT_PATH, 50),base_color=Colors.WHITE,hovering_color=Colors.LIGHT_RED
            )
            back_button = Button(
                image=None,pos=(screen_width * 0.5, screen_height * 0.65),text_input="MENU",font=pygame.font.Font(FONT_PATH, 50),base_color=Colors.WHITE,hovering_color=Colors.LIGHT_RED
            )

            # Draw buttons
            for button in [try_again_button, back_button]:
                button.changeColor(pygame.mouse.get_pos())
                button.update(screen)

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if try_again_button.checkForInput(pygame.mouse.get_pos()):
                        pygame.event.clear()
                        pygame.mixer.music.rewind()  # Rewind the background music to the start
                        pygame.mixer.music.unpause()  # Resume the background music
                        return
                    if back_button.checkForInput(pygame.mouse.get_pos()):
                        back = True
                        pygame.event.clear()
                        self.main_menu(screen, DISPLAY_WIDTH, DISPLAY_HEIGHT)
                        pygame.mixer.music.rewind()  # Rewind the background music to the start
                        pygame.mixer.music.unpause()  # Resume the background music
                        return back

            # Update display
            pygame.display.update()
        
    def pause_menu(self, screen, speed, move_delay, screen_width, screen_height):
        
        pygame.display.set_caption("Game Paused!")
        
        def draw_buttons():
            
            rect_surface = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.SRCALPHA)
            rect_surface.fill(Colors.TLIGHT_BLUE)  # Semi-transparent red

            # Blit the surface onto the main screen
            screen.blit(rect_surface, (0,0))
            pygame.display.flip()


            
            # Render title with outline or shadow for a more appealing look
            title_font = pygame.font.Font(FONT_PATH, 100)

            # Create shadow effect by rendering the title slightly offset
            title_shadow = title_font.render("PAUSED", True, Colors.BLACK)
            titleshadow_rect = title_shadow.get_rect(center=(screen_width * 0.5+5, screen_height * 0.2+5))
            screen.blit(title_shadow, titleshadow_rect)
            
             # Render the title
            title_text = title_font.render("PAUSED", True, Colors.WHITE)
            title_rect = title_text.get_rect(center=(screen_width * 0.5, screen_height * 0.2))
            screen.blit(title_text, title_rect)

            # Menu buttons
            resume_button = Button(image=None, pos=(screen_width * 0.5, screen_height * 0.4), text_input="RESUME", font = pygame.font.Font(FONT_PATH, 50), base_color="black", hovering_color="red")
            restart_button = Button(image=None, pos=(screen_width * 0.5, screen_height * 0.5), text_input="RESTART", font = pygame.font.Font(FONT_PATH, 50), base_color="black", hovering_color="red")
            controls_button = Button(image=None, pos=(screen_width * 0.5, screen_height * 0.6), text_input="CONTROLS", font = pygame.font.Font(FONT_PATH, 50), base_color="black", hovering_color="red")
            main_menu_button = Button(image=None, pos=(screen_width * 0.5, screen_height * 0.7), text_input="MAIN MENU", font = pygame.font.Font(FONT_PATH, 50), base_color="black", hovering_color="red")
            quit_button = Button(image=None, pos=(screen_width * 0.5, screen_height * 0.9), text_input="QUIT", font = pygame.font.Font(FONT_PATH, 50), base_color="black", hovering_color="red")
            
            return resume_button, restart_button, controls_button, main_menu_button, quit_button
        
        # Draw the initial buttons
        resume_button, restart_button, controls_button, main_menu_button, quit_button = draw_buttons()
        
        while True:
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
                        pygame.event.clear()
                        return"resume"
                    if restart_button.checkForInput(mouse_pos):
                        pygame.event.clear()
                        return "restart"
                    if controls_button.checkForInput(mouse_pos):
                        pygame.event.clear()
                        game_snapshot = screen.copy()
                        Menus().controls_menu(screen, controls, screen_width, screen_height)
                        screen.blit(game_snapshot, (0, 0))
                        continue
                    if main_menu_button.checkForInput(mouse_pos):
                        pygame.event.clear()
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
            controls_button = Button(image=None, pos=(screen_width * 0.5, screen_height * 0.3), text_input="CONTROLS", font = pygame.font.Font(FONT_PATH, 50), base_color="black", hovering_color="red")
            handling_button = Button(image=None, pos=(screen_width * 0.5, screen_height * 0.4), text_input="HANDLING", font = pygame.font.Font(FONT_PATH, 50), base_color="black", hovering_color="red")
            back_button = Button(image=None, pos=(screen_width * 0.5, screen_height * 0.7), text_input="BACK", font = pygame.font.Font(FONT_PATH, 50), base_color="black", hovering_color="red")
            return controls_button, handling_button, back_button
        
        # Draw the initial buttons
        controls_button, handling_button, back_button = draw_buttons()
        while True:
            screen.fill(Colors.BLUE)  # Background color for settings menu
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
                        return game_over
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
            rotate_button = Button(image=None, pos=(screen_width * 0.5, screen_height * 0.4), text_input=f'ROTATE CW: {pygame.key.name(controls["rotate"]).upper()}', 
                                font=pygame.font.Font(FONT_PATH, 40), base_color="black", hovering_color="red")
            rotate_counter_button = Button(image=None, pos=(screen_width * 0.5, screen_height * 0.5), text_input=f'ROTATE CCW: {pygame.key.name(controls["rotate_ccw"]).upper()}', 
                                font=pygame.font.Font(FONT_PATH, 40), base_color="black", hovering_color="red")
            hard_button = Button(image=None, pos=(screen_width * 0.5, screen_height * 0.6), text_input=f'HARD DROP: {pygame.key.name(controls["hard_drop"]).upper()}', 
                                font=pygame.font.Font(FONT_PATH, 40), base_color="black", hovering_color="red")
            hold_button = Button(image=None, pos=(screen_width * 0.5, screen_height * 0.7), text_input=f'HOLD: {pygame.key.name(controls["hold"]).upper()}', 
                                font=pygame.font.Font(FONT_PATH, 40), base_color="black", hovering_color="red")
            default_button = Button(image=None, pos=(screen_width * 0.5, screen_height * 0.8), text_input=f'RETURN TO DEFAULT', 
                                font=pygame.font.Font(FONT_PATH, 35), base_color="black", hovering_color="red")
            back_button = Button(image=None, pos=(screen_width * 0.5, screen_height * 0.9), text_input='BACK', 
                                font=pygame.font.Font(FONT_PATH, 50), base_color="black", hovering_color="red")          
            return left_button, right_button, down_button, rotate_button, rotate_counter_button, hard_button, hold_button, default_button, back_button
        
        # Draw the initial buttons
        left_button, right_button, down_button, rotate_button, rotate_counter_button, hard_button, hold_button, default_button, back_button = draw_buttons()
        
        while True:
            screen.fill(Colors.BLUE)  # Background color for settings menu
            mouse_pos = pygame.mouse.get_pos()

            # Display buttons and update color if hovered
            for button in [left_button, right_button, down_button, rotate_button, rotate_counter_button, hard_button, hold_button, default_button, back_button]:
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
                    if rotate_counter_button.checkForInput(mouse_pos):
                        self.remap_control(screen, 'rotate_ccw', controls, screen_height, screen_width)
                        button_remapped = True   
                    if hard_button.checkForInput(mouse_pos):
                        self.remap_control(screen, 'hard_drop', controls, screen_height, screen_width)
                        button_remapped = True          
                    if hold_button.checkForInput(mouse_pos):
                        self.remap_control(screen, 'hold', controls, screen_height, screen_width)
                        button_remapped = True        
                    if default_button.checkForInput(mouse_pos):
                        controls.update(default_controls)
                        button_remapped = True
                        print("Returned settings to default!")
                    if back_button.checkForInput(mouse_pos):
                        return 

            if button_remapped:
                left_button, right_button, down_button, rotate_button, rotate_counter_button, hard_button, hold_button, default_button, back_button = draw_buttons()
                
            pygame.display.update()  # Ensure the display updates each frame
    
    def remap_control(self, screen, key_name, controls, screen_height, screen_width):
        prompt_font = pygame.font.Font(None, 40)
        prompt_text = f'PRESS NEW KEY FOR {key_name.upper()}'
        prompt_surface = prompt_font.render(prompt_text, True, Colors.BLACK)

        screen.fill((Colors.BLUE))  # Fill screen with dark background
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
            screen.fill(Colors.BLUE)
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
            speed_rect = speed_surface.get_rect(center=(screen_width*0.5, screen_height*0.1))
            move_rect = move_surface.get_rect(center=(screen_width*0.5, screen_height*0.3))
            screen.blit(speed_surface, speed_rect)
            screen.blit(move_surface, move_rect)
            pygame.display.update() 
        
        
        
