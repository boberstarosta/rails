import pyglet
from rails import graphics
from rails.builder import Builder
from rails.rect import Rect
from rails.vec import Vec


theme = {
    "padding": 10,
    "panel_width": 250,
    "panel_bg": (80, 80, 80),
    "button_height": 32,
    "button_bg_color": (50, 100, 120),
    "button_hover_bg_color": (70, 140, 210),
    "button_active_bg_color": (50, 160, 120),
    "button_active_hover_bg_color": (70, 180, 140),
    "button_text_size": 13,
    "button_text_color": (255, 255, 255, 255),
}


class Button:
    def __init__(self, rect: Rect, text: str, action) -> None:
        self._rect = rect
        self._text = text
        self._action = action
        self._back_rect = pyglet.shapes.Rectangle(
            *rect,
            color=theme["button_bg_color"],
            batch=graphics.batch,
            group=graphics.groups.GUI_BUTTON_BG
        )
        self._label = pyglet.text.Label(
            text=text,
            font_size=theme["button_text_size"],
            color=theme["button_text_color"],
            batch=graphics.batch,
            group=graphics.groups.GUI_BUTTON_TEXT
        )
        self._label.update(self.rect.left + 10, self.rect.bottom + 10)

    def hover(self):
        self._back_rect.color = theme["button_hover_bg_color"]

    def unhover(self):
        self._back_rect.color = theme["button_bg_color"]

    def click(self):
        if self._action is not None:
            self._action()

    @property
    def rect(self):
        return self._rect


class ToggleButton(Button):
    def __init__(self, rect, text, action):
        super().__init__(rect, text, action)
        self._active = False

    def hover(self):
        if self._active:
            self._back_rect.color = theme["button_active_hover_bg_color"]
        else:
            self._back_rect.color = theme["button_hover_bg_color"]

    def unhover(self):
        if self._active:
            self._back_rect.color = theme["button_active_bg_color"]
        else:
            self._back_rect.color = theme["button_bg_color"]

    def click(self):
        self._active = not self._active
        if self._active:
            self._back_rect.color = theme["button_active_bg_color"]
        else:
            self._back_rect.color = theme["button_bg_color"]


class Gui:
    def __init__(self, window: pyglet.window.Window, builder: Builder) -> None:
        self._window = window
        width = theme["panel_width"]
        self._rect = Rect(window.width - width, 0, width, window.height)
        self._panel_rect = pyglet.shapes.Rectangle(
            *self._rect,
            color=theme["panel_bg"],
            batch=graphics.batch,
            group=graphics.groups.GUI_BG
        )
        self._buttons = []
        self._hovered_element = None

        self.append_widget(Button, "Button A", lambda: print("A"))
        self.append_widget(Button, "Button B", lambda: print("B"))
        self.append_widget(ToggleButton, "Toggle", None)
    
    def append_widget(self, widget_class, text: str, action: callable) -> Button:
        padding = theme["padding"]
        button_height = theme["button_height"]
        rect = Rect(
            self._window.width - self._rect.width + padding,
            self._window.height - ((len(self._buttons) + 1)*(padding + button_height)),
            self._rect.width - 2*padding,
            button_height
        )
        button = widget_class(rect, text, action)
        self._buttons.append(button)
        return button

    def _update_hover(self, position):
        hovered_element = None
        for button in self._buttons:
            if button.rect.contains(position):
                hovered_element = button
                button.hover()
            else:
                button.unhover()
        if hovered_element is not self._hovered_element:
            self._hovered_element = hovered_element

    def on_mouse_motion(self, x, y, dx, dy):
        self._update_hover(Vec(x, y))
        if self._rect.contains(Vec(x, y)):
            return pyglet.event.EVENT_HANDLED

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self._update_hover(Vec(x, y))
        if self._rect.contains(Vec(x, y)):
            return pyglet.event.EVENT_HANDLED

    def on_mouse_press(self, x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            self._active_element = self._hovered_element
        if self._rect.contains(Vec(x, y)):
            return pyglet.event.EVENT_HANDLED

    def on_mouse_release(self, x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            if (
                self._active_element is self._hovered_element and
                self._active_element is not None
            ):
                self._active_element.click()
            self._active_element = None
        if self._rect.contains(Vec(x, y)):
            return pyglet.event.EVENT_HANDLED
