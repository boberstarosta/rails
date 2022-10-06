from rails.vec import Vec


state = None


class InputState:
    def __init__(self):
        self._cursor = Vec(0, 0)

    def on_mouse_motion(self, x, y, dx, dy):
        self._cursor = Vec(x, y)
    
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self._cursor = Vec(x, y)

    def on_mouse_enter(self, x, y):
        self._cursor = Vec(x, y)

    @property
    def cursor(self):
        return self._cursor


def init():
    global state
    state = InputState()
