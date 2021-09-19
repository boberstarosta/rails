class Graph:
    def __init__(self):
        self._map = {}

    @property
    def node_count(self):
        return len(self._map)

    @property
    def nodes(self):
        return self._map.keys()
    
    @property
    def edge_count(self):
        total = sum(len(self._map[n]) for n in self._map)
        return total // 2

    @property
    def edges(self):
        return {
            frozenset((origin, destination))
            for origin in self._map
            for destination in self._map[origin]
        }
    
    def has_node(self, node):
        return node in self._map

    def has_edge(self, origin, destination):
        return origin in self._map and destination in self._map[origin]

    def get_edge(self, origin, destination):
        if origin not in self._map:
            return None
        return self._map[origin].get(destination)

    def incident_edges(self, node):
        for other in self._map[node]:
            yield frozenset((node, other))
    
    def adjacent_nodes(self, node):
        return (other for other in self._map[node])

    def add_node(self, node):
        self._map[node] = set()
        return node

    def add_nodes(self, *args):
        for node in args:
            self.add_node(node)
        return args
    
    def add_edge(self, origin, destination):
        if not self.has_node(origin):
            self.add_node(origin)
        if not self.has_node(destination):
            self.add_node(destination)
        self._map[origin].add(destination)
        self._map[destination].add(origin)
        return (origin, destination)

    def add_edges(self, *args):
        for origin, destination in args:
            self.add_edge(origin, destination)

    def remove_node(self, node):
        del self._map[node]
        for secondary in self._map.values():
            if node in secondary:
                secondary.remove(node)

    def remove_nodes(self, *args):
        for node in args:
            self.remove_node(node)

    def remove_edge(self, origin, destination):
        self._map[origin].remove(destination)

    def remove_edges(self, *args):
        for origin, destination in args:
            self.remove_edge(origin, destination)
