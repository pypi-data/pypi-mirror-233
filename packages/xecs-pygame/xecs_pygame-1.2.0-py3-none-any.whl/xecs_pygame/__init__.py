from typing import Callable

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
        app.add_system(update_mouse)
        app.add_pool(Circle.create_pool(0))
        app.add_pool(Rectangle.create_pool(0))
        app.add_pool(Polygon.create_pool(0))
        app.add_pool(xx.Transform2.create_pool(0))


class Display(xx.Resource):
    surface: pygame.Surface
    color: str
    hooks: list[Callable[[], None]]


class Circle(xx.Component):
    radius: xx.PyField[float] = xx.py_field(default=5.0)
    color: xx.PyField[str] = xx.py_field(default="purple")
    width: xx.PyField[int] = xx.py_field(default=0)


class Rectangle(xx.Component):
    size: xx.PyField[tuple[float, float]] = xx.py_field(default=(10.0, 10.0))
    color: xx.PyField[str] = xx.py_field(default="purple")
    width: xx.PyField[int] = xx.py_field(default=0)


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
        (w, h) = rectangle.size.get(i)
        pygame.draw.rect(
            display.surface,
            rectangle.color.get(i),
            pygame.Rect(
                x + display_origin[0],
                y + display_origin[1],
                w,
                h,
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

    display.surface.blit(
        pygame.transform.flip(display.surface, False, True),
        dest=(0, 0),
    )

    for hook in display.hooks:
        hook()
    pygame.display.flip()


def update_mouse(mouse: xx.Mouse) -> None:
    pygame.event.get()
    for number, pressed in enumerate(
        pygame.mouse.get_pressed(num_buttons=5), 1
    ):
        button = xx.MouseButton(number)
        if pressed:
            mouse.pressed.add(button)
        else:
            mouse.pressed.discard(button)

    mouse.position = pygame.mouse.get_pos()
