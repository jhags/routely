''' Routely tests '''
# Packages
import numpy as np
import pandas as pd
from routely import Route

# %load_ext autoreload
#%%
# %autoreload 2
x = [0, 5, 15, 20, 10]
y = [0, 10, 40, 10, 5]

z = {
    'foo':[0, 5, 15, 20, 10],
    # 'bar':[0, 10, 40, 10, 5],
    # 'car':[0, 10, 40, 10, 5]
}

r = Route(x, y, z=z)
r.plotroute()
# r.plot_z()

r.fit_to_box(20, 20, keep_aspect=True, inplace=True)
# r.plotroute()

r.interoplate(kind='cubic', num=100, inplace=True)
# r.plotroute()

r.optimise_bbox(200, 200, inplace=True)
# r.plotroute()

r.align_to_origin(align_corner='topleft', inplace=True)
r.plotroute()
r.plot_z()

p = Route(r.d, r.z['foo'])
p.fit_to_box(10, 1, keep_aspect=False, inplace=True)
p.plotroute(markers=False, equal_lims=False)