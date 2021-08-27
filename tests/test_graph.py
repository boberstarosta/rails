import unittest
from rail.graph import Graph


class GraphTest(unittest.TestCase):

    def test_directed(self):
        g = Graph()
        self.assertTrue(g.directed)
        g = Graph(directed=False)
        self.assertFalse(g.directed)
    
    def test_node_count(self):
        g = Graph()
        self.assertEqual(g.node_count, 0)
        g.add_nodes("A", "B")
        self.assertEqual(g.node_count, 2)

    def test_nodes(self):
        g = Graph()
        self.assertFalse(g.nodes)
        g.add_nodes("A", "B", "C")
        self.assertEqual(set(g.nodes), {"A", "B", "C"})

    def test_edge_count(self):
        g = Graph()
        self.assertEqual(g.edge_count, 0)
        g.add_nodes("A", "B", "C")
        g.add_edge("A", "B")
        g.add_edge("B", "C")
        self.assertEqual(g.node_count, 3)
        self.assertEqual(g.edge_count, 2)

    def test_edges(self):
        g = Graph()
        g.add_nodes("A", "B", "C", "D")
        self.assertFalse(set(g.edges))
        g.add_edges("AB", "BC", "CD", "DA")
        self.assertEqual(
            set(g.edges),
            {("A", "B"), ("B", "C"), ("C", "D"), ("D", "A")}
        )

    def test_has_node(self):
        g = Graph()
        self.assertFalse(g.has_node("A"))
        g.add_node("A")
        self.assertTrue(g.has_node("A"))

    def test_get_edge(self):
        g = Graph()
        g.add_nodes("A", "B", "C")
        self.assertFalse(g.has_edge("A", "B"))

    def test_incident_edges(self):
        g = Graph()
        g.add_nodes("A", "B", "C")
        g.add_edges("AB", "BC", "CA", "BA")
        self.assertEqual(
            set(g.edges),
            {("A", "B"), ("B", "C"), ("B", "A"), ("C", "A")}
        )
        self.assertEqual(
            set(g.incident_edges("A")),
            {("A", "B")}
        )
        self.assertEqual(
            set(g.incident_edges("A", outgoing=False)),
            {("B", "A"), ("C", "A")}
        )

    def test_adjacent_nodes(self):
        g = Graph()
        g.add_nodes("A", "B", "C", "D")
        self.assertEqual(set(g.adjacent_nodes("A")), set())
        g.add_edges("AB", "BA", "BC", "CA")
        self.assertEqual(
            set(g.adjacent_nodes("B")),
            {"A", "C"}
        )
        self.assertEqual(
            set(g.adjacent_nodes("A", outgoing=False)),
            {"B", "C"}
        )
        self.assertEqual(set(g.adjacent_nodes("D")), set())

    def test_add_node(self):
        g = Graph()
        self.assertFalse(g.has_node("A"))
        g.add_node("A")
        self.assertTrue(g.has_node("A"))
        self.assertFalse(g.has_node("B"))
    
    def test_add_nodes(self):
        g = Graph()
        self.assertFalse(g.has_node("A"))
        self.assertFalse(g.has_node("B"))
        g.add_nodes("A", "B", "C")
        self.assertEqual(set(g.nodes), {"A", "B", "C"})

    def test_add_edge(self):
        g = Graph()
        g.add_nodes("A", "B", "C")
        self.assertEqual(set(g.edges), set())
        g.add_edge("A", "B")
        self.assertEqual(set(g.edges), {("A", "B")})
    
    def test_add_edges(self):
        g = Graph()
        g.add_nodes("A", "B", "C")
        self.assertEqual(g.edge_count, 0)
        g.add_edges("AB", "BC", "BA")
        self.assertEqual(
            set(g.edges), {("A", "B"), ("B", "A"), ("B", "C")})

    def test_remove_node(self):
        g = Graph()
        g.add_nodes("A", "B", "C")
        g.add_edges("AB", "BC", "CA")
        self.assertEqual(set(g.nodes), {"A", "B", "C"})
        self.assertEqual(
            set(g.edges), {("A", "B"), ("B", "C"), ("C", "A")})
        g.remove_node("C")
        self.assertEqual(set(g.nodes), {"A", "B"})
        self.assertEqual(set(g.edges), {("A", "B"),})
