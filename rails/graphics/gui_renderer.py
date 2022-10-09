import pyglet
import settings
from rails import graphics


class WidgetShapes:
    def __init__(self, widget):
        self.background = pyglet.shapes.Rectangle(
            *widget.rect,
            color=settings.GUI_WIDGET_BG_COLOR,
            batch=graphics.batch,
            group=graphics.groups.GUI_WIDGET_BACKGROUND
        )


class GuiRenderer:
    def __init__(self):
        self.shapes = {}

    def on_widget_created(self, widget):
        self.shapes[widget] = WidgetShapes(widget)
