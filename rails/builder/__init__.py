from rails.builder.modes import *


class Builder:
    def __init__(self, network):
        self.network = network
        self.modes = {
            "ADD_TRACK": AddTrackMode(network)
        }
        self.current_mode = self.modes["ADD_TRACK"]

    def on_load(self):
        self.current_mode.on_load()

    def on_mouse_motion(self, x, y, dx, dy):
        self.current_mode.on_mouse_motion(x, y, dx, dy)
    
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.current_mode.on_mouse_drag(x, y, dx, dy, buttons, modifiers)
    
    def on_mouse_press(self, x, y, button, modifiers):
        self.current_mode.on_mouse_press(x, y, button, modifiers)
    
    def on_mouse_release(self, x, y, button, modifiers):
        self.current_mode.on_mouse_release(x, y, button, modifiers)

    def on_mouse_enter(self, x, y):
        self.current_mode.on_mouse_enter(x, y)
    
    def on_mouse_leave(self, x, y):
        self.current_mode.on_mouse_leave(x, y)
    
    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        self.current_mode.on_mouse_scroll(x, y, scroll_x, scroll_y)

    def on_key_press(self, symbol, modifiers):
        self.current_mode.on_key_press(symbol, modifiers)
    
    def on_key_release(self, symbol, modifiers):
        self.current_mode.on_key_release(symbol, modifiers)
