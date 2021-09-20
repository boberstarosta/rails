import pyglet
from pyglet import gl
from rail import config
from rail.tracks import TrackManager
from rail.renderer import Renderer


class App:
    def __init__(self):
        width, height = config.WINDOW_SIZE
        self.window = pyglet.window.Window(width=width, height=height)
        self.window.push_handlers(self)
        pyglet.clock.schedule_interval(self.on_update, 1.0 / config.FPS)
        self.setup_opengl()

        self.tracks = TrackManager()
        self.renderer = Renderer(self.tracks)

    def setup_opengl(self):
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

    def on_key_press(self, symbol, modifiers):
        if modifiers & pyglet.window.key.MOD_CTRL:
            if symbol == pyglet.window.key.S:
                self.tracks.save("track.json")
            elif symbol == pyglet.window.key.L:
                self.tracks.load("track.json")
            elif symbol == pyglet.window.key.P:
                self.tracks.print()

    def on_update(self, dt):
        pass

    def on_draw(self):
        self.window.clear()
        self.renderer.draw()
