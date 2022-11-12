import pyglet
from rails import graphics
from rails.network import Network
from rails.vec import Vec


class Builder:
    def __init__(self, network: Network):
        self._network = network
        self._highlighted_node = None
        self._highlighted_node_sprite = pyglet.shapes.Circle(
            0, 0, 6,
            color=(0, 255, 0),
            batch=graphics.batch,
            group=graphics.groups.BUILDER_HIGHLIGHT
        )
        self._highlighted_node_sprite.visible = False

    def update_highlighted_node(self, point):
        self._highlighted_node = self._network.nearest_node(point)
        if self._highlighted_node is not None:
            self._highlighted_node_sprite.position = self._highlighted_node.position
            self._highlighted_node_sprite.visible = True
        else:
            self._highlighted_node_sprite.visible = False

    def on_mouse_motion(self, x, y, dx, dy):
        self.update_highlighted_node(Vec(x, y))

    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        pass

    def on_mouse_release(self, x, y, button, modifiers):
        pass
