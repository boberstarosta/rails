from rail.geometry import Vector
from rail.graph import Graph


class Node:
    def __init__(self, position):
        self._position = Vector(position)

    @property
    def position(self):
        return self._position


class TrackManager:
    def __init__(self):
        self.graph = Graph()
    
    def add_track(self, start, end):
        node1 = Node(start)
        node2 = Node(end)
        self.graph.add_edge(node1, node2)
