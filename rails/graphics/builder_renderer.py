import pyglet
import settings
from rails import graphics


class BuilderRenderer:
    node_radius = settings.NODE_RADIUS
    highlight_color = settings.BUILDER_HIGHLIGHT_COLOR
    select_color = settings.BUILDER_SELECT_COLOR

    def __init__(self):
        self.highlighted_node = pyglet.shapes.Circle(
            0, 0, self.node_radius, 20,
            color=self.highlight_color,
            batch=graphics.batch,
            group=graphics.groups.BUILDER_HIGHLIGHT
        )
        self.highlighted_node.visible = False
        self.selected_node = pyglet.shapes.Circle(
            0, 0, self.node_radius, 20,
            color=self.select_color,
            batch=graphics.batch,
            group=graphics.groups.BUILDER_SELECT
        )
        self.selected_node.visible = False
    
    def on_node_highlighted(self, node):
        if node is None:
            self.highlighted_node.visible = False
        else:
            self.highlighted_node.position = node.position
            self.highlighted_node.visible = True

    def on_node_selected(self, node):
        if node is None:
            self.selected_node.visible = False
        else:
            self.selected_node.position = node.position
            self.selected_node.visible = True
