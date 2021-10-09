from math import dist
from rail.event import Event


class Vehicle:
    on_create = Event()
    on_move = Event()
    
    def __init__(self, tracks, node1, node2, offset):
        self.tracks = tracks
        self.node1 = node1
        self.node2 = node2
        self.offset = offset
        self.on_create(self)

    @property
    def direction(self):
        """Return direction from node1 to node2 as a unit vector."""
        return (self.node2.position - self.node1.position).normalized

    @property
    def position(self):
        """Return 2D position."""
        return self.node1.position + self.direction*self.offset

    def move(self, distance):
        if distance < 0:
            self.node1, self.node2 = self.node2, self.node1
            segment_length = (self.node2.position - self.node1.position).length
            self.offset = segment_length - self.offset
            distance *= -1
        self._do_move(distance)
        self.on_move(self)

    def _do_move(self, distance):
        segment_length = (self.node2.position - self.node1.position).length
        distance_left = segment_length - self.offset
        if distance >= distance_left:
            next_node = self.tracks.get_next_node(self.node1, self.node2)
            if next_node is not None:
                self.node1 = self.node2
                self.node2 = next_node
                self.offset = 0
                self._do_move(distance - distance_left)
            else:
                self.offset = segment_length
        else:
            self.offset += distance


class VehicleManager:
    def __init__(self, tracks):
        self.tracks = tracks
        self.vehicles = []
    
    def create_vehicle(self, node1, node2, offset):
        vehicle = Vehicle(self.tracks, node1, node2, offset)
        self.vehicles.append(vehicle)
        return vehicle
