''' Routely tests '''
# Packages
import numpy as np
import unittest
from routely.routely import Route
%load_ext autoreload

# Tests
#%%
%autoreload

x = [0, 10, 20, 30]
y = [0, 20, 40, 60]

r = Route(x=x, y=y)
r.plotroute()
r.d
r.interoplate(inplace=True)
r.plotroute()
#%%
np.array(r.route)
list(np.arange(0, np.array(r.d).max(), 1))
# Class tests

class routely_test(unittest.TestCase):

    def test_distance_between_two_points(self):
        p1 = (0, 0)
        p2 = (3, 4)

        output = Route.distance_between_two_points(p1, p2)
        self.assertEqual(output, 5)
