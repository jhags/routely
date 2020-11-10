''' Routely tests '''
# Packages
import numpy as np
import unittest
from routely.routely import Route


class routely_test(unittest.TestCase):

    def test_distance_between_two_points(self):
        p1 = (0, 0)
        p2 = (3, 4)

        output = Route.distance_between_two_points(p1, p2)
        self.assertEqual(output, 5)

    def test_calculate_distance(self):
        x = [0, 7.5, 15, 22.5, 30]
        y = [0, 0, 0, 0, 0]
        r = Route(x, y)

        output = np.diff(np.array(r.d))
        self.assertEqual(7.5, output[0])

        x = [0, 3, 6, 9, 12]
        y = [0, 4, 8, 12, 16]
        r = Route(x, y)

        output = np.diff(np.array(r.d))
        self.assertEqual(5, output[0])
