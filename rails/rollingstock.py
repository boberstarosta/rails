import pyglet
from rails import graphics
from rails.container import Container, Element


class TrainCar(Element):
    def __init__(self, source_node, target_node, place, speed, inverted=False, id=None):
        super().__init__(id)
        self._nodes = (source_node, target_node)
        self._place = place
        self._inverted = inverted
        self._speed = speed
    
    @property
    def source_node(self):
        return self._nodes[0]
    
    @property
    def target_node(self):
        return self._nodes[1]

    @property
    def place(self):
        return self._place

    @property
    def speed(self):
        return self._speed

    @property
    def inverted(self):
        return self._inverted

    @property
    def position(self):
        direction = (self.target_node.position - self.source_node.position).normalized
        return self.source_node.position + direction*self._place

    @property
    def rotation(self):
        rotation = (self.target_node.position - self.source_node.position).angle
        if self.inverted:
            rotation += 180
        return rotation

    def tick(self, dt, network):
        length = (self.target_node.position - self.source_node.position).length
        self._place += self.speed*dt
        while self._place > length:
            next_node = network.next_node(self.source_node, self.target_node)
            if next_node is None:
                self._place = length
                self._speed = 0
                break
            self._nodes = (self.target_node, next_node)
            self._place -= length
            length = (self.target_node.position - self.source_node.position).length
        while self._place < 0:
            prev_node = network.next_node(self.target_node, self.source_node)
            if prev_node is None:
                self._place = 0
                self._speed = 0
                break
            self._nodes = (prev_node, self.source_node)
            length = (self.target_node.position - self.source_node.position).length
            self._place += length

    def serialize(self):
        return {
            "id": self.id,
            "nodes": [self.source_node.id, self.target_node.id],
            "place": self.place,
            "speed": self.speed,
            "inverted": self.inverted
        }

    @classmethod
    def deserialize(cls, network, data):
        nodes = (network.nodes[node_id] for node_id in data["nodes"])
        return cls(*nodes, data["place"], data["speed"], id=data["id"], inverted=data["inverted"])


class RollingStock(pyglet.event.EventDispatcher):
    def __init__(self, network):
        self.network = network
        self.cars = Container()
    
    def create_car(self, node1, node2, param):
        new_car = TrainCar(node1, node2, param)
        return self.add_car(new_car)

    def add_car(self, car):
        self.cars.add(car)
        self.dispatch_event("on_car_added", car)
        return car

    def clear(self):
        self.cars = Container()
        self.dispatch_event("on_cleared")

    def tick(self, dt):
        for car in self.cars.values():
            car.tick(dt, self.network)
            self.dispatch_event("on_car_updated", car)

    def serialize(self):
        cars = [car.serialize() for car in self.cars.values()]
        return {"cars": cars}

    def load(self, data):
        self.clear()
        for car_data in data["cars"]:
            car = TrainCar.deserialize(self.network, car_data)
            self.add_car(car)


RollingStock.register_event_type("on_car_added")
RollingStock.register_event_type("on_car_updated")
RollingStock.register_event_type("on_cleared")
