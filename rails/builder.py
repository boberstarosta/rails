import pyglet
from rails import input


class Builder(pyglet.event.EventDispatcher):
    def __init__(self, network):
        self.network = network
        self.highlighted_node = None
        self.selected_node = None

    def highlight_node(self, node):
        self.highlighted_node = node
        self.dispatch_event("on_node_highlighted", node)

    def select_node(self, node):
        self.selected_node = node
        self.dispatch_event("on_node_selected", node)

    def on_mouse_motion(self, x, y, dx, dy):
        self.highlight_node(self.network.nearest_node(input.state.cursor))
    
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if buttons & pyglet.window.mouse.LEFT:
            self.highlight_node(self.network.nearest_node(input.state.cursor, self.selected_node))
    
    def on_mouse_press(self, x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            self.select_node(self.network.nearest_node(input.state.cursor))
            self.highlight_node(self.network.nearest_node(input.state.cursor, self.selected_node))
    
    def on_mouse_release(self, x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            self.select_node(None)


Builder.register_event_type("on_node_highlighted")
Builder.register_event_type("on_node_selected")
