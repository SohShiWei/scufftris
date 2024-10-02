from settings import *

def show_settings_menu(sc, controls):
    sc.fill((50, 50, 50))  # Background color for settings menu
    settings_font = pygame.font.Font(None, 50)

    options = ['Left', 'Right', 'Down', 'Rotate']
    instructions = 'Remap using ARROW keys'
    esc = 'ESC to go back to MENU'
    
    # Render and display the instructions
    instructions_text = settings_font.render(instructions, True, pygame.Color('white'))
    sc.blit(instructions_text, (100, 50))  # Position above the control options
    
    esc_text = settings_font.render(esc, True, pygame.Color('white'))
    sc.blit(esc_text, (100, 90))  

    for i, option in enumerate(options):  # Render and display the control options
        text = settings_font.render(f'{option}: {pygame.key.name(controls[option.lower()])}', True, pygame.Color('white'))
        sc.blit(text, (100, 200 + i * 60))
    
    pygame.display.flip()

def remap_control(sc, key_name, controls):
    prompt_text = f'Press new key for {key_name}'
    prompt_font = pygame.font.Font(None, 50)
    prompt_surface = prompt_font.render(prompt_text, True, pygame.Color('white'))

    sc.fill((50, 50, 50))
    sc.blit(prompt_surface, (100, 100))
    pygame.display.flip()

    waiting_for_key = True
    while waiting_for_key:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                controls[key_name.lower()] = event.key
                waiting_for_key = False
                show_settings_menu(sc, controls)  # Refresh menu to show updated controls
                return
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

def handle_settings(sc, controls):
    show_settings_menu(sc, controls)
    
    settings_running = True
    while settings_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Press 'ESC' to exit settings
                    settings_running = False
                    return
                elif event.key == pygame.K_LEFT:
                    remap_control(sc, 'left', controls)
                elif event.key == pygame.K_RIGHT:
                    remap_control(sc, 'right', controls)
                elif event.key == pygame.K_DOWN:
                    remap_control(sc, 'down', controls)
                elif event.key == pygame.K_UP:
                    remap_control(sc, 'rotate', controls)