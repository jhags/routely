''' Routely '''

import math

import matplotlib.pyplot as plt
import numpy as np

from matplotlib.ticker import MultipleLocator
from scipy.interpolate import UnivariateSpline, interp1d


class Route:
    """
    Create a Route.

    Description
    -----------
    Route is designed to provide many of the common route operations and transformations to make route processing simpler and quicker.

    A route is represented by a series of point coordinates on a two dimensional x-y plane. Z-axis data can be specified as well, however the primary focus of these common transformations are based on the x-y plane data with z-axis data being transformed accordingly.

    The primary focus is on x-y plane data because z-axis data does not have to represent a path through three dimensional space, rather z-data can represent additonal layers of route data that correspond to the x-y path.

    For example, a runner may be tracking pace or heartrate, a car will have changes in speed, etc. Therefore, transformations are primarily concerned with the x-y route taken.

    Args:
    -----
        x (array-like) : List or array of x-coordinates of the route.

        y (array-like) : List or array of y-coordinates of the route.

        z (dict {key:array-like}, optional) : List or array of z data for the route. This does not need to be elevation, but any data corresponding to the route in the x-y plane. Defaults to None.
    """

    def __init__(self, x, y, z=None):

        self.x = x
        self.y = y
        self.z = z

        self._prep_inputs()

        self._check_inputs()

        self.d = self._calculate_distance()


    def _prep_inputs(self):
        """Convert args to array if not none.
        """
        if self.x is not None:
            self.x = np.array(self.x)

        if self.y is not None:
            self.y = np.array(self.y)

        if self.z is not None:
            for k in self.z.keys():
                self.z[k] = np.array(self.z[k])


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
            for v in self.z.values():
                assert (len(v) == len_x), "Route input 'z' must be of equal length to 'x' and 'y'"
                assert (v.dtype in [np.int, np.float]), "Route input 'x' must be either int or float dtypes"


    def route(self):
        """
        Returns route data in list form -> [(x, y, z, distance)]. z will be included if specified as an input arguement.
        """
        if self.z is not None:
            return list(zip(self.x, self.y, self.z, self.d))
        else:
            return list(zip(self.x, self.y, self.d))


    def bbox(self):
        """Get the bounding box coordinates of the route.

        Returns:
            tuple: (lower-left corner coordinates, upper-right corner coordinates).
        """
        lower = (self.x.min(), self.y.min())
        upper = (self.x.max(), self.y.max())
        return (lower, upper)


    def width(self):
        """Get the width of the route (from min x to max x).

        Returns:
            float: route width.
        """
        return self.x.max() - self.x.min()


    def height(self):
        """Get the height of the route (from min y to max y).

        Returns:
            float: route height.
        """
        return self.y.max() - self.y.min()


    def size(self):
        """Returns the width and height (w, h) of the route along the x and y axes.

        Returns:
            tuple: (width, height)
        """
        return (self.width(), self.height())


    def center(self):
        """Get the center point of the route as defined as the mid-point between the max and min extents on each axis.

        Returns:
            tuple: (x, y) coordinates of the route center point
        """
        xc = (self.x.max() + self.x.min())/2.
        yc = (self.y.max() + self.y.min())/2.
        return (xc, yc)


    def nr_points(self):
        """Get the number of coordinate points that comprise the route.

        Returns:
            float: number of coordinates.
        """
        return len(self.x)

    # TODO: close off the route
    # def close_off_route(self):
    #     """Close off the route by ensuring the first and last coordinates are equal.
    #     """

    #     return


    def plotroute(self, markers=True, equal_aspect=True, equal_lims=True):
        """Plot the route (x vs y).

        Args:
            markers (bool, optional): Choose to display markers. Defaults to True.
            equal_aspect (bool, optional): Choose to maintain an equal aspect ration in the plot. Defaults to True.
            equal_lims (bool, optional): Choose to display equal x and y limits. Defaults to True.
        """

        if markers:
            marker = 'o'
        else:
            marker = None

        fig, ax = plt.subplots()
        ax.plot(self.x, self.y, 'k', marker=marker)

        fig.tight_layout()

        if equal_aspect:
            ax.set_aspect('equal', 'box')

        # Set equal lims if chosen. If not, let matplotlib set lims automatically
        if equal_lims:
            # Determine plot limits centered on the route center point
            c = self.center()
            lim = round((max(self.size())/2) * 1.1, 0) # add approx 10% to the lims
            x_lim = [c[0] - lim, c[0] + lim]
            y_lim = [c[1] - lim, c[1] + lim]

            # Set lims on plot
            ax.set_xlim(x_lim)
            ax.set_ylim(y_lim)

        # Axis formating
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.grid(True)


    def plot_z(self, markers=True):
        """Plot Route z-data (d vs z).

        Args:
            markers (bool, optional): Choose to display markers. Defaults to True.
        """

        # Check is z data is present
        if self.z is None:
            print('No z data provided')
            return

        if markers:
            marker = 'o'
        else:
            marker = None

        nr_plots = len(self.z)

        fig, _ = plt.subplots(nr_plots, sharex=True)

        # Use enumerate on fig which works with one axes or multiple axes
        for idx, ax in enumerate(fig.axes):
            # data and corersponding label
            label = list(self.z.keys())[idx]
            z_data = list(self.z.values())[idx]

            # Plot data and label
            ax.plot(self.d, z_data, 'k', marker=marker)
            ax.set(xlabel='d', ylabel=label)
            ax.grid(True)
            ax.label_outer()

        fig.tight_layout()


    def _calculate_distance(self):
        """Calculate cumulative distance given Route x and y coordinates lists.

        Returns:
            array: 1d array of cumulative distance from the start of the Route to the end.
        """
        xy = list(zip(self.x, self.y))

        dist = [0]
        for i in range(1, len(xy)):
            dist.append(self.distance_between_two_points(xy[i-1], xy[i]))

        return np.array(dist).cumsum()


    @staticmethod
    def distance_between_two_points(p1, p2):
        """Calulate the Euclidean distance between two (x, y) points.

        Args:
            p1 (tuple): (x, y) tuple of the first point
            p2 (tuple): (x, y) tuple of the second point

        Returns:
            float: distance between point 1 and point 2
        """
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


    def interoplate(self, kind='equidistant_steps', num=1, inplace=False):
        """
        Interpolate Route x and y coordinate lists given various interpolation stategies.


        Available strategies include (specify chosen strategy in 'kind' args):
        > 'equidistant_Steps': equally spaced steps along the route path from start to end, using np.arange(). Step spacing specified by 'num' arg. This is not equidistant steps along x or y axis but distance along the path ie between route waypoints. Note: some variation in steps may occur in order to coincide with existing x and y coordinates.

        > 'absolute_steps': the total number of points along the full route as specified by 'num' arg. The spacing of the points will be linear along the length of the route using np.linspace.

        > 'cubic': cubic interpolation uses the same method as 'absolute_steps' to linearly space a chosen number of points, but uses a cubic formula to smooth the route as well.

        Note, in all cases, the total route distance may vary from the original but the start and end coordinates will remain the same.

        Args:
            kind (str, optional): See docs for options. Defaults to 'equidistant_steps'.
            num (int, optional): step value corresponding to chosen 'kind' of interpolation. Defaults to 1.
            inplace (bool, optional): If True, modify Route attributes in place. If False, return a new Route object. Defaults to False.

        Returns:
            Route: Return a new Route object if inplace is False.
        """
        x = self.x
        y = self.y
        d = self.d

        # cubic requires a different calculation, so check the kind first
        if (kind == 'equidistant_steps') | (kind == 'absolute_steps'):
            if kind == 'equidistant_steps':
                # New list of distance points to interpolate Route data against
                dist = list(np.arange(d.min(), d.max()+num, step=num))

            elif kind == 'absolute_steps':
                # New list of distance points to interpolate Route data against
                dist = list(np.linspace(d.min(), d.max(), num=num))

            # Interpolate x and y wrt to d against the new list of distanced points
            xx = np.interp(dist, d, x)
            yy = np.interp(dist, d, y)

            # interpolate z too if it exists
            if self.z is not None:
                # Start a new dict of z-axis data
                zz = {}
                # for each, interpolate and add to the new dict
                for k, v in self.z.items():
                    zz[k] = np.interp(dist, d, v)
            else:
                zz = None

        # for cubic method only
        elif kind == 'cubic':
            # Use linspace to get a new list of distanced points
            dist = np.linspace(d.min(), d.max(), num=num)

            # interpolation functions for x and y wrt to d
            fx = interp1d(d, x, kind='cubic')
            fy = interp1d(d, y, kind='cubic')

            # apply function to distanced points
            xx, yy = fx(dist), fy(dist)

            # repeat for z if it exists
            if self.z is not None:
                zz = {}
                for k, v in self.z.items():
                    fz = interp1d(d, v, kind='cubic')
                    zz[k] = fz(dist)
            else:
                zz = None

        else:
            raise Exception ("Keyword argument for 'kind' not recognised. Please choose one of 'equidistant_steps', 'absolute_steps', or 'cubic'")

        if inplace:
            self.x = xx
            self.y = yy
            self.d = np.array(dist)
            self.z = zz

        elif inplace is False:
            return Route(xx, yy, z=zz)

    # TODO: Add Univariate Spline
    # def add_spline(self):

    #     return


    def center_on_origin(self, new_origin=(0, 0), inplace=False):
        """Translate the Route to the origin, where the Route center point will be equal to the origin.

        Args:
            new_origin (tuple, optional): New Route origin, which will correspond to the Route's center point. Defaults to (0, 0).
            inplace (bool, optional): If True, modify Route attributes in place. If False, return a new Route object. Defaults to False.

        Returns:
            Route: Return a new Route object if inplace is False.
        """
        center = self.center()

        # translate x and y
        x_new = self.x - center[0] + new_origin[0]
        y_new = self.y - center[1] + new_origin[1]

        if inplace:
            self.x = np.array(x_new)
            self.y = np.array(y_new)
            self.d = self._calculate_distance()
        else:
            return Route(x_new, y_new)


    def align_to_origin(self, origin=(0, 0), align_corner='bottomleft', inplace=False):
        """Align a corner of Route extents to the origin.

        Args:
            origin (tuple, optional): Route origin to align a chosen corner to. Defaults to (0, 0).
            align_corner (str, optional): Choose a corner to align. Options: 'bottomleft', 'bottomright', 'topleft', 'topright'. Defaults to 'bottomleft'.
            inplace (bool, optional): If True, modify Route attributes in place. If False, return a new Route object. Defaults to False.

        Returns:
            Route: Return a new Route object if inplace is False.
        """
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
            self.d = self._calculate_distance()
        else:
            return Route(x_new, y_new)


    @staticmethod
    def _rotate_point(origin, point, angle):
        """Rotate a point counterclockwise by a given angle around a given origin.

        Args:
            origin (tuple): (x, y) point about which to rotate the point
            point (tuple): (x, y) point to rotate
            angle (float): angle to rotate point. The angle should be given in radians.

        Returns:
            tuple: (x, y) coordinates of rotated point
        """

        ox, oy = origin
        px, py = point

        qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
        qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
        return qx, qy


    def rotate(self, angle_deg, inplace=False):
        """Rotate Route x and y coordinates clockwise for a given angle in degrees. This does not modify z-axis data.

        Args:
            angle_deg (float): angle of rotation in degrees.
            inplace (bool, optional): If True, modify Route attributes in place. If False, return a new Route object. Defaults to False.

        Returns:
            Route: Return a new Route object if inplace is False.
        """
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
            self.d = self._calculate_distance()
        else:
            return Route(x_new, y_new)


    def mirror(self, about_x=False, about_y=False, about_axis=False, inplace=False):
        """Mirror Route x and y coordinates in the x and y planes as may be specified.

        Args:
            about_x (bool, optional): If True, mirror Route horizontally. Defaults to False.
            about_y (bool, optional): If True, mirror Route vertically. Defaults to False.
            about_axis (bool, optional): If True, mirror Route about the x or y axis. If False, mirror Route about the Route's center point. Defaults to False.
            inplace (bool, optional): If True, modify Route attributes in place. If False, return a new Route object. Defaults to False.

        Returns:
            Route: Return a new Route object if inplace is False.
        """
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
            self.d = self._calculate_distance()
        else:
            return Route(x_new, y_new)


    def fit_to_box(self, box_width, box_height, keep_aspect=True, inplace=False):
        """Scale the Route to fit within a specified bounding box of given width and height. This modifies the x, y and d Route attributes.

        Args:
            box_width (float): Desired width.
            box_height (float): Desired height.
            keep_aspect (bool, optional): If True, the route will be scalled equal in both x and y directions ensuring the new route will fit within the smallest extent. If False, x and y coordinates will be scalled independently such that the modified route will fill the specified width and height. Note: this modifies the aspect ratio of the route. Defaults to True.
            inplace (bool, optional): If True, modify Route attributes in place. If False, return a new Route object. Defaults to False.

        Returns:
            Route: Return a new Route object if inplace is False.
        """
        #Scale factors for width and height
        if keep_aspect:
            sfactor = max(self.height()/box_height, self.width()/box_width)
            sfactor_x = sfactor
            sfactor_y = sfactor

        elif keep_aspect is False:
            sfactor_x = abs(self.width()/box_width)
            sfactor_y = abs(self.height()/box_height)

        # scale x and y
        x_new = self.x/sfactor_x
        y_new = self.y/sfactor_y

        if inplace:
            self.x = np.array(x_new)
            self.y = np.array(y_new)
            self.d = self._calculate_distance()
        else:
            return Route(x_new, y_new)


    def optimise_bbox(self, box_width, box_height, inplace=False):
        """Rotate the route to the most efficient use of space given the width and height of a bounding box. This does not scale the route to fill the space but rather find the best aspect ratio of the route that best matches that of the specified box width and height.

        The route is rotated 90 degrees clockwise in steps of one degree about the route's center point.

        Args:
            box_width (float): box width.
            box_height (float): box height.
            inplace (bool, optional): If True, modify Route attributes in place. If False, return a new Route object. Defaults to False.

        Returns:
            Route: Return a new Route object if inplace is False.
        """
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
