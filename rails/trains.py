import pyglet
from rails.renderers import TrainRenderer
from rails.network import Location


class TrainCar:
    def __init__(self, location, speed):
        self._location = location
        self._speed = speed
    
    @property
    def location(self):
        return self._location

    @property
    def speed(self):
        return self._speed

    @property
    def rotation(self):
        rotation = (self.location.target.position - self.location.source.position).angle
        return rotation

    def tick(self, dt):
        self._location, track_end = self.location.move(self.speed * dt)
        if track_end:
            self._speed = 0

    def serialize(self):
        return {
            "location": {
                "source": self.location.source.id,
                "target": self.location.target.id,
                "place": self.location.place
            },
            "speed": self.speed
        }

    @classmethod
    def deserialize(cls, data, network):
        source = network.get_node(data["location"]["source"])
        target = network.get_node(data["location"]["target"])
        place = data["location"]["place"]
        return cls(Location(source, target, place), data["speed"])


class Trains:
    def __init__(self, network):
        self._network = network
        self._cars = []
        self._renderer = TrainRenderer()
    
    def create_car(self, node1, node2, place):
        new_car = TrainCar(node1, node2, place)
        return self.add_car(new_car)

    def add_car(self, car: TrainCar) -> TrainCar:
        self._cars.append(car)
        self._renderer.add_car(car)
        return car

    def clear(self):
        self._cars = []
        self._renderer.clear()

    def tick(self, dt):
        for car in self._cars:
            car.tick(dt)
            self._renderer.update_car(car)

    def serialize(self):
        cars = [car.serialize() for car in self._cars.values()]
        return {"cars": cars}

    def load(self, data):
        self.clear()
        for car_data in data["cars"]:
            car = TrainCar.deserialize(car_data, self._network)
            self.add_car(car)
