''' Routely tests '''
# Packages
import json

import gpxpy
import numpy as np
import pandas as pd
import pyproj
from geopy.distance import geodesic
from pyproj import transform
from routely import Route


def parsegpx(GPX_filepath):
    points2 = list()
    with open(GPX_filepath, 'r') as gpxfile:
        gpx = gpxpy.parse(gpxfile)
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    gpx_dict = {
                        'time': point.time,
                        'lat': point.latitude,
                        'lng': point.longitude,
                        'alt': point.elevation}
                    points2.append(gpx_dict)
    points2 = pd.DataFrame(points2)
    return points2

def calculate_distance(df):
    df['dlat'] = df['lat'].shift(periods=1, fill_value=None)
    df['dlng'] = df['lng'].shift(periods=1, fill_value=None)
    df = df.dropna(subset=['dlat', 'dlng'])

    df['dd'] = df.apply(lambda x: geodesic((x['lat'], x['lng']), (x['dlat'], x['dlng'])).meters, axis=1)
    df['distance'] = df['dd'].cumsum()
    df = df.drop(columns=['dlat', 'dlng']).reset_index(drop=True)
    return df

def convert_latlng(data):
    wgs84 = pyproj.CRS("EPSG:4326") # LatLon with WGS84 datum used by GPS units
    web_merc = pyproj.CRS('EPSG:3857') # Web mercator projection used by Google Maps

    x, y = transform(wgs84, web_merc, list(data['lat']), list(data['lng']))
    data[['x', 'y']] = pd.DataFrame(zip(x, y))
    return data


f = r'C:\Users\hag67301\Documents\GitHub\routely\tests\003.gpx'

gps = parsegpx(f)
gps = calculate_distance(gps)
gps = convert_latlng(gps)

coords = {
    'x':list(gps['x'].values),
    'y':list(gps['y'].values),
    'e':list(gps['alt'].values)
}

x = coords['x']
y = coords['y']
z = {'e': coords['e']}

r = Route(x, y, z=z)
r.center_on_origin(inplace=True)
r.plotroute(markers=False)
r.plot_z(markers=False)

coords = {
    'x':list(r.x),
    'y':list(r.y),
    'e':list(r.z['e'])
}

with open('test_dataset1.json', 'w') as fp:
    json.dump(coords, fp)

