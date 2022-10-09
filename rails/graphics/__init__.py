import itertools
import os
import pyglet
import settings

batch = pyglet.graphics.Batch()
images = None


_layer_iter = itertools.count()

class groups:
    EDGES = pyglet.graphics.OrderedGroup(next(_layer_iter))
    NODES = pyglet.graphics.OrderedGroup(next(_layer_iter))

    BUILDER_PLAN_TRACK = pyglet.graphics.OrderedGroup(next(_layer_iter))
    BUILDER_PLAN_NODE = pyglet.graphics.OrderedGroup(next(_layer_iter))
    BUILDER_CONTROL_TRACK = pyglet.graphics.OrderedGroup(next(_layer_iter))
    BUILDER_CONTROL_NODE = pyglet.graphics.OrderedGroup(next(_layer_iter))
    BUILDER_SELECT = pyglet.graphics.OrderedGroup(next(_layer_iter))
    BUILDER_HIGHLIGHT = pyglet.graphics.OrderedGroup(next(_layer_iter))

    TRAINS = pyglet.graphics.OrderedGroup(next(_layer_iter))

    GUI_BACKGROUND = pyglet.graphics.OrderedGroup(next(_layer_iter))
    GUI_WIDGET_BACKGROUND = pyglet.graphics.OrderedGroup(next(_layer_iter))
    GUI_WIDGET_FOREGROUND = pyglet.graphics.OrderedGroup(next(_layer_iter))


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
