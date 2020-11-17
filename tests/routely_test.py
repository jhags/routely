''' Routely tests '''
# Packages
import numpy as np
import unittest
from routely.routely import Route


class routely_test(unittest.TestCase):

    def setUp(self):
        self.x = [0, 5, 15, 20, 10]
        self.y = [0, 10, 40, 10, 5]
        self.z = {
            'foo':[0, 10, 40, 10, 5]
        }

        self.r = Route(self.x, self.y, z=self.z)


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

    # def test_check_inputs(self):
    #     x = [0, 1, '2']
    #     y = [3, 4, 5]
    #     Route(x, y)
        # self.assertRaises(ZeroDivisionError, Route, x, y)

    def test_bbox(self):
        bbox = self.r.bbox()
        self.assertEqual(((0, 0), (20, 40)), bbox)

    def test_width_height_size(self):
        width = self.r.width()
        self.assertEqual(20, width)

        height = self.r.height()
        self.assertEqual(40, height)

        size = (width, height)
        self.assertEqual((20, 40), size)

    def test_center(self):
        center = self.r.center()
        self.assertEqual((10, 20), center)

    def test_interpolate_steps(self):
        num = 2
        r2 = self.r.interoplate(kind='equidistant_steps', num=num, inplace=False)

        # check start and end coords
        r1_start_coord = (self.r.x[0], self.r.y[0])
        r2_start_coord = (r2.x[0], r2.y[0])
        self.assertEqual(r1_start_coord, r2_start_coord)

        r1_end_coord = (self.r.x[-1], self.r.y[-1])
        r2_end_coord = (r2.x[-1], r2.y[-1])
        self.assertEqual(r1_end_coord, r2_end_coord)

        # check change in step
        self.assertAlmostEqual(num, np.diff(r2.d)[0], 2)

        # check number of points in interpolated list
        expected_nr_points = 1 + (self.r.d[-1] + num)//num
        self.assertEqual(expected_nr_points, len(r2.d))

    def test_interpolate_linear(self):
        num = 20
        r2 = self.r.interoplate(kind='absolute_steps', num=num, inplace=False)

        # check start and end coords
        r1_start_coord = (self.r.x[0], self.r.y[0])
        r2_start_coord = (r2.x[0], r2.y[0])
        self.assertEqual(r1_start_coord, r2_start_coord)

        r1_end_coord = (self.r.x[-1], self.r.y[-1])
        r2_end_coord = (r2.x[-1], r2.y[-1])
        self.assertEqual(r1_end_coord, r2_end_coord)

        # check number of points in interpolated list
        self.assertEqual(20, len(r2.d))

    def test_interpolate_cubic(self):

        r2 = self.r.smooth(0.9, inplace=False)

        # check start and end coords
        r1_start_coord = (self.r.x[0], self.r.y[0])
        r2_start_coord = (r2.x[0], r2.y[0])
        self.assertEqual(r1_start_coord, r2_start_coord)

        r1_end_coord = (self.r.x[-1], self.r.y[-1])
        r2_end_coord = (r2.x[-1], r2.y[-1])
        self.assertEqual(r1_end_coord, r2_end_coord)


    def test_copy(self):

        # Take a copy
        route_copy = self.r.copy()

        # modify that copy
        route_copy.align_to_origin(origin=(10, 10), inplace=True)

        # compare x and y
        self.assertNotEqual(list(route_copy.x), list(self.r.x))
        self.assertNotEqual(list(route_copy.y), list(self.r.y))