import unittest
from math import pi

from src.area_calculator import Circle, Triangle, TriangleType


class TestGeometry(unittest.TestCase):
    def test_circle_area(self):
        circle = Circle(5)
        self.assertAlmostEqual(circle.area(), pi * 5 ** 2, delta=0.001)

    def test_triangle_area(self):
        triangle = Triangle(3, 4, 5)
        self.assertAlmostEqual(triangle.area(), 6.0, delta=0.001)

    def test_negative_radius_circle(self):
        with self.assertRaises(ValueError):
            Circle(-1)

    def test_negative_side_length_triangle(self):
        with self.assertRaises(ValueError):
            Triangle(-3, 4, 5)

    def test_right_triangle_check(self):
        triangle = Triangle(3, 4, 5)
        self.assertTrue(TriangleType.is_right_triangle(triangle))


if __name__ == '__main__':
    unittest.main()
