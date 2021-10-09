import itertools
import pyglet
import rail.tracks as tracks
import rail.vehicles as vehicles
from rail.geometry import Vector


_layer_counter = itertools.count()

layers = {
    "track_segments": pyglet.graphics.OrderedGroup(next(_layer_counter)),
    "track_nodes": pyglet.graphics.OrderedGroup(next(_layer_counter)),
    "vehicles": pyglet.graphics.OrderedGroup(next(_layer_counter)),
    "debug": pyglet.graphics.OrderedGroup(next(_layer_counter)),
}


class Renderer:
    def __init__(self, track_manager, vehicle_manager):
        self._track_manager = track_manager
        self._batch = pyglet.graphics.Batch()
        tracks.Node.on_create.append(self.on_track_node_created)
        track_manager.on_track_created.append(self.on_track_created)
        track_manager.on_cleared.append(self.on_tracks_cleared)
        vehicles.Vehicle.on_create.append(self.on_vehicle_created)
        vehicles.Vehicle.on_move.append(self.on_vehicle_moved)
        self._shapes = {}
    
    def on_track_node_created(self, node):
        self._shapes[node] = pyglet.shapes.Circle(
            node.position.x,
            node.position.y,
            3,
            color=(0, 128, 0),
            batch=self._batch,
            group=layers["track_nodes"]
        )
    
    def on_track_node_moved(self, node):
        shape = self._shapes.get(node)
        shape.position = node.position
    
    def on_track_created(self, node1, node2):
        self._shapes[node1, node2] = pyglet.shapes.Line(
            node1.position.x,
            node1.position.y,
            node2.position.x,
            node2.position.y,
            width=5,
            color=(96, 64, 0),
            batch=self._batch,
            group=layers["track_segments"]
        )

    def on_tracks_cleared(self):
        for shape in self._shapes.values():
            shape.delete()
        self._shapes.clear()

    def on_vehicle_created(self, vehicle):
        rectangle = pyglet.shapes.Rectangle(
            vehicle.position.x,
            vehicle.position.y,
            11,
            19,
            color=(0, 0, 255),
            batch=self._batch,
            group=layers["vehicles"]
        )
        rectangle.anchor_x = rectangle.width/2
        rectangle.anchor_y = rectangle.height/2
        rectangle.rotation = vehicle.direction.angle(Vector(0, 1))

        node1 = pyglet.shapes.Circle(
            vehicle.node1.position.x,
            vehicle.node1.position.y,
            3,
            color=(128, 128, 128),
            batch=self._batch,
            group=layers["debug"]
        )

        node2 = pyglet.shapes.Circle(
            vehicle.node2.position.x,
            vehicle.node2.position.y,
            3,
            color=(255, 255, 255),
            batch=self._batch,
            group=layers["debug"]
        )

        point = pyglet.shapes.Circle(
            vehicle.position.x,
            vehicle.position.y,
            1,
            color=(0, 255, 0),
            batch=self._batch,
            group=layers["debug"]
        )

        arrow_position = vehicle.position + vehicle.direction*20
        arrow = pyglet.shapes.Circle(
            arrow_position.x,
            arrow_position.y,
            3,
            color=(255, 0, 0),
            batch=self._batch,
            group=layers["debug"]
        )

        self._shapes[vehicle] = rectangle, node1, node2, point, arrow

    def on_vehicle_moved(self, vehicle):
        rectangle, node1, node2, point, arrow = self._shapes[vehicle]
        rectangle.position = vehicle.position
        rectangle.rotation = vehicle.direction.angle(Vector(0, 1))
        node1.position = vehicle.node1.position
        node2.position = vehicle.node2.position
        point.position = vehicle.position
        arrow.position = vehicle.position + vehicle.direction*20

    def draw(self):
        self._batch.draw()
