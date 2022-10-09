import pyglet
import settings
from rails import graphics


class BuilderRenderer:
    node_radius = settings.NODE_RADIUS
    edge_width = settings.EDGE_WIDTH
    highlight_color = settings.BUILDER_HIGHLIGHT_COLOR
    select_color = settings.BUILDER_SELECT_COLOR
    plan_color = settings.BUILDER_PLAN_COLOR

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

        self.plan_points = []
    
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

    def on_plan_changed(self, points):
        while self.plan_points:
            self.plan_points.pop().delete()
        for point in points:
            self.plan_points.append(pyglet.shapes.Circle(
                *point, self.node_radius, 30,
                color=self.plan_color,
                batch=graphics.batch,
                group=graphics.groups.BUILDER_PLAN_NODE
            ))
        for source, target in zip(points[:-1], points[1:]):
            self.plan_points.append(pyglet.shapes.Line(
                *source, *target, self.edge_width,
                color=self.plan_color,
                batch=graphics.batch,
                group=graphics.groups.BUILDER_PLAN_TRACK
            ))
