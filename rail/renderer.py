import itertools
import pyglet
import rail.tracks as tracks


_layer_counter = itertools.count()

layers = {
    "track_segments": pyglet.graphics.OrderedGroup(next(_layer_counter)),
    "track_nodes": pyglet.graphics.OrderedGroup(next(_layer_counter)),
}


class Renderer:
    def __init__(self, track_manager):
        self._track_manager = track_manager
        self._batch = pyglet.graphics.Batch()
        tracks.Node.on_create.append(self.on_track_node_created)
        track_manager.on_track_created.append(self.on_track_created)
        track_manager.on_cleared.append(self.on_tracks_cleared)
        self._shapes = {}
    
    def on_track_node_created(self, node):
        self._shapes[node] = pyglet.shapes.Circle(
            node.position.x,
            node.position.y,
            9,
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

    def draw(self):
        self._batch.draw()
