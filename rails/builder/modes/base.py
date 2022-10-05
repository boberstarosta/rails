class BaseBuiilderMode:
    def __init__(self, network):
        self.network = network

    def on_mouse_motion(self, x, y, dx, dy): pass
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers): pass
    def on_mouse_press(self, x, y, button, modifiers): pass
    def on_mouse_release(self, x, y, button, modifiers): pass
    def on_mouse_enter(self, x, y): pass
    def on_mouse_leave(self, x, y): pass
    def on_mouse_scroll(self, x, y, scroll_x, scroll_y): pass
    def on_key_press(self, symbol, modifiers): pass
    def on_key_release(self, symbol, modifiers): pass
