import pyglet
from rails import input
from rails.renderers.builder_renderer import BuilderRenderer


class Builder:
    def __init__(self, track_manager):
        self.track_manager = track_manager
        self.renderer = BuilderRenderer()

        self.is_building = False

        self.highlighted_node = None
        self.active_node = None
        self.selected_node = None

        self.active_point = None
        self.selected_point = None

        self.source_node = None
        self.target_node = None
        self.plan_points = []

    def highlight_nearest_node(self):
        self.highlighted_node = self.track_manager.nearest_node(input.state.cursor)
        point = None if self.highlighted_node is None else self.highlighted_node.position
        self.renderer.on_point_highlighted(point)

    def select_active_node_or_point(self):
        if self.highlighted_node is self.active_node:
            self.selected_node = self.active_node
        self.active_node = None
        if self.active_point is not None:
            self.selected_point = self.active_point
        self.active_point = None
        point = self.selected_point if self.selected_node is None else self.selected_node.position
        self.renderer.on_point_selected(point)

    def clear_selection(self):
        self.selected_node = None
        self.selected_point = None
        self.renderer.on_point_selected(None)

    def start_building(self):
        self.is_building = True
        if self.selected_node is not None:
            self.source_node = self.selected_node
            self.plan_points.append(self.source_node.position)
        else:
            self.plan_points.append(self.selected_point)
        self.plan_points.append(input.state.cursor)

    def continue_building(self):
        self.target_node = self.highlighted_node
        if self.target_node is self.source_node:
            self.target_node = None
        if self.target_node is None:
            self.plan_points[-1] = input.state.cursor
        else:
            self.plan_points[-1] = self.target_node.position
        self.renderer.on_plan_changed(self.plan_points)

    def finish_building(self):
        self.target_node = self.selected_node
        if self.source_node is None:
            start = 0
        else:
            start = 1
            self.track_manager.create_edge(self.source_node, self.plan_points[start])
        if self.target_node is None:
            stop = len(self.plan_points)
        else:
            stop = -1
            self.track_manager.create_edge(self.plan_points[stop-1], self.target_node)

        for source, target in zip(self.plan_points[start:stop-1], self.plan_points[start+1:stop]):
            self.track_manager.create_edge(source, target)

        self.source_node = None
        self.target_node = None
        self.plan_points.clear()
        self.renderer.on_plan_changed(self.plan_points)
        self.is_building = False

    def on_mouse_motion(self, x, y, dx, dy):
        self.highlight_nearest_node()
        if self.is_building:
            self.continue_building()
    
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.highlight_nearest_node()

    def on_mouse_press(self, x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            self.active_node = self.highlighted_node
            if self.active_node is None:
                self.active_point = input.state.cursor
            else:
                self.active_point = None
    
    def on_mouse_release(self, x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            self.select_active_node_or_point()
            if self.is_building:
                self.finish_building()
                self.clear_selection()
            else:
                self.start_building()
