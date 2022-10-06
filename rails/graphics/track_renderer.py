import settings
from rails import graphics
from rails.graphics.base_network_renderer import BaseNetworkRenderer


class TrackRenderer(BaseNetworkRenderer):
    node_radius = settings.NODE_RADIUS
    node_color = settings.NODE_COLOR
    node_group = graphics.groups.NODES
    edge_width = settings.EDGE_WIDTH
    edge_color = settings.EDGE_COLOR
    edge_group = graphics.groups.EDGES
