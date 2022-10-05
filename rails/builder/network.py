from typing import Dict, Iterable, Tuple, Union
import settings
import pyglet
from rails import graphics
from rails.container import Container, Element
from rails.graph import Graph
from rails.vec import Vec


class Node(Element):
    def __init__(self, position, id=None, container=None):
        super().__init__(id=id, container=container)
        self._position = Vec(position)

    @property
    def position(self):
        return self._position

    def serialize(self):
        return {"id": self.id, "position": self.position}

    @classmethod
    def deserialize(cls, data):
        return cls(data["position"], id=data["id"])

    def __str__(self):
        return f"{self.__class__.__name__}(position={self.position})"


class Network(pyglet.event.EventDispatcher):
    MAX_NODE_CONNECTIONS = settings.MAX_TRACK_NODE_CONNECTIONS
    MIN_EDGE_LENGTH = settings.MIN_TRACK_LENGTH

    def __init__(self) -> None:
        self.nodes = Container()
        self.graph = Graph(directed=False, loops_allowed=False)

    def next_node(self, source: Node, pivot: Node) -> Union[Node, None]:
        try:
            return next(n for n in self.graph.adjacent(pivot) if n is not source)
        except StopIteration:
            return None

    def nearest_node(self, point: Vec, *exclude: Iterable[Node]) -> Union(Node, None):
        point = Vec(point)
        search_radius_sq = settings.NODE_SEARCH_RADIUS**2
        nearest = None
        min_dist_sq = float("inf")
        for node in self.nodes.values():
            dist_sq = (node.position - point).length_sq
            if dist_sq < search_radius_sq and dist_sq < min_dist_sq and node not in exclude:
                min_dist_sq = dist_sq
                nearest = node
        return nearest

    def create_node(self, point: Vec) -> Node:
        new_node = Node(point, container=self.nodes)
        self.graph.add_node(new_node)
        self.dispatch_event("on_node_created", new_node)
        return new_node
    
    def can_create_edge(self, source: Union[Vec, Node], target: Union[Vec, Node]) -> bool:
        for node in (node for node in (source, target) if node in self.nodes):
            if node in self.nodes:
                if len(self.graph.adjacent(node)) >= self.MAX_NODE_CONNECTIONS:
                    return False

        source_pos = source.position if source in self.nodes else source
        target_pos = target.position if target in self.nodes else target
        if (target_pos - source_pos).length <= self.MIN_EDGE_LENGTH:
            return False

        return True

    def create_edge(self, source: Union[Vec, Node], target: Union[Vec, Node]) -> Tuple[Node, Node]:
        source_node = source if source in self.nodes else self.create_node(source)
        target_node = target if target in self.nodes else self.create_node(target)
        self.graph.add_edge(source_node, target_node)
        self.dispatch_event("on_edge_created", source_node, target_node)
        return (source_node, target_node)

    def clear(self) -> None:
        graphics.track_renderer.clear()
        self.nodes = Container()
        self.graph = Graph(directed=False, loops_allowed=False)
        self.dispatch_event("on_cleared")

    def serialize(self) -> Dict:
        nodes = [node.serialize() for node in self.nodes.values()]
        edges = [
            (node_id, adjacent_node.id)
            for node_id, node in self.nodes.items()
            for adjacent_node in self.graph.adjacent(node)
        ]
        return {"nodes": nodes, "edges": edges}

    def load(self, data: Dict) -> None:
        self.clear()

        for node_data in data["nodes"]:
            node = Node.deserialize(node_data)
            self.nodes.add(node)
            self.graph.add_node(node)
            graphics.track_renderer.add_node(node)

        for node1_id, node2_id in data["edges"]:
            node1 = self.nodes[node1_id]
            node2 = self.nodes[node2_id]
            self.graph.add_edge(node1, node2)
            graphics.track_renderer.add_edge(node1, node2)
        
        self.dispatch_event("on_loaded")


Network.register_event_type("on_node_created")
Network.register_event_type("on_edge_created")
Network.register_event_type("on_cleared")
Network.register_event_type("on_loaded")
