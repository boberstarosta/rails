import unittest
from rail.geometry import Vector


class VectorTest(unittest.TestCase):

    def test_init_no_args_creates_zero_vec(self):
        v = Vector()
        self.assertEqual(v, (0, 0))
    
    def test_init_one_arg_unpacks_xy(self):
        v = Vector((2, 3))
        self.assertEqual(v, (2, 3))
    
    def test_init_two_args_xy(self):
        v = Vector(2, 3)
        self.assertEqual(v, (2, 3))
    
    def test_xy_always_float(self):
        v = Vector(1, 2)
        self.assertIsInstance(v.x, float)
        self.assertIsInstance(v.y, float)

    def test_add(self):
        result = Vector(1, 2) + Vector(3, 4)
        self.assertEqual(result, (4, 6))
        self.assertIsInstance(result, Vector)
    
    def test_sub(self):
        result = Vector(3, 4) - Vector(2, 1)
        self.assertEqual(result, (1, 3))
        self.assertIsInstance(result, Vector)

    def test_mul(self):
        result = Vector(3, 4) * 2
        self.assertEqual(result, (6, 8))
        self.assertIsInstance(result, Vector)        

    def test_truediv(self):
        result = Vector(3, 4) / 2
        self.assertEqual(result, (1.5, 2))
        self.assertIsInstance(result, Vector)

    def test_length_sq(self):
        self.assertEqual(Vector(0, 0).length_sq, 0)
        self.assertEqual(Vector(1, -4).length_sq, 17)

    def test_length(self):
        self.assertEqual(Vector(0, 0).length, 0)
        self.assertEqual(Vector(3, -4).length, 5)

    def test_dot(self):
        self.assertEqual(Vector(3, 4).dot(Vector(-4, 3)), 0)
        self.assertEqual(Vector(3, 4).dot(Vector(4, -3)), 0)

    def test_perpendicular(self):
        self.assertEqual(Vector(0, 3).perpendicular(), (-3, 0))
        self.assertEqual(Vector(0, 3).perpendicular(left=False), (3, 0))
        self.assertEqual(Vector(-1, -1).perpendicular(), (1, -1))

    def test_angle_x(self):
        self.assertEqual(Vector(0, 0).angle_x, 0)
        self.assertEqual(Vector(4, 0).angle_x, 0)
        self.assertEqual(Vector(-4, 0).angle_x, 180)
        self.assertEqual(Vector(0, 2).angle_x, 90)
        self.assertEqual(Vector(0, -2).angle_x, -90)
        self.assertEqual(Vector(3, 3).angle_x, 45)

    def test_angle(self):
        self.assertEqual(Vector(0, 3).angle(Vector(2, 0)), -90)
        self.assertEqual(Vector(2, 0).angle(Vector(0, 3)), 90)
        self.assertEqual(Vector(3, 3).angle(Vector(-3, 3)), 90)

    def test_from_angle(self):
        self.assertEqual(Vector.from_angle_x(0), (1, 0))
        result = Vector.from_angle_x(90, length=5)
        self.assertAlmostEqual(result.x, 0)
        self.assertAlmostEqual(result.y, 5)

    def test_copy(self):
        v = Vector(2.5, -1)
        self.assertEqual(v, Vector(v))
