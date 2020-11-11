''' Routely '''

import math

import matplotlib.pyplot as plt
import numpy as np

from matplotlib.ticker import MultipleLocator
from scipy.interpolate import UnivariateSpline, interp1d, interp2d


class Route:

    def __init__(self, x=None, y=None):
        self.x = np.array(x)
        self.y = np.array(y)
        self.d = self.calculate_distance()


    def check_inputs(self):
        # check is list
        # check list has more than 1
        # check x and y equal length
        return


    def route(self):
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
        '''Width and height of the route from min to max'''
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


    def calculate_distance(self):
        xy = list(zip(self.x, self.y))

        dist = [0]
        for i in range(1, len(xy)):
            dist.append(self.distance_between_two_points(xy[i-1], xy[i]))

        return np.array(dist).cumsum()


    @staticmethod
    def distance_between_two_points(p1, p2):
        ''' distance between two points (tuples) '''
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


    def interoplate(self, kind='steps', num=1, inplace=False):
        x = self.x
        y = self.y
        d = self.d

        if (kind == 'steps') | (kind == 'linear'):
            if kind == 'steps':
                dist = list(np.arange(d.min(), d.max()+num, step=num))

            elif kind == 'linear':
                dist = list(np.linspace(d.min(), d.max(), num=num))

            xx = np.interp(dist, d, x)
            yy = np.interp(dist, d, y)

        elif kind == 'cubic':
            dist = np.linspace(d.min(), d.max(), num=num)

            fx = interp1d(d, x, kind='cubic')
            fy = interp1d(d, y, kind='cubic')

            xx, yy = fx(dist), fy(dist)

        else:
            raise Exception ("Keyword argument for 'kind' not recognised. Please choose one of 'steps', 'linear, or 'cubic'.")

        if inplace:
            self.x = xx
            self.y = yy
            self.d = dist

        elif inplace is False:
            return Route(list(xx), list(yy))


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
    def rotate_point(origin, point, angle):
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
            p = self.rotate_point(c, (x, y), rad)
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
