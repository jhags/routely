''' Routely tests '''
# Packages
import numpy as np
import pytest
from routely import Route

def _setup():
    x = [0, 5, 15, 20, 10]
    y = [0, 10, 40, 10, 5]
    z = {'foo':[0, 10, 40, 10, 5]}
    return Route(x, y, z=z)


def test_distance_between_two_points():
    p1 = (0, 0)
    p2 = (3, 4)

    output = Route.distance_between_two_points(p1, p2)
    assert output == 5


def test_calculate_distance():
    x = [0, 7.5, 15, 22.5, 30]
    y = [0, 0, 0, 0, 0]
    r = Route(x, y)

    output = np.diff(np.array(r.d))
    assert 7.5 == output[0]

    x = [0, 3, 6, 9, 12]
    y = [0, 4, 8, 12, 16]
    r = Route(x, y)

    output = np.diff(np.array(r.d))
    assert 5 == output[0]


def test_bbox():
    r = _setup()
    bbox = r.bbox()
    assert ((0, 0), (20, 40)) == bbox


def test_width_height_size():
    r = _setup()
    width = r.width()
    assert 20 == width

    height = r.height()
    assert 40 == height

    size = (width, height)
    assert (20, 40) == size


def test_center():
    r = _setup()
    center = r.center()
    assert (10, 20) == center


def test_interpolate_steps():
    r = _setup()
    num = 2
    r2 = r.interoplate(kind='equidistant_steps', num=num, inplace=False)

    # check start and end coords
    r1_start_coord = (r.x[0], r.y[0])
    r2_start_coord = (r2.x[0], r2.y[0])
    assert r1_start_coord == r2_start_coord

    r1_end_coord = (r.x[-1], r.y[-1])
    r2_end_coord = (r2.x[-1], r2.y[-1])
    assert r1_end_coord == r2_end_coord

    # check change in step
    assert num == pytest.approx(np.diff(r2.d)[0], 0.01)

    # check number of points in interpolated list
    expected_nr_points = 1 + (r.d[-1] + num)//num
    assert expected_nr_points == len(r2.d)

def test_interpolate_linear():
    r = _setup()
    num = 20
    r2 = r.interoplate(kind='absolute_steps', num=num, inplace=False)

    # check start and end coords
    r1_start_coord = (r.x[0], r.y[0])
    r2_start_coord = (r2.x[0], r2.y[0])
    assert r1_start_coord == r2_start_coord

    r1_end_coord = (r.x[-1], r.y[-1])
    r2_end_coord = (r2.x[-1], r2.y[-1])
    assert r1_end_coord == r2_end_coord

    # check number of points in interpolated list
    assert 20 == len(r2.d)


# def test_interpolate_cubic():

#     r2 = r.smooth(0.9, inplace=False)

#     # check start and end coords
#     r1_start_coord = (r.x[0], r.y[0])
#     r2_start_coord = (r2.x[0], r2.y[0])
#     assert (r1_start_coord, r2_start_coord)

#     r1_end_coord = (r.x[-1], r.y[-1])
#     r2_end_coord = (r2.x[-1], r2.y[-1])
#     assert (r1_end_coord, r2_end_coord)


def test_copy():
    r = _setup()

    # Take a copy
    route_copy = r.copy()

    # modify that copy
    route_copy.align_to_origin(origin=(10, 10), inplace=True)

    # compare x and y
    assert list(route_copy.x) != list(r.x)
    assert list(route_copy.y) != list(r.y)


def test_center_on_origin():
    r = _setup()
    r2 = r.center_on_origin(new_origin=(0, 0))

    assert (0, 0) == r2.center()
    assert r.size() == r2.size()
    assert r.nr_points() == r2.nr_points()
    assert r.center() != r2.center()
