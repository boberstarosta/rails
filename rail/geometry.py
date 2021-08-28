from collections import namedtuple


class Vec(namedtuple("Vec", ("x", "y"))):
    def __new__(cls, *args):
        if len(args) == 2:
            x, y = args
        elif len(args) == 1:
            x, y = args[0]
        elif len(args) == 0:
            x, y = 0, 0
        return super().__new__(cls, x, y)
    
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
