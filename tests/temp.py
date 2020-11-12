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
z = [0, 10, 40, 10, 5]

r = Route(x, y, z)

# r.plotroute()


# r.fit_to_box(200, 200, inplace=True)
# r.plotroute()

# r.interoplate(kind='cubic', num=100, inplace=True)
# r.plotroute()

# r.optimise_bbox(200, 200, inplace=True)
# r.plotroute()

# r.align_to_origin(align_corner='topleft', inplace=True)
# r.plotroute()

