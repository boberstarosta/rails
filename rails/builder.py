import pyglet
import settings
from rails import input


class Builder(pyglet.event.EventDispatcher):
    def __init__(self, network):
        self.network = network

        self.is_building = False

        self.highlighted_node = None
        self.active_node = None
        self.selected_node = None

        self.active_point = None
        self.selected_point = None

    def highlight_nearest_node(self):
        self.highlighted_node = self.network.nearest_node(input.state.cursor)
        point = None if self.highlighted_node is None else self.highlighted_node.position
        self.dispatch_event("on_point_highlighted", point)

    def select_active_node_or_point(self):
        if self.highlighted_node is self.active_node:
            self.selected_node = self.active_node
        self.active_node = None
        if (self.active_point is not None and
            (self.active_point - input.state.cursor).length <= settings.NODE_SEARCH_RADIUS
        ):
            self.selected_point = self.active_point
        self.active_point = None
        point = self.selected_point if self.selected_node is None else self.selected_node.position
        self.dispatch_event("on_point_selected", point)

    def clear_selection(self):
        self.selected_node = None
        self.selected_point = None
        self.dispatch_event("on_point_selected", None)

    def start_building(self):
        self.is_building = True

    def continue_building(self):
        print("continue building")

    def finish_building(self):
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
    
    def on_mouse_release(self, x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            self.select_active_node_or_point()
            if self.is_building:
                self.finish_building()
                self.clear_selection()
            else:
                self.start_building()


Builder.register_event_type("on_point_highlighted")
Builder.register_event_type("on_point_selected")
