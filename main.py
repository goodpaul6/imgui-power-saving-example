import pygame
import ui

pygame.init()
screen = pygame.display.set_mode((640, 360))

running = True

show_goodbye = False
frames_rendered = 0

while running:
    event = ui.wait_or_poll()

    if event.type == pygame.QUIT:
        running = False

    ui.start_frame()

    screen.fill("black")

    if ui.button(screen, "Hello", center=(100, 100)):
        show_goodbye = True

    if show_goodbye and ui.button(screen, "Goodbye", center=(300, 100)):
        show_goodbye = False

    frames_rendered += 1

    ui.label(
        screen,
        f"Frames Rendered: {frames_rendered}",
        "colors.common.white",
        "typography.body1.fontSize",
        top_left=(2, 2),
    )

    ui.end_frame()

    # flip() the display to put your work on screen
    pygame.display.flip()

pygame.quit()
