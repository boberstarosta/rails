import pyglet
from pyglet import gl
from rail import config


class App:
    def __init__(self):
        width, height = config.WINDOW_SIZE
        self.window = pyglet.window.Window(width=width, height=height)
        self.window.push_handlers(self)
        pyglet.clock.schedule_interval(self.on_update, 1.0 / config.FPS)
        self.setup_opengl()

    def setup_opengl(self):
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

    def on_update(self, dt):
        pass

    def on_draw(self):
        self.window.clear()
