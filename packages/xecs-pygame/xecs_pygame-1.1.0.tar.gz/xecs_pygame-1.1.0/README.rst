xecs-pygame
===========

A plugin for xecs_, allowing you to render your entities with pygame_.

Usage
-----

First, add the plugin to your xecs_ app.

.. code-block:: python

  import xecs as xx
  from xecs_pygame import PyGamePlugin

  def main() -> None:
      app = xx.RealTimeApp()
      app.add_plugin(PyGamePlugin())


Now, when you spawn entities, you can give them a
``Circle``, ``Polygon``, ``Rectangle`` component. If you do that,
your entities will be rendered on the screen:


.. code-block:: python

  import xecs as xx
  from xecs_pygame import Circle, PyGamePlugin

  def spawn_three_circles(commands: xx.Commands, world: xx.World) -> None:
      transformi, _ = commands.spawn((xx.Transform2, Circle), 3)
      transform = world.get_view(xx.Transform2, transformi)
      transform.translation.x.fill([0, 15, 30])

  def main() -> None:
      app = xx.RealTimeApp()
      app.add_plugin(PyGamePlugin())
      app.add_startup_system(spawn_three_circles)
      app.add_pool(Circle.create_pool(3))
      app.add_pool(xx.Transform2.create_pool(3))
      app.run()

  if __name__ == "__main__":
      main()


Further examples
----------------

* `draw shapes`_
* `moving circles`_
* `boids`_
* `mouse presses`_

.. _xecs: https://github.com/lukasturcani/xecs
.. _pygame: https://github.com/pygame/pygame
.. _`draw shapes`: https://github.com/lukasturcani/xecs-pygame/blob/master/examples/draw_shapes.py
.. _`moving circles`: https://github.com/lukasturcani/xecs/blob/master/examples/moving_circles/moving_circles.py
.. _boids: https://github.com/lukasturcani/xecs/blob/master/examples/boids/boids.py
.. _`mouse presses`: https://github.com/lukasturcani/xecs/blob/master/examples/mouse_presses/mouse_presses.py


Installation
------------

.. code-block:: bash

  pip install xecs-pygame
