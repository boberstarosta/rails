import logging
import pyglet
import settings
from rails import graphics


class WidgetShapes:
    def __init__(self, widget):
        print(widget.rect)
        self.background = pyglet.shapes.Rectangle(
            *widget.rect,
            color=settings.GUI_WIDGET_BG_COLOR,
            batch=graphics.batch,
            group=graphics.groups.GUI_WIDGET_BACKGROUND
        )
        self.text = pyglet.text.Label(
            text=widget.text,
            font_size=settings.GUI_WIDGET_FONT_SIZE,
            stretch=True,
            color=settings.GUI_WIDGET_FG_COLOR,
            x=widget.rect.left,
            y=widget.rect.bottom,
            width=widget.rect.width,
            height=widget.rect.height,
            anchor_x="left",
            anchor_y="bottom",
            align="center",
            batch=graphics.batch,
            group=graphics.groups.GUI_WIDGET_FOREGROUND
        )
        logging.debug(f"gui shapes created for {widget}")


class GuiRenderer:
    def __init__(self):
        self.shapes = {}

    def on_widget_created(self, widget):
        self.shapes[widget] = WidgetShapes(widget)
