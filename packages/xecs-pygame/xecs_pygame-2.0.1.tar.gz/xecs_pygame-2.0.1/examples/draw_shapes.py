import xecs as xx
from xecs_pygame import Circle, Polygon, PyGamePlugin, Rectangle


def spawn_objects(commands: xx.Commands, world: xx.World) -> None:
    polygon_transformi, _ = commands.spawn((xx.Transform2, Polygon), 3)
    polygon_transform = world.get_view(xx.Transform2, polygon_transformi)
    polygon_transform.translation.x.fill([0, 15, 30])
    polygon_transform.translation.y.fill(0)

    rectangle_transformi, _ = commands.spawn((xx.Transform2, Rectangle), 3)
    rectangle_transform = world.get_view(xx.Transform2, rectangle_transformi)
    rectangle_transform.translation.x.fill([0, 15, 30])
    rectangle_transform.translation.y.fill(15)

    circle_transformi, _ = commands.spawn((xx.Transform2, Circle), 3)
    circle_transform = world.get_view(xx.Transform2, circle_transformi)
    circle_transform.translation.x.fill([0, 15, 30])
    circle_transform.translation.y.fill(35)


def main() -> None:
    app = xx.RealTimeApp()
    app.add_plugin(PyGamePlugin())
    app.add_startup_system(spawn_objects)
    app.add_pool(xx.Transform2.create_pool(9))
    app.add_pool(Polygon.create_pool(3))
    app.add_pool(Rectangle.create_pool(3))
    app.add_pool(Circle.create_pool(3))
    app.run()


if __name__ == "__main__":
    main()
