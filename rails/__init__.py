import json
import pyglet
import settings
from rails import graphics
from rails import input
from rails.builder import Builder
from rails.network import Network
from rails.rollingstock import RollingStock


class App:
    def __init__(self):
        self.window = pyglet.window.Window(
            width=settings.WINDOW_WIDTH, height=settings.WINDOW_HEIGHT)

        self.network = Network()
        self.rollingstock = RollingStock(self.network)
        self.builder = Builder(self.network)

        self.window.push_handlers(self)
        self.window.push_handlers(input.state)
        self.window.push_handlers(self.builder)
        pyglet.clock.schedule_interval(self.on_tick, 1/settings.FRAMES_PER_SECOND)

    def save(self, filename):
        data = {
            "network": self.network.serialize(),
            "trains": self.rollingstock.serialize()
        }
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        self.window.dispatch_event("on_load")

    def load(self, filename):
        with open(filename) as f:
            data = json.load(f)
        self.network.load(data["network"])
        self.rollingstock.load(data["trains"])

    def on_key_press(self, key, modifiers):
        if modifiers & pyglet.window.key.MOD_CTRL:
            if key == pyglet.window.key.L:
                self.load("testtrack.json")
            if key == pyglet.window.key.S:
                self.save("testtrack.json")

    def on_tick(self, dt):
        self.rollingstock.tick(dt)

    def on_draw(self):
        self.window.clear()
        graphics.batch.draw()


app = None


def init():
    graphics.init()
    input.init()
    global app
    app = App()
