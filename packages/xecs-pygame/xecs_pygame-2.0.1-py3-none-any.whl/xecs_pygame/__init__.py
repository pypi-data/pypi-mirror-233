from collections.abc import Callable

import numpy as np
import pygame
import xecs as xx


class PyGamePlugin(xx.RealTimeAppPlugin):
    def __init__(self, window_size: tuple[int, int] = (640, 640)) -> None:
        super().__init__()
        self._window_size = window_size

    def build(self, app: xx.RealTimeApp) -> None:
        pygame.init()
        app.add_resource(
            Display(pygame.display.set_mode(self._window_size), "black", [])
        )
        app.add_system(draw)
        app.add_system(process_events)
        app.add_system(update_mouse)
        app.add_system(update_keyboard)
        app.add_pool(Circle.create_pool(0))
        app.add_pool(Rectangle.create_pool(0))
        app.add_pool(Polygon.create_pool(0))
        app.add_pool(xx.Transform2.create_pool(0))
        app.add_pool(Text.create_pool(0))


class Display(xx.Resource):
    surface: pygame.Surface
    color: str
    hooks: list[Callable[[], None]]


class Circle(xx.Component):
    radius: xx.Float = xx.float_(default=5.0)
    color: xx.PyField[str] = xx.py_field(default="purple")
    width: xx.Int = xx.int_(default=0)


class Rectangle(xx.Component):
    length_x: xx.Float = xx.float_(default=10.0)
    length_y: xx.Float = xx.float_(default=10.0)
    color: xx.PyField[str] = xx.py_field(default="purple")
    width: xx.Int = xx.int_(default=0)


class TextError(Exception):
    pass


class Text(xx.Component):
    font: xx.PyField[pygame.font.Font | None] = xx.py_field(default=None)
    text: xx.PyField[str] = xx.py_field(default="")
    color: xx.PyField[str] = xx.py_field(default="purple")


def _get_star() -> list[tuple[float, float]]:
    outer_xs = np.cos(np.linspace(0, 2 * np.pi, 5, endpoint=False)) * 10
    outer_ys = np.sin(np.linspace(0, 2 * np.pi, 5, endpoint=False)) * 10
    inner_xs = (
        np.cos(np.linspace(0, 2 * np.pi, 5, endpoint=False) + 0.3 * np.pi) * 5
    )
    inner_ys = (
        np.sin(np.linspace(0, 2 * np.pi, 5, endpoint=False) + 0.3 * np.pi) * 5
    )

    coordinates = []
    for i in range(5):
        coordinates.append((outer_xs[i], outer_ys[i]))
        coordinates.append((inner_xs[i], inner_ys[i]))

    return coordinates


class Polygon(xx.Component):
    vertices: xx.PyField[list[tuple[float, float]]] = xx.py_field(
        default=_get_star(),
    )
    color: xx.PyField[str] = xx.py_field(default="purple")


def draw(
    display: Display,
    polygon_query: xx.Query[tuple[xx.Transform2, Polygon]],
    rectangle_query: xx.Query[tuple[xx.Transform2, Rectangle]],
    circle_query: xx.Query[tuple[xx.Transform2, Circle]],
    text_query: xx.Query[tuple[xx.Transform2, Text]],
) -> None:
    (transform, polygon) = polygon_query.result()
    display.surface.fill(display.color)
    display_origin = np.array(display.surface.get_size()) / 2
    for i in range(len(transform)):
        x = transform.translation.x.get(i)
        y = transform.translation.y.get(i)
        angle = transform.rotation.get(i)
        r = [
            [np.cos(angle), -np.sin(angle)],
            [np.sin(angle), np.cos(angle)],
        ]
        vertices = np.array(polygon.vertices.get(i)).T
        drawn_polygon = [x, y] + display_origin + (r @ vertices).T
        pygame.draw.polygon(
            display.surface,
            polygon.color.get(i),
            drawn_polygon.tolist(),
        )

    (transform, rectangle) = rectangle_query.result()
    for i in range(len(transform)):
        x = transform.translation.x.get(i)
        y = transform.translation.y.get(i)
        pygame.draw.rect(
            display.surface,
            rectangle.color.get(i),
            pygame.Rect(
                x + display_origin[0],
                y + display_origin[1],
                rectangle.length_x.get(i),
                rectangle.length_y.get(i),
            ),
            rectangle.width.get(i),
        )

    (transform, circle) = circle_query.result()
    for i in range(len(transform)):
        x = transform.translation.x.get(i) + display_origin[0]
        y = transform.translation.y.get(i) + display_origin[1]
        pygame.draw.circle(
            display.surface,
            circle.color.get(i),
            (x, y),
            circle.radius.get(i),
            width=circle.width.get(i),
        )

    (transform, text) = text_query.result()
    for i in range(len(transform)):
        font = text.font.get(i)
        if font is None:
            raise TextError("uninitialized font")
        text_surface = pygame.transform.flip(
            font.render(text.text.get(i), True, text.color.get(i)), False, True
        )
        x = transform.translation.x.get(i) + display_origin[0]
        y = transform.translation.y.get(i) + display_origin[1]
        display.surface.blit(text_surface, (x, y))

    display.surface.blit(
        pygame.transform.flip(display.surface, False, True),
        dest=(0, 0),
    )

    for hook in display.hooks:
        hook()
    pygame.display.flip()


