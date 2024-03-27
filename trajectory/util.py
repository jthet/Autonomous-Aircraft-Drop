from math import degrees, acos

class Vector3:
    __slots__ = ('x', 'y', 'z')

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return 'Vector3(%.3f, %.3f, %.3f)' % (self.x, self.y, self.z)

    def magnitude(self):
        return (self.x**2 + self.y**2 + self.z**2)**0.5

    def unit(self):
        mag = self.magnitude()
        return Vector3(self.x/mag, self.y/mag, self.z/mag)

    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def dot(self, other):
        return self.x*other.x + self.y*other.y + self.z*other.z

    def angle(self, other):
        m = self.unit()
        n = other.unit()
        r = m.dot(n)

        return degrees(acos(r))
