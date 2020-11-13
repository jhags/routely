''' Routely '''

import math

import matplotlib.pyplot as plt
import numpy as np

from matplotlib.ticker import MultipleLocator
from scipy.interpolate import UnivariateSpline, interp1d, interp2d


class Route:
    """
    Create a Route.

    Description
    -----------
    Route is designed to provide many of the common route operations and transformations to make route processing simpler and quicker.

    A route is represented by a series of point coordinates on a two dimensional x-y plane. Z-axis data can be specified as well, however the primary focus of these common transformations are based on the x-y plane data with z-axis data being transformed accordingly.

    The primary focus is on x-y plane data because z-axis data does not have to represent a path through three dimensional space, rather z-data can represent additonal layers of route data that correspond to the x-y path.

    For example, a runner may be tracking pace or heartrate, a car will have changes in speed, etc. Therefore, transformations are primarily concerned with the x-y route taken.

    Args
    ----
    x (array-like) : List or array of x-coordinates of the route.

    y (array-like) : List or array of y-coordinates of the route.

    z (array-like, optional) : List or array of z data for the route. This does not need to be elevation, but any data corresponding to the route in the x-y plane. Defaults to None.
    """

    def __init__(self, x, y, z=None, z_labels=None):
        self.x = x
        self.y = y
        self.z = z
        self.z_labels = z_labels

        self._prep_inputs()

        self._check_inputs()

        self.d = self._calculate_distance()

    def _prep_inputs(self):
        if self.x is not None:
            self.x = np.array(self.x)

        if self.y is not None:
            self.y = np.array(self.y)

        if self.z is not None:
            self.z = np.array(self.z)

        if self.z_labels is not None:
            self.z_labels = np.array(self.z_labels)


    def _check_inputs(self):
        """
        Check Route argument inputs and raise exceptions where necessary.
        """

        len_x, len_y = len(self.x), len(self.y)

        # Check x and y have more than 1 item
        assert (len_x > 1), "Route input 'x' must contain more than 1 item"
        assert (len_y > 1), "Route input 'y' must contain more than 1 item"

        # Check x and y are equal length
        assert (len_x == len_y), "Route inputs 'x' and 'y' must be of equal length"

        # Check x, y and z are int or float dtypes
        # ie do not contain any unusable values like strings
        assert (self.x.dtype in [np.int, np.float]), "Route input 'x' must be either int or float dtypes"
        assert (self.y.dtype in [np.int, np.float]), "Route input 'x' must be either int or float dtypes"

        # Performs checks on z if not empty
        if self.z is not None:
            assert (self.z.shape[-1] == len_x), "Route input 'z' must be of equal length to 'x' and 'y'"
            assert (self.z.dtype in [np.int, np.float]), "Route input 'x' must be either int or float dtypes"
            assert (self.z_labels.shape[-1] == self.z.shape[0]), "Route input 'z_labels' length must match 'z' shape"

    def route(self):
        """
        Returns route data in list form -> [(x, y, z, distance)]. z will be included if specified as an input arguement.
        """
        if self.z is not None:
            return list(zip(self.x, self.y, self.z, self.d))
        else:
            return list(zip(self.x, self.y, self.d))


    def bbox(self):
        lower = (self.x.min(), self.y.min())
        upper = (self.x.max(), self.y.max())
        return (lower, upper)


    def width(self):
        return self.x.max() - self.x.min()


    def height(self):
        return self.y.max() - self.y.min()


    def size(self):
        """
        Returns the width and height (w, h) of the route along the x and y axes.
        """
        return (self.width(), self.height())


    def center(self):
        xc = (self.x.max() + self.x.min())/2.
        yc = (self.y.max() + self.y.min())/2.
        return (xc, yc)


    def nr_points(self):
        return len(self.x)


    def close_off_route(self):

        return


    def plotroute(self, markers=True):
        x = self.x
        y = self.y

        if markers:
            marker = 'o'
        else:
            marker = None

        c = self.center()
        lim = round((max(self.size())/2) * 1.1, 0)
        x_lim = [c[0] - lim, c[0] + lim]
        y_lim = [c[1] - lim, c[1] + lim]

        fig, ax = plt.subplots()
        ax.plot(x, y, 'k', marker=marker)

        fig.tight_layout()

        ax.set_aspect('equal', 'box')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_xlim(x_lim)
        ax.set_ylim(y_lim)
        ax.grid(True)

    def plot_z(self, markers=True):
        if self.z is None:
            print('No z data provided')

        if markers:
            marker = 'o'
        else:
            marker = None

        nr_plots = self.z.shape[0]

        fig, axs = plt.subplots(nr_plots, sharex=True)

        for idx, z_data in enumerate(self.z):
            axs[idx].plot(self.d, z_data, 'k', marker=marker)
            axs[idx].set(xlabel='d', ylabel=self.z_labels[idx])
            axs[idx].grid(True)
            axs[idx].label_outer()

        fig.tight_layout()


    def _calculate_distance(self):
        xy = list(zip(self.x, self.y))

        dist = [0]
        for i in range(1, len(xy)):
            dist.append(self.distance_between_two_points(xy[i-1], xy[i]))

        return np.array(dist).cumsum()


    @staticmethod
    def distance_between_two_points(p1, p2):
        """[summary]

        Args:
            p1 ([type]): [description]
            p2 ([type]): [description]

        Returns:
            [type]: [description]
        """
        ''' distance between two points (tuples) '''
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


    def interoplate(self, kind='equidistant_steps', num=1, inplace=False):
        """[summary]

        Args:
            kind (str, optional): Please choose one of 'steps', 'linear, or 'cubic'. Defaults to 'steps'.
            num (int, optional): [description]. Defaults to 1.
            inplace (bool, optional): [description]. Defaults to False.

        Raises:
            Exception: [description]

        Returns:
            [type]: [description]
        """
        x = self.x
        y = self.y
        d = self.d

        if (kind == 'equidistant_steps') | (kind == 'absolute_steps'):
            if kind == 'equidistant_steps':
                dist = list(np.arange(d.min(), d.max()+num, step=num))

            elif kind == 'absolute_steps':
                dist = list(np.linspace(d.min(), d.max(), num=num))

            xx = np.interp(dist, d, x)
            yy = np.interp(dist, d, y)

            if self.z is not None:
                zz = np.interp(dist, d, self.z)
            else:
                zz = None

        elif kind == 'cubic':
            dist = np.linspace(d.min(), d.max(), num=num)

            fx = interp1d(d, x, kind='cubic')
            fy = interp1d(d, y, kind='cubic')

            xx, yy = fx(dist), fy(dist)

            if self.z is not None:
                fz = interp1d(d, self.z, kind='cubic')
                zz = fz(dist)
            else:
                zz = None

        else:
            raise Exception ("Keyword argument for 'kind' not recognised. Please choose one of 'equidistant_steps', 'absolute_steps', or 'cubic'")

        if inplace:
            self.x = xx
            self.y = yy
            self.d = dist
            self.z = zz

        elif inplace is False:
            return Route(xx, yy, z=zz)


    def add_spline(self):

        return


    def center_on_origin(self, new_origin=(0, 0), inplace=False):
        center = self.center()

        # scale x and y
        x_new = self.x - center[0] + new_origin[0]
        y_new = self.y - center[1] + new_origin[1]

        if inplace:
            self.x = np.array(x_new)
            self.y = np.array(y_new)
        else:
            return Route(x_new, y_new)


    def align_to_origin(self, origin=(0, 0), align_corner='bottomleft', inplace=False):
        # Options: bottomleft, bottomright, topleft, topright

        if align_corner == 'bottomleft':
            corner = self.bbox()[0]

        elif align_corner == 'topright':
            corner = self.bbox()[1]

        elif align_corner == 'bottomright':
            corner = (self.bbox()[1][0], self.bbox()[0][1])

        elif align_corner == 'topleft':
            corner = (self.bbox()[0][0], self.bbox()[1][1])

        else:
            raise Exception ("Keyword argument for 'align_corner' not recognised. Please choose one from 'bottomleft', 'bottomright', 'topleft', 'topright'.")

        # scale x and y
        x_new = self.x - corner[0] + origin[0]
        y_new = self.y - corner[1] + origin[1]

        if inplace:
            self.x = np.array(x_new)
            self.y = np.array(y_new)
        else:
            return Route(x_new, y_new)
        return


    @staticmethod
    def _rotate_point(origin, point, angle):
        # Rotate a point counterclockwise by a given angle around a given origin.
        # The angle should be given in radians.

        ox, oy = origin
        px, py = point

        qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
        qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
        return qx, qy


    def rotate(self, angle_deg, inplace=False):
        xy = list(zip(self.x, self.y))
        c = self.center()
        rad = -math.radians(angle_deg)

        x_new = []
        y_new = []
        for x, y in xy:
            p = self._rotate_point(c, (x, y), rad)
            x_new.append(p[0])
            y_new.append(p[1])

        if inplace:
            self.x = np.array(x_new)
            self.y = np.array(y_new)
        else:
            return Route(x_new, y_new)


    def mirror(self, about_x=False, about_y=False, about_axis=False, inplace=False):

        if about_axis:
            c = (0, 0)
        elif about_axis is False:
            c = self.center()

        if about_y:
            x_new = []
            for p in self.x:
                x_new.append(c[0] + (c[0] - p))
        else:
            x_new = self.x

        if about_x:
            y_new = []
            for p in self.y:
                y_new.append(c[1] + (c[1] - p))
        else:
            y_new = self.y

        if inplace:
            self.x = np.array(x_new)
            self.y = np.array(y_new)
        else:
            return Route(x_new, y_new)


    def fit_to_box(self, box_width, box_height, inplace=False):

        #Scale factors for width and height?
        sfactor = max(self.height()/box_height, self.width()/box_width)

        # scale x and y
        x_new = self.x/sfactor
        y_new =  self.y/sfactor

        if inplace:
            self.x = np.array(x_new)
            self.y = np.array(y_new)
        else:
            return Route(x_new, y_new)


    def optimise_bbox(self, box_width, box_height, inplace=False):

        target = box_width/box_height

        angles = []
        spatial_eff = [] # spatial efficiency
        for angle in np.arange(0, 91, 1):
            r_rotated = self.rotate(angle)
            spatial_ratio = abs(r_rotated.width()/r_rotated.height())

            angles.append(angle)
            spatial_eff.append(abs(spatial_ratio - target))

        angles = np.array(angles)
        spatial_eff = np.array(spatial_eff)

        idx = spatial_eff.argmin()
        angle = angles[idx]

        return self.rotate(angle, inplace=inplace)