def process_events() -> None:
    pygame.event.get()


def update_mouse(mouse: xx.Mouse) -> None:
    for number, pressed in enumerate(
        pygame.mouse.get_pressed(num_buttons=5), 1
    ):
        button = xx.MouseButton(number)
        if pressed:
            mouse.pressed.add(button)
        else:
            mouse.pressed.discard(button)

    mouse.position = pygame.mouse.get_pos()


KEY_MAP = (
    (xx.KeyboardButton.KEY_0, pygame.K_0),
    (xx.KeyboardButton.KEY_1, pygame.K_1),
    (xx.KeyboardButton.KEY_2, pygame.K_2),
    (xx.KeyboardButton.KEY_3, pygame.K_3),
    (xx.KeyboardButton.KEY_4, pygame.K_4),
    (xx.KeyboardButton.KEY_5, pygame.K_5),
    (xx.KeyboardButton.KEY_6, pygame.K_6),
    (xx.KeyboardButton.KEY_7, pygame.K_7),
    (xx.KeyboardButton.KEY_8, pygame.K_8),
    (xx.KeyboardButton.KEY_9, pygame.K_9),
    (xx.KeyboardButton.A, pygame.K_a),
    (xx.KeyboardButton.B, pygame.K_b),
    (xx.KeyboardButton.C, pygame.K_c),
    (xx.KeyboardButton.D, pygame.K_d),
    (xx.KeyboardButton.E, pygame.K_e),
    (xx.KeyboardButton.F, pygame.K_f),
    (xx.KeyboardButton.G, pygame.K_g),
    (xx.KeyboardButton.H, pygame.K_h),
    (xx.KeyboardButton.I, pygame.K_i),
    (xx.KeyboardButton.J, pygame.K_j),
    (xx.KeyboardButton.K, pygame.K_k),
    (xx.KeyboardButton.L, pygame.K_l),
    (xx.KeyboardButton.M, pygame.K_m),
    (xx.KeyboardButton.N, pygame.K_n),
    (xx.KeyboardButton.O, pygame.K_o),
    (xx.KeyboardButton.P, pygame.K_p),
    (xx.KeyboardButton.Q, pygame.K_q),
    (xx.KeyboardButton.R, pygame.K_r),
    (xx.KeyboardButton.S, pygame.K_s),
    (xx.KeyboardButton.T, pygame.K_t),
    (xx.KeyboardButton.U, pygame.K_u),
    (xx.KeyboardButton.V, pygame.K_v),
    (xx.KeyboardButton.W, pygame.K_w),
    (xx.KeyboardButton.X, pygame.K_x),
    (xx.KeyboardButton.Y, pygame.K_y),
    (xx.KeyboardButton.Z, pygame.K_z),
    (xx.KeyboardButton.ESCAPE, pygame.K_ESCAPE),
    (xx.KeyboardButton.F1, pygame.K_F1),
    (xx.KeyboardButton.F2, pygame.K_F2),
    (xx.KeyboardButton.F3, pygame.K_F3),
    (xx.KeyboardButton.F4, pygame.K_F4),
    (xx.KeyboardButton.F5, pygame.K_F5),
    (xx.KeyboardButton.F6, pygame.K_F6),
    (xx.KeyboardButton.F7, pygame.K_F7),
    (xx.KeyboardButton.F8, pygame.K_F8),
    (xx.KeyboardButton.F9, pygame.K_F9),
    (xx.KeyboardButton.F10, pygame.K_F10),
    (xx.KeyboardButton.F11, pygame.K_F11),
    (xx.KeyboardButton.F12, pygame.K_F12),
    (xx.KeyboardButton.F13, pygame.K_F13),
    (xx.KeyboardButton.F14, pygame.K_F14),
    (xx.KeyboardButton.F15, pygame.K_F15),
    (xx.KeyboardButton.SNAPSHOT, pygame.K_PRINT),
    (xx.KeyboardButton.SCROLL, pygame.K_SCROLLLOCK),
    (xx.KeyboardButton.PAUSE, pygame.K_PAUSE),
    (xx.KeyboardButton.INSERT, pygame.K_INSERT),
    (xx.KeyboardButton.HOME, pygame.K_HOME),
    (xx.KeyboardButton.DELETE, pygame.K_DELETE),
    (xx.KeyboardButton.END, pygame.K_END),
    (xx.KeyboardButton.PAGE_DOWN, pygame.K_PAGEDOWN),
    (xx.KeyboardButton.PAGE_UP, pygame.K_PAGEUP),
    (xx.KeyboardButton.LEFT, pygame.K_LEFT),
    (xx.KeyboardButton.UP, pygame.K_UP),
    (xx.KeyboardButton.RIGHT, pygame.K_RIGHT),
    (xx.KeyboardButton.DOWN, pygame.K_DOWN),
    (xx.KeyboardButton.BACK, pygame.K_BACKSPACE),
    (xx.KeyboardButton.RETURN, pygame.K_RETURN),
    (xx.KeyboardButton.SPACE, pygame.K_SPACE),
    (xx.KeyboardButton.CARET, pygame.K_CARET),
    (xx.KeyboardButton.NUM_LOCK, pygame.K_NUMLOCK),
    (xx.KeyboardButton.NUMPAD_0, pygame.K_KP0),
    (xx.KeyboardButton.NUMPAD_1, pygame.K_KP1),
    (xx.KeyboardButton.NUMPAD_2, pygame.K_KP2),
    (xx.KeyboardButton.NUMPAD_3, pygame.K_KP3),
    (xx.KeyboardButton.NUMPAD_4, pygame.K_KP4),
    (xx.KeyboardButton.NUMPAD_5, pygame.K_KP5),
    (xx.KeyboardButton.NUMPAD_6, pygame.K_KP6),
    (xx.KeyboardButton.NUMPAD_7, pygame.K_KP7),
    (xx.KeyboardButton.NUMPAD_8, pygame.K_KP8),
    (xx.KeyboardButton.NUMPAD_9, pygame.K_KP9),
    (xx.KeyboardButton.NUMPAD_ADD, pygame.K_KP_PLUS),
    (xx.KeyboardButton.APOSTROPHE, pygame.K_QUOTE),
    (xx.KeyboardButton.ASTERISK, pygame.K_ASTERISK),
    (xx.KeyboardButton.PLUS, pygame.K_PLUS),
    (xx.KeyboardButton.AT, pygame.K_AT),
    (xx.KeyboardButton.BACKSLASH, pygame.K_BACKSLASH),
    (xx.KeyboardButton.CAPITAL, pygame.K_CAPSLOCK),
    (xx.KeyboardButton.COLON, pygame.K_COLON),
    (xx.KeyboardButton.COMMA, pygame.K_COMMA),
    (xx.KeyboardButton.NUMPAD_DECIMAL, pygame.K_KP_PERIOD),
    (xx.KeyboardButton.NUMPAD_DIVIDE, pygame.K_KP_DIVIDE),
    (xx.KeyboardButton.EQUALS, pygame.K_EQUALS),
    (xx.KeyboardButton.GRAVE, pygame.K_BACKQUOTE),
    (xx.KeyboardButton.ALT_LEFT, pygame.K_LALT),
    (xx.KeyboardButton.BRACKET_LEFT, pygame.K_LEFTBRACKET),
    (xx.KeyboardButton.CONTROL_LEFT, pygame.K_LCTRL),
    (xx.KeyboardButton.SHIFT_LEFT, pygame.K_LSHIFT),
    (xx.KeyboardButton.SUPER_LEFT, pygame.K_LMETA),
    (xx.KeyboardButton.MINUS, pygame.K_MINUS),
    (xx.KeyboardButton.NUMPAD_MULTIPLY, pygame.K_KP_MULTIPLY),
    (xx.KeyboardButton.NUMPAD_ENTER, pygame.K_KP_ENTER),
    (xx.KeyboardButton.NUMPAD_EQUALS, pygame.K_KP_EQUALS),
    (xx.KeyboardButton.PERIOD, pygame.K_PERIOD),
    (xx.KeyboardButton.POWER, pygame.K_POWER),
    (xx.KeyboardButton.ALT_RIGHT, pygame.K_RALT),
    (xx.KeyboardButton.BRACKET_RIGHT, pygame.K_RIGHTBRACKET),
    (xx.KeyboardButton.CONTROL_RIGHT, pygame.K_RCTRL),
    (xx.KeyboardButton.SHIFT_RIGHT, pygame.K_RSHIFT),
    (xx.KeyboardButton.SUPER_RIGHT, pygame.K_RMETA),
    (xx.KeyboardButton.SEMICOLON, pygame.K_SEMICOLON),
    (xx.KeyboardButton.SLASH, pygame.K_SLASH),
    (xx.KeyboardButton.NUMPAD_SUBTRACT, pygame.K_KP_MINUS),
    (xx.KeyboardButton.UNDERLINE, pygame.K_UNDERSCORE),
)


def update_keyboard(keyboard: xx.Keyboard) -> None:
    pressed = pygame.key.get_pressed()
    for button, key in KEY_MAP:
        if pressed[key]:
            keyboard.pressed.add(button)
        else:
            keyboard.pressed.discard(button)
