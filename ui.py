from typing import Union, Tuple, Optional, Any

import pygame
import functools

Point: "TypeAlias" = Tuple[int, int]
Color: "TypeAlias" = pygame.Color

BUTTON_W = 120
BUTTON_H = 60

theme = {
    "colors": {
        "common": {
            "black": "black",
            "white": "white",
        },
        "primary": {
            "main": "antiquewhite2",
            "light": "antiquewhite1",
            "dark": "antiquewhite3",
        },
    },
    "typography": {
        "body1": {
            "fontSize": 24,
        }
    },
}

mouse_pos = (0, 0)
was_mouse_down = False
is_mouse_down = False

# id: pygame.Rect
interactive_rects = {}

# When an interaction occurs, we make sure to not wait for an event
# before repainting so the interaction feels instant
can_wait = True


def theme_value(path: str) -> Union[str, int]:
    value = theme

    try:
        for part in path.split("."):
            value = value[part]
    except KeyError:
        print(path)
        raise

    return value


@functools.lru_cache(maxsize=16)
def _text_surface(text: str, color: str, font_size: int) -> pygame.Surface:
    font = pygame.font.SysFont("calibri", font_size)
    return font.render(text, False, color).convert()


def label(
    screen: pygame.Surface,
    text: str,
    color_path: str,
    size_path: int,
    top_left: Optional[Point] = None,
    center: Optional[Point] = None,
):
    textsurf = _text_surface(text, theme_value(color_path), theme_value(size_path))
    textsurf_rect = (
        textsurf.get_rect(topleft=top_left)
        if top_left
        else textsurf.get_rect(center=center)
    )

    screen.blit(textsurf, textsurf_rect)


def button(
    screen: pygame.Surface,
    text: str,
    top_left: Optional[Point] = None,
    center: Optional[Point] = None,
):
    rect = pygame.Rect(0, 0, BUTTON_W, BUTTON_H)

    if center:
        rect.center = center
    if top_left:
        rect.top_left = top_left

    colliding = rect.collidepoint(*mouse_pos)
    pressed = colliding and is_mouse_down

    if not colliding:
        col = "colors.primary.main"
    elif not pressed:
        col = "colors.primary.light"
    else:
        col = "colors.primary.dark"

    pygame.draw.rect(screen, theme_value(col), rect)

    label(
        screen,
        text,
        "colors.common.black",
        "typography.body1.fontSize",
        center=rect.center,
    )

    interactive_rects[text] = rect.inflate(2, 2)

    res = colliding and not is_mouse_down and was_mouse_down

    if res:
        global can_wait
        can_wait = False

    return res


def start_frame():
    global can_wait
    global interactive_rects

    interactive_rects.clear()
    can_wait = True


def should_repaint():
    return not interactive_rects or any(
        rect.collidepoint(*mouse_pos) for rect in interactive_rects.values()
    )


def end_frame():
    global was_mouse_down
    global is_mouse_down

    was_mouse_down = is_mouse_down
    is_mouse_down = False
