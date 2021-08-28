from collections import namedtuple
import math


class Vector(namedtuple("Vec", ("x", "y"))):
    def __new__(cls, *args):
        if len(args) == 2:
            x, y = args
        elif len(args) == 1:
            x, y = args[0]
        elif len(args) == 0:
            x, y = 0, 0
        return super().__new__(cls, float(x), float(y))
    
    def __add__(self, other):
        return self.__class__(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return self.__class__(self.x - other.x, self.y - other.y)
    
    def __mul__(self, number):
        return self.__class__(self.x * number, self.y * number)
    
    def __truediv__(self, number):
        return self.__class__(self.x / number, self.y / number)
    
    @property
    def length(self):
        return (self.x*self.x + self.y * self.y)**0.5

    @property    
    def length_sq(self):
        return self.x*self.x + self.y * self.y

    @property
    def normalized(self):
        return self / self.length

    def dot(self, other):
        return self.x*other.x + self.y*other.y

    def perpendicular(self, left=True):
        return self.__class__(-self.y, self.x) if left else self.__class__(self.y, -self.x)
    
    @property
    def angle_x(self):
        return math.degrees(math.atan2(self.y, self.x))

    def angle(self, other):
        return other.angle_x - self.angle_x

    @classmethod
    def from_angle_x(cls, degrees, length=1):
        radians = math.radians(degrees)
        return cls(math.cos(radians), math.sin(radians)) * length
