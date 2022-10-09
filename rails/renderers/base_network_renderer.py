import pyglet
import settings
from rails import graphics


class BaseNetworkRenderer:
    node_radius = settings.NODE_RADIUS
    node_color = None
    node_group = None
    edge_width = settings.EDGE_WIDTH
    edge_color = None
    edge_group = None

    def __init__(self):
        self.sprites = {}

    def on_node_added(self, node):
        self.sprites[node] = pyglet.shapes.Circle(
            *node.position, self.node_radius, 20,
            color=self.node_color,
            batch=graphics.batch,
            group=self.node_group
        )

    def on_edge_added(self, source, target):
        self.sprites[source, target] = pyglet.shapes.Line(
            *source.position, *target.position,
            width=self.edge_width,
            color=self.edge_color,
            batch=graphics.batch,
            group=self.edge_group
        )

    def on_cleared(self):
        while self.sprites:
            self.sprites.popitem()[1].delete()
