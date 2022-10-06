import pyglet
import settings
from typing import Dict, Iterable, Tuple, Type, Union
from rails.container import Container, Element
from rails.graph import Graph
from rails.vec import Vec


class TrackNode(Element):
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


class TrackNetwork(pyglet.event.EventDispatcher):
    node_class: Type[TrackNode] = TrackNode

    def __init__(self) -> None:
        self.nodes = Container()
        self.graph = Graph(directed=False, loops_allowed=False)

    def next_node(self, source: TrackNode, pivot: TrackNode) -> Union[TrackNode, None]:
        try:
            return next(n for n in self.graph.adjacent(pivot) if n is not source)
        except StopIteration:
            return None

    def nearest_node(self, point: Vec, *exclude: Iterable[TrackNode]) -> Union[TrackNode, None]:
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

    def create_node(self, point: Vec) -> TrackNode:
        new_node = self.node_class(point, container=self.nodes)
        return self.add_node(new_node)
    
    def add_node(self, node: TrackNode) -> TrackNode:
        self.nodes.add(node)
        self.graph.add_node(node)
        self.dispatch_event("on_node_added", node)
        return node

    def delete_node(self, node: TrackNode) -> None:
        self.graph.remove_node(node)
        self.nodes.remove(element=node)
        self.dispatch_event("on_node_removed", node)

    def create_edge(self, source: Union[Vec, TrackNode], target: Union[Vec, TrackNode]) -> Tuple[TrackNode, TrackNode]:
        source_node = source if source in self.nodes else self.create_node(source)
        target_node = target if target in self.nodes else self.create_node(target)
        self.graph.add_edge(source_node, target_node)
        self.dispatch_event("on_edge_added", source_node, target_node)
        return (source_node, target_node)

    def clear(self) -> None:
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
            node = TrackNode.deserialize(node_data)
            self.add_node(node)

        for source_id, target_id in data["edges"]:
            source_node = self.nodes[source_id]
            target_node = self.nodes[target_id]
            self.create_edge(source_node, target_node)


TrackNetwork.register_event_type("on_node_added")
TrackNetwork.register_event_type("on_node_removed")
TrackNetwork.register_event_type("on_edge_added")
TrackNetwork.register_event_type("on_cleared")
