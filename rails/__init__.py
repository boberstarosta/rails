import json
import pyglet
import settings
from rails import graphics
from rails import input
from rails.network import Network
from rails.trains import Trains
from rails.builder import Builder
from rails.gui import Gui


class App:
    def __init__(self):
        self.window = pyglet.window.Window(
            width=settings.WINDOW_WIDTH, height=settings.WINDOW_HEIGHT)
        self.window.set_caption(settings.WINDOW_TITLE)

        self.network = Network()
        self.trains = Trains(self.network)
        self.builder = Builder(self.network)
        self.gui = Gui(self.window, self.builder)

        self.window.push_handlers(self)
        self.window.push_handlers(input.state)
        self.window.push_handlers(self.builder)
        self.window.push_handlers(self.gui)

        pyglet.clock.schedule_interval(self.on_tick, 1/settings.FRAMES_PER_SECOND)

    def save(self, filename):
        data = {
            "network": self.network.serialize(),
            "trains": self.trains.serialize()
        }
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

    def load(self, filename):
        with open(filename) as f:
            data = json.load(f)
        self.network.load(data["network"])
        self.trains.load(data["trains"])

    def on_key_press(self, key, modifiers):
        if modifiers & pyglet.window.key.MOD_CTRL:
            if key == pyglet.window.key.L:
                self.load("testtrack.json")
            if key == pyglet.window.key.S:
                self.save("testtrack.json")

    def on_tick(self, dt):
        self.trains.tick(dt)

    def on_draw(self):
        graphics.setup_opengl()
        self.window.clear()
        graphics.batch.draw()


app = None


def init():
    input.init()
    global app
    app = App()
