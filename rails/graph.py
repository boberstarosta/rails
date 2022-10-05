class Graph:
    def __init__(self, directed=False, loops_allowed=False):
        self._directed = directed
        self._loops_allowed = loops_allowed
        self._outgoing = {}
        self._incomming = {} if directed else self._outgoing

    @property
    def directed(self):
        return self._directed

    @property
    def loops_allowed(self):
        return self._loops_allowed

    @property
    def nodes(self):
        return self._outgoing.keys()

    @property
    def edges(self):
        return (
            (a, b)
            for a in self.nodes
            for b in self._outgoing[a]
        )

    def adjacent(self, node, incomming=False):
        result = list(self._outgoing[node])
        if self.directed and incomming:
            result.extend(self._incomming[node])
        return result

    def add_node(self, node):
        if node not in self.nodes:
            self._outgoing[node] = {}
            if self.directed:
                self._incomming[node] = {}

    def add_edge(self, start, end, weight=1):
        if not self.loops_allowed and start is end:
            raise ValueError("Loops not allowed")
        if start not in self.nodes:
            self.add_node(start)
        if end not in self.nodes:
            self.add_node(end)
        self._outgoing[start][end] = weight
        self._incomming[end][start] = weight

    def remove_node(self, node):
        del self._incomming[node]
        del self._outgoing[node]
