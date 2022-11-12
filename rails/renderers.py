import pyglet
from rails import graphics


class NetworkRenderer:
    node_radius = 5
    node_color = (200, 200, 200)
    node_segments = 20
    node_group = None
    edge_width = 3
    edge_color = (160, 160, 160)
    edge_group = None

    def __init__(self) -> None:
        self._entities = {}

    def add_node(self, node: "Node") -> None:
        self._entities[node] = pyglet.shapes.Circle(
            *node.position, self.node_radius, self.node_segments,
            color=self.node_color,
            batch=graphics.batch,
            group=self.node_group
        )

    def add_edge(self, source: "Node", target: "Node"):
        self._entities[source, target] = pyglet.shapes.Line(
            *source.position, *target.position,
            width=self.edge_width,
            color=self.edge_color,
            batch=graphics.batch,
            group=self.edge_group
        )

    def clear(self):
        while self._entities:
            self._entities.popitem()[1].delete()


class TrackRenderer(NetworkRenderer):
    node_radius = 5
    node_color = (200, 160, 0)
    node_group = graphics.groups.TRACK_NODES
    edge_width = 3
    edge_color = (180, 140, 0)
    edge_group = graphics.groups.TRACK_EDGES


class TrainRenderer:
    def __init__(self):
        self.sprites = {}

    def add_car(self, car):
        self.sprites[car] = pyglet.sprite.Sprite(
            graphics.images["arrow red.png"],
            batch=graphics.batch,
            group=graphics.groups.TRAINS
        )
        self.update_car(car)

    def update_car(self, car):
        self.sprites[car].update(
            *car.location.position,
            rotation = -car.rotation
        )

    def clear(self):
        while self.sprites:
            self.sprites.popitem()[1].delete()
