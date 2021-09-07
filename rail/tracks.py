from rail import events
from rail.graph import Graph


class Node:
    def __init__(self, position):
        self._position = position

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        if value != self._position:
            self._position = value
            events.track_node_moved(self)


class TrackManager:
    def __init__(self):
        self.graph = Graph()
    
    def create_node(self, position):
        new_node = Node(position)
        self.graph.add_node(new_node)
        events.track_node_created(new_node)

    def connect_nodes(self, node1, node2):
        edge = self.graph.add_edge(node1, node2)
        events.track_nodes_connected(edge)
