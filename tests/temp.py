''' Routely tests '''
# Packages
import json

import numpy as np
import pandas as pd
from routely import Route

with open('test_dataset1.json', 'r') as fp:
    data = json.load(fp)


x = [0, 5, 5, 20, 10]
y = [0, 10, 10, 10, 5]

z = {
    'foo':[0, 5, 15, 20, 10],
    # 'bar':[0, 10, 40, 10, 5],
    # 'car':[0, 10, 40, 10, 5]
}

x = data['x']
y = data['y']
z = {list(data.keys())[-1]: data[list(data.keys())[-1]]}

r = Route(x, y, z=z)
r.center_on_origin(inplace=True)
r.plotroute(markers=False)
r.plot_z(markers=False)
