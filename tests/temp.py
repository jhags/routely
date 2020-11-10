''' Routely tests '''
# Packages
import numpy as np

from routely import Route

# %load_ext autoreload
#%%
# %autoreload 2
x = [0, 5, 15, 20, 10]
y = [0, 10, 20, 10, 5]

r = Route(x, y)

r.interoplate(kind='cubic', num=100, inplace=True)
r.plotroute()

r2 = r.mirror(about_x=False, about_y=False, about_axis=False, inplace=False)
r2.plotroute()
r2.centre()

# r.reset_origin(new_origin=(100, 100), inplace=True)
# r.plotroute(markers=False)

# r.interoplate(kind='cubic', num=100, inplace=True)
# r.plotroute(markers=False)
