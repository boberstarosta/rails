import json
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
    
    def __repr__(self):
        return f"{self.__class__.__name__}({self.position})"


class TrackManager:
    def __init__(self):
        self.graph = Graph()
        self.on_track_created = Event()
        self.on_cleared = Event()
    
    def add_track(self, start, end):
        node1 = Node(start)
        node2 = Node(end)
        self.graph.add_edge(node1, node2)
        self.on_track_created(node1, node2)
        return node1, node2

    def extend_node(self, node1, point):
        node2 = Node(point)
        self.graph.add_edge(node1, node2)
        self.on_track_created(node1, node2)
        return node2

    def save(self, filename):
        data = {
            "tracks": [(n1.position, n2.position) for (n1, n2) in self.graph.edges]
        }
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

    def load(self, filename):
        data = {}
        try:
            with open(filename, "r") as f:
                data = json.load(f)
        except IOError as ex:
            print(f"Error loading {filename}")
            return
        self.graph = Graph()
        self.on_cleared()
        for p1, p2 in data["tracks"]:
            self.add_track(p1, p2)
