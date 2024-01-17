from typing import Union, Tuple, Optional, Dict

import pygame
import functools

Point: "TypeAlias" = Tuple[int, int]
Color: "TypeAlias" = pygame.Color

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
    "components": {"button": {"width": 120, "height": 40}},
}

mouse_pos = (0, 0)
_was_mouse_down = False
is_mouse_down = False

# id: pygame.Rect
_interactive_rects: Dict[str, pygame.Rect] = {}

# For every interaction (e.g. button click) we want to repaint at least once
_interactions = 0


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


def _remove_id_portion(text: str):
    parts = text.split("####", maxsplit=1)
    return parts[0]


def label(
    screen: pygame.Surface,
    text: str,
    color_path: str,
    size_path: str,
    top_left: Optional[Point] = None,
    center: Optional[Point] = None,
):
    textsurf = _text_surface(
        _remove_id_portion(text), theme_value(color_path), theme_value(size_path)
    )
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
    width: Optional[int] = None,
    height: Optional[int] = None,
):
    global _interactive_rects
    global _interactions

    if width is None:
        width = theme_value("components.button.width")
    if height is None:
        height = theme_value("components.button.height")

    rect = pygame.Rect(0, 0, width, height)

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

    _interactive_rects[text] = rect

    res = colliding and not is_mouse_down and _was_mouse_down

    if res:
        _interactions += 1

    return res


def start_frame():
    global _interactive_rects

    _interactive_rects.clear()


def _should_repaint():
    return (
        _interactions > 0
        or not _interactive_rects
        or any(rect.collidepoint(*mouse_pos) for rect in _interactive_rects.values())
    )


def wait_or_poll():
    global mouse_pos
    global is_mouse_down
    global _interactions

    while True:
        if _interactions > 0:
            event = pygame.event.poll()
        else:
            event = pygame.event.wait()

        if event.type == pygame.MOUSEMOTION:
            mouse_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONDOWN:
            is_mouse_down = True
        elif event.type == pygame.MOUSEBUTTONUP:
            is_mouse_down = False
            _interactions += 1

        if event.type != pygame.QUIT and not _should_repaint():
            continue

        if _interactions > 0:
            _interactions -= 1

        break

    return event


def end_frame():
    global _was_mouse_down
    global is_mouse_down

    _was_mouse_down = is_mouse_down
