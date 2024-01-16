import pygame
import functools

BUTTON_HOVER_COL = "antiquewhite1"
BUTTON_UP_COL = "antiquewhite2"
BUTTON_DOWN_COL = "antiquewhite3"
BUTTON_TEXT_COL = "black"
BUTTON_TEXT_SIZE = 24

BUTTON_W = 120
BUTTON_H = 60

pygame.init()
screen = pygame.display.set_mode((1280, 720))

running = True
mouse_x = 0
mouse_y = 0
was_mouse_down = False
is_mouse_down = False

# id: pygame.Rect
relevant_rects = {}

@functools.lru_cache(maxsize=16)
def text_surface(text, color, font_size):
    font = pygame.font.SysFont('calibri', font_size)
    return font.render(text, False, color)

def button(screen, x, y, text):
    rect = pygame.Rect(x, y, BUTTON_W, BUTTON_H)
    colliding = rect.collidepoint(mouse_x, mouse_y)
    pressed = colliding and is_mouse_down

    if not colliding:
        col = BUTTON_UP_COL
    elif not pressed:
        col = BUTTON_HOVER_COL
    else:
        col = BUTTON_DOWN_COL

    textsurf = text_surface(text, BUTTON_TEXT_COL, BUTTON_TEXT_SIZE)
    textsurf_rect = textsurf.get_rect(center=(x + BUTTON_W / 2, y + BUTTON_H / 2))

    pygame.draw.rect(screen, col, rect)

    screen.blit(textsurf, textsurf_rect)

    relevant_rects[text] = rect.inflate(2, 2)

    return colliding and not is_mouse_down and was_mouse_down
    

def end_frame():
    global was_mouse_down
    global is_mouse_down

    was_mouse_down = is_mouse_down
    is_mouse_down = False

show_goodbye = False

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    event = pygame.event.wait()

    is_mouse_down = any(pygame.mouse.get_pressed())

    if event.type == pygame.QUIT:
        running = False
    elif event.type == pygame.MOUSEMOTION:
        mouse_x, mouse_y = event.pos

    if relevant_rects and \
        not any(rect.collidepoint(mouse_x, mouse_y) for rect in relevant_rects.values()):
        continue
 
    screen.fill("black")

    relevant_rects.clear()

    if button(screen, 100, 100, "Hello"):
        print("Hello")
        show_goodbye = True

    if show_goodbye and button(screen, 300, 100, "Goodbye"):
        print("Goodbye")
        show_goodbye = False

    print("Rendered frame")
 
    end_frame()

    # flip() the display to put your work on screen
    pygame.display.flip()

pygame.quit()