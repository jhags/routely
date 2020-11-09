''' Routely '''
import numpy as np
from scipy.interpolate import interp1d

class Route:

    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y
        self.route = list(zip(x, y))


    @staticmethod
    def interoplate(self, nr_points):
        df = data_xy_dist.copy()
        x = df[df.columns[0]]
        y = df[df.columns[1]]
        a = df[df.columns[2]] # altitude
        d = df[df.columns[-1]] # the last col is distance

        dist = list(np.arange(0, d.max(), nr_points))
        xx = np.interp(dist, d, x)
        yy = np.interp(dist, d, y)
        aa = np.interp(dist, d, a)

        data_int = pd.DataFrame(list(zip(dist, xx, yy, aa)), columns=['distance', 'x', 'y', 'alt'])

        return data_int


    @staticmethod
    def interpolate_cubic(self, data_xy_dist):
        df = data_xy_dist.copy()
        x = df[df.columns[0]]
        y = df[df.columns[1]]


        # d2 = (np.linspace(d.min(), d.max(), num = 1 + round(d.max()/10,0))).astype(int)
        d2 = (np.linspace(d.min(), d.max(), num=5000)) # ensure smooth line with lots of points
        fx = interp1d(d, x, kind='cubic')
        fy = interp1d(d, y, kind='cubic')
        fa = interp1d(d, a, kind='cubic')

        x2, y2, a2 = fx(d2), fy(d2), fa(d2)

        data_interopated = pd.DataFrame({'distance':d2, 'x':x2, 'y':y2, 'alt':a2})
        return data_interopated



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

def translate_to_new_origin(data_xy, origin_xy):
    df = data_xy.copy()
    x = df[df.columns[0]]
    y = df[df.columns[1]]

    centre = ((x.max()+x.min())/2., (y.max()+y.min())/2.)

    # scale x and y
    df['x_new'] = x - centre[0] + origin_xy[0]
    df['y_new'] = y - centre[1] + origin_xy[1]

    return df[['x_new','y_new']]


def rotate(origin, point, angle):
    # Rotate a point counterclockwise by a given angle around a given origin.
    # The angle should be given in radians.

    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy


def rotate_coords_list(x_coords_list, y_coords_list, angle_deg):
    rad = math.radians(angle_deg)

    new_coords = list()
    for x, y in zip(x_coords_list, y_coords_list):
        new_coords.append(rotate((0,0), (x, y), rad))

    return new_coords


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