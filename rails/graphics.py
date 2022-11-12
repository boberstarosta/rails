import itertools
import os
import pyglet
import settings


def _load_all_images(path):
    pyglet.resource.path = [path]
    pyglet.resource.reindex()
    images = {
        image_file: pyglet.resource.image(image_file)
        for image_file in os.listdir(path)
        if os.path.splitext(image_file)[1] in (".jpg", ".png")
    }
    for image in images.values():
        image.anchor_x = image.width/2
        image.anchor_y = image.height/2
    return images


batch = pyglet.graphics.Batch()
images = _load_all_images(settings.CONTENT_PATH)

_layer_iter = itertools.count()

class groups:
    TRACK_EDGES = pyglet.graphics.OrderedGroup(next(_layer_iter))
    TRACK_NODES = pyglet.graphics.OrderedGroup(next(_layer_iter))
    TRAINS      = pyglet.graphics.OrderedGroup(next(_layer_iter))

    BUILDER_HIGHLIGHT = pyglet.graphics.OrderedGroup(next(_layer_iter))

    GUI_BG          = pyglet.graphics.OrderedGroup(next(_layer_iter))
    GUI_BUTTON_BG   = pyglet.graphics.OrderedGroup(next(_layer_iter))
    GUI_BUTTON_TEXT = pyglet.graphics.OrderedGroup(next(_layer_iter))


def setup_opengl():
    pyglet.gl.glClearColor(*settings.WINDOW_CLEAR_COLOR)
