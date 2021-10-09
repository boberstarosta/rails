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

    def create_node(self, point):
        node = Node(point)
        self.graph.add_node(node)
        return node

    def extend_node(self, node1, point):
        node2 = Node(point)
        self.graph.add_edge(node1, node2)
        self.on_track_created(node1, node2)
        return node2

    def connect_nodes(self, node1, node2):
        self.graph.add_edge(node1, node2)
        self.on_track_created(node1, node2)
        return node1, node2

    def get_next_node(self, node_from, node_to):
        for node in self.graph.adjacent_nodes(node_to):
            if node is not node_from:
                print(f"Next node: {node}")
                return node

    def save(self, filename):
        data = {
            "tracks": {
                "nodes": [(id(n), n.position) for n in self.graph.nodes],
                "edges": [(id(n1), id(n2)) for (n1, n2) in self.graph.edges]
            }
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
        nodes = {}
        for n_id, n_pos in data["tracks"]["nodes"]:
            nodes[n_id] = self.create_node(n_pos)
        for n1_id, n2_id in data["tracks"]["edges"]:
            self.connect_nodes(nodes[n1_id], nodes[n2_id])

    def print(self):
        print("==== Tracks ====")
        print(f"Node count: {self.graph.node_count}")
        print(f"Edge count: {self.graph.edge_count}")
        for n1, n2 in self.graph.edges:
            print(n1, n2)
