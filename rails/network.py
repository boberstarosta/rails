import settings
from rails import graphics
from rails.container import Container, Element
from rails.graph import Graph
from rails.vec import Vec


class TrackNode(Element):
    def __init__(self, position, id=None):
        super().__init__(id=id)
        self._position = Vec(position)

    @property
    def position(self):
        return self._position

    def serialize(self):
        return {"id": self.id, "position": self.position}

    @classmethod
    def deserialize(cls, data):
        return cls(data["position"], id=data["id"])


class Network:
    def __init__(self):
        self.track_nodes = Container()
        self.tracks_graph = Graph(directed=False, loops_allowed=False)

    def next_track_node(self, source, pivot):
        try:
            return next(n for n in self.tracks_graph.adjacent(pivot) if n is not source)
        except StopIteration:
            return None

    def nearest_track_node(self, point):
        point = Vec(point)
        search_radius_sq = settings.NODE_SEARCH_RADIUS**2
        nearest = None
        min_dist_sq = float("inf")
        for node in self.track_nodes.values():
            dist_sq = (node.position - point).length_sq
            if dist_sq < search_radius_sq and dist_sq < min_dist_sq:
                min_dist_sq = dist_sq
                nearest = node
        return nearest

    def clear(self):
        graphics.track_renderer.clear()
        self.track_nodes = Container()
        self.tracks_graph = Graph(directed=False, loops_allowed=False)

    def serialize(self):
        nodes = [node.serialize() for node in self.track_nodes.values()]
        edges = [
            (node_id, adjacent_node.id)
            for node_id, node in self.track_nodes.items()
            for adjacent_node in self.tracks_graph.adjacent(node)
        ]
        return {"nodes": nodes, "edges": edges}

    def load(self, data):
        self.clear()

        for node_data in data["nodes"]:
            node = TrackNode.deserialize(node_data)
            self.track_nodes.add(node)
            self.tracks_graph.add_node(node)
            graphics.track_renderer.add_node(node)

        for node1_id, node2_id in data["edges"]:
            node1 = self.track_nodes[node1_id]
            node2 = self.track_nodes[node2_id]
            self.tracks_graph.add_edge(node1, node2)
            graphics.track_renderer.add_edge(node1, node2)
