import settings
from rails.network import Network, Node


class TrackNode(Node):
    pass


class TrackNetwork(Network):
    node_class = TrackNode
    max_node_connections = settings.MAX_TRACK_NODE_CONNECTIONS
    min_edge_length = settings.MIN_TRACK_LENGTH
