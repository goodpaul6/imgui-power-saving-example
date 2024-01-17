import pygame
import ui

pygame.init()
screen = pygame.display.set_mode((640, 360))

running = True

show_goodbye = False
frames_rendered = 0

while running:
    if ui.can_wait:
        event = pygame.event.wait()

        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEMOTION:
            ui.mouse_pos = event.pos

        if not ui.should_repaint():
            continue

    ui.is_mouse_down = any(pygame.mouse.get_pressed())

    ui.start_frame()

    screen.fill("black")

    if ui.button(screen, "Hello", center=(100, 100)):
        print("Hello")
        show_goodbye = True

    if show_goodbye and ui.button(screen, "Goodbye", center=(300, 100)):
        print("Goodbye")
        show_goodbye = False

    frames_rendered += 1

    frames_surf = ui._text_surface(f"Frames Rendered: {frames_rendered}", "white", 24)
    screen.blit(frames_surf, (2, 2))

    ui.end_frame()

    # flip() the display to put your work on screen
    pygame.display.flip()

pygame.quit()
