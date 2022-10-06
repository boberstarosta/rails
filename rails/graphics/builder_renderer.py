import pyglet
import settings
from rails import graphics


class BuilderRenderer:
    node_radius = settings.NODE_RADIUS
    edge_width = settings.EDGE_WIDTH
    highlight_color = settings.BUILDER_HIGHLIGHT_COLOR
    select_color = settings.BUILDER_SELECT_COLOR

    def __init__(self):
        self.highlighted_point = pyglet.shapes.Circle(
            0, 0, self.node_radius, 20,
            color=self.highlight_color,
            batch=graphics.batch,
            group=graphics.groups.BUILDER_HIGHLIGHT
        )
        self.highlighted_point.visible = False

        self.selected_point = pyglet.shapes.Circle(
            0, 0, self.node_radius, 20,
            color=self.select_color,
            batch=graphics.batch,
            group=graphics.groups.BUILDER_SELECT
        )
        self.selected_point.visible = False
    
    def on_point_highlighted(self, point):
        if point is None:
            self.highlighted_point.visible = False
        else:
            self.highlighted_point.position = point
            self.highlighted_point.visible = True

    def on_point_selected(self, point):
        if point is None:
            self.selected_point.visible = False
        else:
            self.selected_point.position = point
            self.selected_point.visible = True
