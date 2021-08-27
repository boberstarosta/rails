class Graph:
    def __init__(self, directed=True):
        self._outgoing = {}
        self._incomming = {} if directed else self._outgoing

    @property
    def directed(self):
        return not self._incomming is self._outgoing
    
    @property
    def node_count(self):
        return len(self._outgoing)

    @property
    def nodes(self):
        return self._outgoing.keys()
    
    @property
    def edge_count(self):
        total = sum(len(self._outgoing[n]) for n in self._outgoing)
        return total if self.directed else total // 2

    @property
    def edges(self):
        return (
            (origin, destination)
            for origin in self._outgoing
            for destination in self._outgoing[origin]
        )
    
    def has_node(self, node):
        return node in self._outgoing

    def has_edge(self, origin, destination):
        return origin in self._outgoing and destination in self._outgoing[origin]

    def get_edge(self, origin, destination):
        if origin not in self._outgoing:
            return None
        return self._outgoing[origin].get(destination)

    def incident_edges(self, node, outgoing=True):
        adj = self._outgoing if outgoing else self._incomming
        for other in adj[node]:
            yield (node, other) if outgoing else (other, node)
    
    def adjacent_nodes(self, node, outgoing=True):
        adj = self._outgoing if outgoing else self._incomming
        return (other for other in adj[node])

    def add_node(self, node):
        self._outgoing[node] = set()
        self._incomming[node] = set()
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
        self._outgoing[origin].add(destination)
        self._incomming[destination].add(origin)
        return (origin, destination)

    def add_edges(self, *args):
        for origin, destination in args:
            self.add_edge(origin, destination)

    def remove_node(self, node):
        del self._outgoing[node]
        for secondary in self._outgoing.values():
            if node in secondary:
                secondary.remove(node)
        if self.directed:
            del self._incomming[node]

    def remove_nodes(self, *args):
        for node in args:
            self.remove_node(node)

    def remove_edge(self, origin, destination):
        self._outgoing[origin].remove(destination)
        self._incomming[destination].remove(origin)

    def remove_edges(self, *args):
        for origin, destination in args:
            self.remove_edge(origin, destination)
