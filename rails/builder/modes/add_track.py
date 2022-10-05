import pyglet
import settings
from rails import graphics
from rails import input
from rails.builder.modes.base import BaseBuiilderMode


class AddTrackMode(BaseBuiilderMode):
    def __init__(self, network):
        super().__init__(network)

        self.node_under_cursor = None
        self.node_under_cursor_sprite = pyglet.shapes.Circle(
            0, 0, settings.NODE_RADIUS, 30,
            settings.BUILDER_NODE_UNDER_CURSOR_COLOR,
            batch=graphics.batch,
            group=graphics.GROUPS.BUILDER_HIGHLIGHT
        )
        self.node_under_cursor_sprite.visible = False

        self.selected_node = None
        self.selected_node_sprite = pyglet.shapes.Circle(
            0, 0, settings.NODE_RADIUS, 30,
            settings.BUILDER_SELECTED_NODE_COLOR,
            batch=graphics.batch,
            group=graphics.GROUPS.BUILDER_SELECT
        )
        self.selected_node_sprite.visible = False

        self.new_target = None
        self.new_target_sprite = pyglet.shapes.Circle(
            0, 0, settings.NODE_RADIUS, 30,
            settings.BUILDER_SELECTED_NODE_COLOR,
            batch=graphics.batch,
            group=graphics.GROUPS.BUILDER_SELECT
        )
        self.new_target_sprite.visible = False
    
    def highlight_node(self, node):
        self.node_under_cursor = node
        if node is None:
            self.node_under_cursor_sprite.visible = False
        else:
            self.node_under_cursor_sprite.position = node.position
            self.node_under_cursor_sprite.visible = True

    def select_node(self, node):
        self.selected_node = node
        if node is None:
            self.selected_node_sprite.visible = False
        else:
            self.selected_node_sprite.position = node.position
            self.selected_node_sprite.visible = True

    def on_load(self):
        self.highlight_node(input.state.cursor)

    def on_mouse_motion(self, x, y, dx,dy):
        self.highlight_node(self.network.nearest_track_node(input.state.cursor))

    def on_mouse_press(self, x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            self.select_node(self.node_under_cursor)
            self.highlight_node(None)

    def on_mouse_release(self, x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            self.select_node(None)
            self.highlight_node(self.network.nearest_track_node(input.state.cursor))
