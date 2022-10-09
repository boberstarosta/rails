import pyglet
from rails import graphics


class TrainRenderer:
    def __init__(self):
        self.sprites = {}

    def on_car_added(self, car):
        self.sprites[car] = pyglet.sprite.Sprite(
            graphics.images["arrow red.png"],
            batch=graphics.batch,
            group=graphics.groups.TRAINS
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
