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


    def route(self):
        return list(zip(self.x, self.y, self.d))


    def bbox(self):
        lower = (self.x.min(), self.y.min())
        upper = (self.x.max(), self.y.max())
        return (lower, upper)


    def centre(self):
        xc = (self.x.max() + self.x.min())/2.
        yc = (self.y.max() + self.y.min())/2.
        return (xc, yc)


    def plotroute(self, markers=True):
        x = self.x
        y = self.y

        if markers:
            marker = 'o'
        else:
            marker = None

        lb_lim = min(x.min(), y.min())
        ub_lim = max(x.max(), y.max())
        tolerance = round((ub_lim - lb_lim) * 0.05, 0)
        limits = [lb_lim - tolerance, ub_lim + tolerance]

        fig, ax = plt.subplots()
        ax.plot(x, y, 'k', marker=marker)

        fig.tight_layout()

        ax.set_aspect('equal', 'box')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_xlim(limits)
        ax.set_ylim(limits)
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


    def reset_origin(self, new_origin=(0, 0), inplace=False):
        centre = self.centre()

        # scale x and y
        x_new = self.x - centre[0] + new_origin[0]
        y_new = self.y - centre[1] + new_origin[1]

        if inplace:
            self.x = np.array(x_new)
            self.y = np.array(y_new)
        else:
            return Route(x_new, y_new)


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
        c = self.centre()
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


def scale_to_print(data_xy, bbox_print):
    # Scale is in px not mm
    df = data_xy.copy()
    x = df[df.columns[0]]
    y = df[df.columns[1]]

    #Scale to width or height?
    line_width = abs(x.max() - x.min())
    line_height = abs(y.max() - y.min())

    sfactor = max(line_height/bbox_print[1], line_width/bbox_print[0])

    # scale x and y
    df_scaled = df/sfactor
    return df_scaled

def fit_to_bbox(data_xy, bbox_print):
    # Scale is in px not mm
    df = data_xy.copy()
    x = df[df.columns[0]]
    y = df[df.columns[1]]

    #Scale factors for width and height?
    sfactor_w = abs(x.max() - x.min())/bbox_print[0]
    sfactor_h = abs(y.max() - y.min())/bbox_print[1]

    # scale x and y
    x,y = x/sfactor_w, y/sfactor_h
    df[df.columns[0]] = x
    df[df.columns[1]] = y
    return df





def optimise_bbox(data_xy, bbox_xy):
    df = data_xy.copy() # format dataframe[[x, y]]
    df.columns = ['x','y']
    spatial_eff = list() # spatial efficiency

    for angle in np.arange(5, 360, 5):
        df_rot = rotate_coords_list(list(df['x']), list(df['y']), angle)
        df_rot = pd.DataFrame(df_rot, columns=['x','y'])

        dx = df_rot['x'].max() - df_rot['x'].min()
        dy = df_rot['y'].max() - df_rot['y'].min()
        spatial_eff.append([angle, abs(dx/dy)])

    spatial_eff = pd.DataFrame(spatial_eff, columns=['angle','ratio'])
    spatial_eff['target'] = bbox_xy[0]/bbox_xy[1]
    spatial_eff['efficiency'] = spatial_eff['ratio'] - spatial_eff['target']
    spatial_eff['efficiency'] = spatial_eff['efficiency'].abs()
    spatial_eff = spatial_eff.sort_values(by=['efficiency'], ascending=True).reset_index(drop=True)
    # print(spatial_eff)
    coords = rotate_coords_list(list(df['x']), list(df['y']), spatial_eff.loc[0]['angle'])
    coords = pd.DataFrame(coords, columns=['x','y'])

    return coords[['x','y']]


def flip_coords_horizontally(data_xy):
    df = data_xy.copy()
    x = df[df.columns[0]]
    y = df[df.columns[1]]

    xy = scale(Polygon(list(zip(x,y))), xfact=-1, yfact=1).exterior.coords[:]
    df[['x_new','y_new']] = pd.DataFrame(xy)
    return df[['x_new','y_new']]

def flip_coords_about_X_axis(data_xy):
    df = data_xy.copy()
    x = df[df.columns[0]]
    y = df[df.columns[1]]

    xy = scale(Polygon(list(zip(x,y))), xfact=1, yfact=-1).exterior.coords[:]
    df[['x_new','y_new']] = pd.DataFrame(xy)
    return df[['x_new','y_new']]
