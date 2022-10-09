import settings
from typing import Dict, Iterable, Tuple, Type, Union
from rails.renderers.track_renderer import TrackRenderer
from rails.graph import Graph
from rails.vec import Vec


class TrackNode:
    def __init__(self, position):
        self._position = Vec(position)

    @property
    def position(self):
        return self._position

    def serialize(self):
        return {"position": tuple(self.position)}

    def __str__(self):
        return f"{self.__class__.__name__}(position={self.position})"


class TrackManager:
    def __init__(self) -> None:
        self.graph = Graph(directed=False, loops_allowed=False)
        self.renderer = TrackRenderer()

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
        for node in self.graph.nodes:
            dist_sq = (node.position - point).length_sq
            if dist_sq < search_radius_sq and dist_sq < min_dist_sq and node not in exclude:
                min_dist_sq = dist_sq
                nearest = node
        return nearest

    def create_node(self, point: Vec) -> TrackNode:
        new_node = TrackNode(point)
        self.graph.add_node(new_node)
        self.renderer.on_node_added(new_node)
        return new_node
    
    def delete_node(self, node: TrackNode) -> None:
        self.graph.remove_node(node)
        self.nodes.remove(element=node)
        self.dispatch_event("on_node_removed", node)

    def create_edge(self, source: Union[Vec, TrackNode], target: Union[Vec, TrackNode]) -> Tuple[TrackNode, TrackNode]:
        source_node = source if source in self.graph.nodes else self.create_node(source)
        target_node = target if target in self.graph.nodes else self.create_node(target)
        self.graph.add_edge(source_node, target_node)
        self.renderer.on_edge_added(source_node, target_node)
        return (source_node, target_node)

    def clear(self) -> None:
        self.graph = Graph(directed=False, loops_allowed=False)
        self.renderer.on_cleared()

    def serialize(self) -> Dict:
        nodes = list(self.graph.nodes)
        node_id_map = {node.serialize(): i for i, node in enumerate(nodes)}
        edges = [
            (node_id_map[node], node_id_map[adjacent_node])
            for node in nodes
            for adjacent_node in self.graph.adjacent(node)
        ]
        return {"nodes": nodes, "edges": edges}

    def load(self, data: Dict) -> None:
        self.clear()

        node_id_map = {}

        for i, node_data in enumerate(data["nodes"]):
            node = self.create_node(node_data["position"])
            node_id_map[i] = node

        for source_id, target_id in data["edges"]:
            source_node = node_id_map[source_id]
            target_node = node_id_map[target_id]
            self.create_edge(source_node, target_node)
