# Routely
Common operations and transformations on routes represented by a 2D line in xy space

Route is designed to provide many of the common route operations and transformations to make route processing simpler and quicker.

A route is represented by a series of point coordinates on a two dimensional x-y plane. Z-axis data can be specified as well, however the primary focus of these common transformations are based on the x-y plane data with z-axis data being transformed accordingly.

The primary focus is on x-y plane data because z-axis data does not have to represent a path through three dimensional space, rather z-data can represent additonal layers of route data that correspond to the x-y path.

For example, a runner may be tracking pace or heartrate, a car will have changes in speed, etc. Therefore, transformations are primarily concerned with the x-y route taken.

## Installation

```python
pip install routely
```

## Usage
To begin with, let's define a path that comprises two lists of x and y points that together form the coordinates of the line.
```python
# x and y coordinates of a path.
x = [-5, 5, 15, 25, 20, 0]
y = [0, 10, 40, 15, 5, 20]
```

To make use of Routely, we can pass these lists of x and y points to Routely's Route class.
```python
from routely import Routely

r = Route(x, y)
r.plotroute()
```
