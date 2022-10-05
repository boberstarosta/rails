import pyglet
import settings
from rails import graphics
from rails import input
from rails.builder.modes.base import BaseBuiilderMode


class AddTrackMode(BaseBuiilderMode):
    def __init__(self, network):
        super().__init__(network)

        self.highlighted_node = None
        self.highlighted_node_sprite = pyglet.shapes.Circle(
            0, 0, settings.NODE_RADIUS, 30,
            settings.BUILDER_NODE_UNDER_CURSOR_COLOR,
            batch=graphics.batch,
            group=graphics.GROUPS.BUILDER_HIGHLIGHT
        )
        self.highlighted_node_sprite.visible = False

        self.selected_node = None
        self.selected_node_sprite = pyglet.shapes.Circle(
            0, 0, settings.NODE_RADIUS, 30,
            settings.BUILDER_SELECTED_NODE_COLOR,
            batch=graphics.batch,
            group=graphics.GROUPS.BUILDER_SELECT
        )
        self.selected_node_sprite.visible = False

        self.new_source_sprite = pyglet.shapes.Circle(
            0, 0, settings.NODE_RADIUS, 30,
            settings.BUILDER_NEW_COLOR,
            batch=graphics.batch,
            group=graphics.GROUPS.BUILDER_NEW_NODE
        )
        self.new_source_sprite.visible = False

        self.new_target_sprite = pyglet.shapes.Circle(
            0, 0, settings.NODE_RADIUS, 30,
            settings.BUILDER_NEW_COLOR,
            batch=graphics.batch,
            group=graphics.GROUPS.BUILDER_NEW_NODE
        )
        self.new_target_sprite.visible = False
    
        self.new_track_sprite = pyglet.shapes.Line(
            0, 0, 10, 0,
            width=settings.BUILDER_NEW_TRACK_WIDTH,
            color=settings.BUILDER_NEW_COLOR,
            batch=graphics.batch,
            group=graphics.GROUPS.BUILDER_NEW_TRACK
        )
        self.new_track_sprite.visible = False

    def highlight_node(self, node):
        self.highlighted_node = node
        if node is None:
            self.highlighted_node_sprite.visible = False
        else:
            self.highlighted_node_sprite.position = node.position
            self.highlighted_node_sprite.visible = True

    def select_node(self, node):
        self.selected_node = node
        if node is None:
            self.selected_node_sprite.visible = False
        else:
            self.selected_node_sprite.position = node.position
            self.selected_node_sprite.visible = True

    def start_building(self):
        if self.selected_node is None:
            self.new_source_sprite.position = input.state.cursor
        else:
            self.new_source_sprite.position = self.selected_node.position
        self.new_source_sprite.visible = True
        self.new_target_sprite.position = input.state.cursor
        self.new_target_sprite.visible = True
        self.new_track_sprite.position = (
            *self.new_source_sprite.position,
            *self.new_target_sprite.position
        )
        self.new_track_sprite.visible = True
        self.highlight_node(self.network.nearest_track_node(input.state.cursor, self.selected_node))

    def continue_building(self):
        self.highlight_node(self.network.nearest_track_node(input.state.cursor, self.selected_node))
        if self.highlighted_node is None:
            self.new_target_sprite.position = input.state.cursor
        else:
            self.new_target_sprite.position = self.highlighted_node.position
        self.new_track_sprite.position = (
            *self.new_source_sprite.position,
            *self.new_target_sprite.position
        )

    def finish_building(self):
        source_node = None
        if self.selected_node is not None and self.highlighted_node is None:
            source_node = self.selected_node
            extend_point = self.new_target_sprite.position
        elif self.selected_node is None and self.highlight_node is not None:
            source_node = self.highlighted_node
            extend_point = self.new_source_sprite.position
        if source_node is not None and self.network.can_extend_track(source_node, extend_point):
            self.network.extend_track(source_node, extend_point)

        self.select_node(None)
        self.new_source = None
        self.new_target = None
        self.new_source_sprite.visible = False
        self.new_target_sprite.visible = False
        self.new_track_sprite.visible = False

    def on_load(self):
        self.highlight_node(self.network.nearest_track_node(input.state.cursor))

    def on_mouse_motion(self, x, y, dx,dy):
        self.highlight_node(self.network.nearest_track_node(input.state.cursor))

    def on_mouse_press(self, x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            self.select_node(self.highlighted_node)

    def on_mouse_release(self, x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            self.finish_building()
            self.highlight_node(self.network.nearest_track_node(input.state.cursor))

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if buttons & pyglet.window.mouse.LEFT:
            if self.new_source_sprite.visible:
                self.continue_building()
            else:
                self.start_building()
