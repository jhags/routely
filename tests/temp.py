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
z = [0, 5, 15, 20, 10]
z_labels = ['foo']

z = {
    'foo':[0, 5, 15, 20, 10],
    'bar':[0, 10, 40, 10, 5]
}

r = Route(x, y, z=z, z_labels=z_labels)
r.plotroute()
r.plot_z()

# r2 = r.interoplate(kind='cubic', num=20, inplace=False)
# r2.plotroute()


# r.fit_to_box(200, 200, inplace=True)
# r.plotroute()

# r.interoplate(kind='cubic', num=100, inplace=True)
# r.plotroute()

# r.optimise_bbox(200, 200, inplace=True)
# r.plotroute()

# r.align_to_origin(align_corner='topleft', inplace=True)
# r.plotroute()

