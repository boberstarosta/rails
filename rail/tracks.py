from rail.event import Event
from rail.geometry import Vector
from rail.graph import Graph


class Node:
    on_create = Event()
    on_move = Event()

    def __init__(self, position):
        self._position = Vector(position)
        self.on_create.fire(self)

    @property
    def position(self):
        return self._position
    
    @position.setter
    def position(self, value):
        if value != self._position:
            self._position = Vector(value)
            self.on_move.fire(self)


class TrackManager:
    def __init__(self):
        self.graph = Graph(directed=False)
        self.on_track_created = Event()
    
    def add_track(self, start, end):
        node1 = Node(start)
        node2 = Node(end)
        self.graph.add_edge(node1, node2)
        self.on_track_created(node1, node2)
