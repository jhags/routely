''' Routely tests '''
# Packages
import numpy as np

from routely import Route

# %load_ext autoreload
#%%
# %autoreload 2
x = [0, 5, 15, 20, 10]
y = [0, 10, 40, 10, 5]

r = Route(x, y)
r.plotroute()
# r.bbox()
# r.center()

r.optimise_bbox(20, 20, inplace=True)
# r.interoplate(kind='cubic', num=100, inplace=True)
r.plotroute()
# r.fit_to_box(100, 100, inplace=True)
# r.plotroute()



# dist_between_points = int(data['distance'].max()/len(data)/(1 - smoothing_factor))

# r2 = r.mirror(about_x=False, about_y=True, about_axis=True, inplace=False)
# r2.plotroute()


# r.reset_origin(new_origin=(100, 100), inplace=True)
# r.plotroute(markers=False)

# r.interoplate(kind='cubic', num=100, inplace=True)
# r.plotroute(markers=False)
