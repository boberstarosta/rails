import itertools
import os
import pyglet
import settings


batch = pyglet.graphics.Batch()
images = None


_layer_iter = itertools.count()

class GROUPS:
    EDGES = pyglet.graphics.OrderedGroup(next(_layer_iter))
    NODES = pyglet.graphics.OrderedGroup(next(_layer_iter))
    BUILDER_NEW_TRACK = pyglet.graphics.OrderedGroup(next(_layer_iter))
    BUILDER_NEW_NODE = pyglet.graphics.OrderedGroup(next(_layer_iter))
    BUILDER_SELECT = pyglet.graphics.OrderedGroup(next(_layer_iter))
    BUILDER_HIGHLIGHT = pyglet.graphics.OrderedGroup(next(_layer_iter))
    TRAINS = pyglet.graphics.OrderedGroup(next(_layer_iter))


class TrackRenderer:
    def __init__(self):
        self.sprites = {}

    def on_node_added(self, node):
        self.sprites[node] = (pyglet.shapes.Circle(
            *node.position, settings.NODE_RADIUS, 20,
            color=settings.NODE_COLOR,
            batch=batch,
            group=GROUPS.NODES
        ))

    def on_edge_added(self, source, target):
        self.sprites[source, target] = (pyglet.shapes.Line(
            *source.position, *target.position,
            settings.EDGE_WIDTH,
            settings.EDGE_COLOR,
            batch=batch,
            group=GROUPS.EDGES
        ))

    def on_cleared(self):
        while self.sprites:
            self.sprites.popitem()[1].delete()


class TrainRenderer:
    def __init__(self):
        self.sprites = {}

    def on_car_added(self, car):
        self.sprites[car] = pyglet.sprite.Sprite(
            images["arrow red.png"],
            batch=batch,
            group=GROUPS.TRAINS
        )
        self.on_car_updated(car)

    def on_car_updated(self, car):
        self.sprites[car].update(
            *car.position,
            rotation = -car.rotation
        )

    def on_cleared(self):
        while self.sprites:
            self.sprites.popitem()[1].delete()


def init():
    global images

    pyglet.resource.path = [settings.CONTENT_PATH]
    pyglet.resource.reindex()
    images = {
        image_file: pyglet.resource.image(image_file)
        for image_file in os.listdir(settings.CONTENT_PATH)
        if os.path.splitext(image_file)[1] in settings.IMAGE_EXTENSIONS
    }
    for image in images.values():
        image.anchor_x = image.width/2
        image.anchor_y = image.height/2

    pyglet.gl.glClearColor(*settings.WINDOW_CLEAR_COLOR)
