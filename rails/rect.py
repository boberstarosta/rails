import collections
from rails.vec import Vec


class Rect(collections.namedtuple("Rect", ("left", "bottom", "width", "height"))):
    @property
    def right(self):
        return self.left + self.width
    
    @property
    def top(self):
        return self.bottom + self.height

    @property
    def bottom_left(self):
        return Vec(self.bottom, self.left)

    @property
    def top_right(self):
        return Vec(self.top, self.right)

    @property
    def size(self):
        return Vec(self.width, self.height)

    def contains(self, point):
        return (
            self.left <= point.x <= self.right and
            self.bottom <= point.y <= self.top
        )
