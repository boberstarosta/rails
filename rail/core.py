import pyglet
from pyglet import gl
from rail import config
from rail.tracks import TrackManager
from rail.geometry import Vec


class App:
    def __init__(self):
        width, height = config.WINDOW_SIZE
        self.window = pyglet.window.Window(width=width, height=height)
        self.window.push_handlers(self)
        pyglet.clock.schedule_interval(self.on_update, 1.0 / config.FPS)
        self.setup_opengl()

        self.tracks = TrackManager()
        self.tracks.add_track(Vec(300, 300), Vec(600, 400))

    def setup_opengl(self):
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

    def on_update(self, dt):
        pass

    def on_draw(self):
        self.window.clear()
