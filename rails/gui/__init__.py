import pyglet

from rails.graphics.gui_renderer import GuiRenderer


gui = None


class Widget:
    def __init__(self, rect):
        self._rect = rect

    @property
    def rect(self):
        return self.rect


class Button(Widget):
    def __init__(self, rect, text, action):
        super().__init__(rect)
        self._text = text
        self._action = action

    def click(self):
        self._action()


class Gui(pyglet.event.EventDispatcher):
    def __init__(self, window):
        self.window = window
        self.renderer = GuiRenderer()
        self.push_handlers(self.renderer)

    def on_mouse_motion(self, x, y, dx, dy):
        pass

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        pass

    def on_mouse_release(self, x, y, button, modifiers):
        pass


Gui.register_event_type("on_widget_created")
