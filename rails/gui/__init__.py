import logging
import pyglet

from rails.graphics.gui_renderer import GuiRenderer
from rails.rect import Rect


gui = None


class Widget:
    def __init__(self, rect):
        self._rect = rect
        logging.debug(f"{self.__class__.__name__} created at {self.rect}")

    @property
    def rect(self):
        return self._rect

    def hover(self): pass
    def click(self): pass


class Button(Widget):
    def __init__(self, rect, text, action):
        super().__init__(rect)
        self._text = text
        self.action = action
    
    @property
    def text(self):
        return self._text
    

class Gui(pyglet.event.EventDispatcher):
    def __init__(self, window):
        self.window = window
        self.renderer = GuiRenderer()
        self.widgets = []

        self.hovered_widget = None
        self.active_widget = None

        self.push_handlers(self.renderer)
        self.create_widgets()

    def button(self, rect, text, action):
        self.widgets.append(Button(rect, text, action))
        self.dispatch_event("on_widget_created", self.widgets[-1])

    def create_widgets(self):
        self.button(Rect(10, 10, 200, 50), "Test Button", lambda: print("test"))

    def on_mouse_motion(self, x, y, dx, dy):
        pass

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        pass

    def on_mouse_release(self, x, y, button, modifiers):
        pass


Gui.register_event_type("on_widget_created")
