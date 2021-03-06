''' Routely tests '''
# Packages
import numpy as np
import pandas as pd
import pytest
from routely import Route

# with pytest-cov: pytest --cov=routely tests/

def _setup():
    x = [0, 5, 15, 20, 10]
    y = [0, 10, 40, 10, 5]
    z = {'foo':[0, 10, 40, 10, 5]}
    return Route(x, y, z=z)


def test_check_inputlengths():
    x = [1, 2, 3, 4]
    y = [4, 5, 6]
    with pytest.raises(ValueError):
        Route(x, y)

    x = [1, 2, 3]
    y = [4, 5, 6, 7]
    with pytest.raises(ValueError):
        Route(x, y)

    x = [1]
    y = [4, 5, 6, 7]
    with pytest.raises(ValueError):
        Route(x, y)

    x = [1, 2, 3, 4]
    y = [4]
    with pytest.raises(ValueError):
        Route(x, y)

    x = [1, 2, 3, 4]
    y = [4, 5, 6, 7]
    z = {'foo': [8, 9]}
    with pytest.raises(ValueError):
        Route(x, y, z=z)


def test_check_inputvalues():
    x = [1, 2, '3']
    y = [4, 5, 6]
    with pytest.raises(TypeError):
        Route(x, y)

    x = [1, 2, 3]
    y = [4, '5', 6]
    with pytest.raises(TypeError):
        Route(x, y)

    x = [1, 2, 3, 4]
    y = [4, 5, 6, 7]
    z = {'foo': [8, '9', 10, 11]}
    with pytest.raises(TypeError):
        Route(x, y, z=z)

def test_dataframe():
    r = _setup()
    df = pd.DataFrame({
        'x':r.x,
        'y':r.y,
        'd':r.d,
        'foo':r.z['foo']
    })

    assert df.astype(float).equals(r.dataframe().astype(float))


def test_nr_points():
    r = _setup()
    assert len(r.x) == r.nr_points()


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
    r2 = r.interpolate(kind='equidistant_steps', num=num)

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
    r2 = r.interpolate(kind='absolute_steps', num=num)

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

#     r2 = r.smooth(0.9)

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
    route_copy = route_copy.align_to_origin(origin=(10, 10))

    # compare x and y
    assert list(route_copy.x) != list(r.x)
    assert list(route_copy.y) != list(r.y)


def test_center_on_origin():
    r1 = _setup()

    r3 = r1.center_on_origin(new_origin=(0, 0))

    assert (0, 0) == r3.center()
    assert r1.size() == r3.size()
    assert r1.nr_points() == r3.nr_points()
    assert r1.center() != r3.center()


def test_align_to_origin():
    r1 = _setup()
    r2 = _setup()

    r3 = r1.align_to_origin(align_corner='bottomleft')

    assert (0, 0) != r3.center()
    assert r1.size() == r3.size()
    assert r1.nr_points() == r3.nr_points()
    assert (0, 0) == r1.bbox()[0]

    r3 = r1.align_to_origin(align_corner='topright')

    assert (0, 0) != r3.center()
    assert r1.size() == r3.size()
    assert r1.nr_points() == r3.nr_points()
    assert (0, 0) == r3.bbox()[1]

    r3 = r1.align_to_origin(align_corner='bottomright')

    assert (0, 0) != r3.center()
    assert r1.size() == r3.size()
    assert r1.nr_points() == r3.nr_points()
    assert (0, 0) == (r3.bbox()[1][0], r3.bbox()[0][1])

    r3 = r1.align_to_origin(align_corner='topleft')

    assert (0, 0) != r3.center()
    assert r1.size() == r3.size()
    assert r1.nr_points() == r3.nr_points()
    assert (0, 0) == (r3.bbox()[0][0], r3.bbox()[1][1])


def test_plotroute():
    r = _setup()
    plot = r.plotroute()
    plot_xdata = plot.lines[0].get_xdata()
    plot_ydata = plot.lines[0].get_ydata()

    assert list(r.x) == list(plot_xdata)
    assert list(r.y) == list(plot_ydata)


def test_plot_z():
    r = _setup()
    plot = r.plot_z()
    plot_xdata = plot.lines[0].get_xdata()
    plot_ydata = plot.lines[0].get_ydata()

    assert list(r.d) == list(plot_xdata)
    assert list(r.z['foo']) == list(plot_ydata)


def test_clean_coordinates():
    #idx 0, 1, 2, 3, 4, 5, 6, 7, 8
    #    0, 1, x, 3, 4, 5, x, x, x, x --> any
    #    0, 1, x, 3, 4, 5, 6, x, x, 9 --> consecutive
    x = [0, 1, 1, 2, 3, 4, 3, 3, 3, 4]
    y = [1, 2, 2, 3, 4, 4, 4, 4, 4, 4]
    z = [8, 7, 6, 5, 4, 3, 2, 1, 0, 0]

    # test duplicates='any'
    r = Route(x, y, z={'foo':z})

    r2 = r.clean_coordinates(duplicates='any')

    expected_x = [0, 1, 2, 3, 4]
    expected_y = [1, 2, 3, 4, 4]
    expected_z = [8, 7, 5, 4, 3]

    # new object
    assert expected_x == list(r2.x)
    assert expected_y == list(r2.y)
    assert expected_z == list(r2.z['foo'])

    # test duplicates='consecutive'
    r = Route(x, y, z={'foo':z})

    r2 = r.clean_coordinates(duplicates='consecutive')

    #             0, 1, x, 3, 4, 5, 6, x, 8 --> consecutive
    expected_x = [0, 1, 2, 3, 4, 3, 4]
    expected_y = [1, 2, 3, 4, 4, 4, 4]
    expected_z = [8, 7, 5, 4, 3, 2, 0]

    # new object
    assert expected_x == list(r2.x)
    assert expected_y == list(r2.y)
    assert expected_z == list(r2.z['foo'])


def test_rotate():
    x = [0, 0, 0, 0, 0]
    y = [-2, -1, 0, 1, 2]
    r1 = Route(x, y)

    r2 = r1.rotate(90)
    x_exp = [-2, -1, 0, 1, 2]
    y_exp = [0, 0, 0, 0, 0]

    assert x_exp == list(r2.x)
    assert y_exp == pytest.approx(list(r2.y), rel=0.1)
