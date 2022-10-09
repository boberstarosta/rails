import logging
import pyglet
import rails


if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)
    rails.init()
    pyglet.app.run()
