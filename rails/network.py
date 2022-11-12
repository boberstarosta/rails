from __future__ import annotations
from collections import namedtuple
from typing import Any
from rails.graph import Graph
from rails.vec import Vec
from rails.renderers import NetworkRenderer


class Node:
    def __init__(self, network: Network, id: int, position: Vec):
        self._network = network
        self._id = id
        self._position = position

    @property
    def id(self):
        return self._id

    @property
    def position(self) -> Vec:
        return self._position

    def next(self, source: Node) -> Node | None:
        return self._network.next_node(source, self)

    def serialize(self) -> dict[str: Any]:
        return {"position": tuple(self.position)}

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(position={self.position})"


class Network:
    search_radius = 30
    renderer_class: type[NetworkRenderer] = NetworkRenderer

    def __init__(self) -> None:
        self._nodes = {}
        self._graph = Graph(directed=False, loops_allowed=False)
        self._renderer = self.renderer_class()
        self._max_node_id = 0

    def get_node(self, node_id: id) -> Node | None:
        return self._nodes[node_id]

    def next_node(self, source: Node, pivot: Node) -> Node:
        try:
            return next(n for n in self._graph.adjacent(pivot) if n is not source)
        except StopIteration:
            return None

    def nearest_node(self, point: Vec, exclude: Node | None = None) -> Node | None:
        search_radius_sq = self.search_radius**2
        nearest = None
        min_dist_sq = float("inf")
        for node in self._graph.nodes:
            dist_sq = (node.position - point).length_sq
            if dist_sq < min_dist_sq and dist_sq < search_radius_sq and node is not exclude:
                min_dist_sq = dist_sq
                nearest = node
        return nearest

    def create_node(self, point: Vec, node_id: int | None = None) -> Node:
        if node_id is None:
            node_id = self._max_node_id
        self._max_node_id += 1
        new_node = Node(self, node_id, point)
        self._nodes[new_node.id] = new_node
        self._graph.add_node(new_node)
        self._renderer.add_node(new_node)
        return new_node

    def create_edge(self, source: Vec | Node, target: Vec | Node) -> tuple[Node, Node]:
        source_node = source if source in self._graph.nodes else self.create_node(source)
        target_node = target if target in self._graph.nodes else self.create_node(target)
        self._graph.add_edge(source_node, target_node)
        self._renderer.add_edge(source_node, target_node)
        return (source_node, target_node)

    def clear(self) -> None:
        self._graph = Graph(directed=False, loops_allowed=False)
        self._renderer.clear()
        self._max_node_id = 0

    def serialize(self) -> dict[str: Any]:
        nodes = list(self._graph.nodes)
        node_id_map = {node.serialize(): i for i, node in enumerate(nodes)}
        edges = [
            (node_id_map[node], node_id_map[adjacent_node])
            for node in nodes
            for adjacent_node in self._graph.adjacent(node)
        ]
        return {"nodes": nodes, "edges": edges}

    def load(self, data: dict[str: Any]) -> None:
        self.clear()
        for node_data in data["nodes"]:
            self.create_node(Vec(node_data["position"]), node_id=node_data["id"])
        for source_id, target_id in data["edges"]:
            source_node = self._nodes[source_id]
            target_node = self._nodes[target_id]
            self.create_edge(source_node, target_node)


class Location(namedtuple("Location", ("source", "target", "place"))):
    @property
    def position(self) -> Vec:
        direction = (self.target.position - self.source.position).normalized
        return self.source.position + direction*self.place

    def move(self, distance: float) -> tuple[Location, bool]:
        if distance == 0:
            return self, False
        length = (self.target.position - self.source.position).length
        source, target = self.source, self.target
        place = self.place + distance
        while place > length:
            next_node = target.next(source)
            if next_node is None:
                return Location(source, target, length), True
            source, target = target, next_node
            place -= length
            length = (target.position - source.position).length
        while place < 0:
            prev_node = source.next(target)
            if prev_node is None:
                return Location(source, target, 0), True
            source, target = prev_node, source
            length = (target.position - source.position).length
            place += length
        return Location(source, target, place), False
