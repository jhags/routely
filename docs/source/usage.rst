Usage
=======

To get started, some example usage is given below. For these examples, a simple route is defined as:

.. code-block:: python

    # Route x and y coordinates and corresponding z-data
    x = [-5, 5, 15, 25, 20, 0]
    y = [0, 10, 40, 15, 5, 10]

    z1 = [0, 1, 2, 3, 4, 5] # foo
    z2 = [0, 1, 2, 3, 2, 1] # bar
    z_data = {'foo':z1, 'bar':z2}

    # These are passed to Route
    r = Route(x, y, z=z_data)

    # Plotting x, y and z looks like this
    r.plotroute()
    r.plot_z()

.. image:: https://raw.githubusercontent.com/jhags/routely/main/docs/images/plot_1.png
    :width: 49%
.. image:: https://raw.githubusercontent.com/jhags/routely/main/docs/images/plot_2.png
    :width: 49%

Common transformation
------------

Translating to origin
^^^^^^^^^^^^

Translate the whole route so that the center coordinate point is now the origin (0, 0).

.. code-block:: python
    r2 = r.center_on_origin()

    # Check the center point coordiates
    r2.center()
    (0.0, 0.0)

    r2.plotroute()

.. image:: https://raw.githubusercontent.com/jhags/routely/main/docs/images/usage_plot3.png

Aligning to origin
^^^^^^^^^^^^

Translate the route to the origin such that a specified corner of the route aligns with the origin (0, 0).
.. code-block:: python
    r2 = r.align_to_origin(align_corner='bottomleft')

    r2.plotroute()

.. image:: https://raw.githubusercontent.com/jhags/routely/main/docs/images/usage_plot4.png


Mirror about axes
^^^^^^^^^^^^

Rotating
^^^^^^^^^^^^
And something on rotation


More complex transformation
------------

Interpolation
^^^^^^^^^^^^

Smoothing
^^^^^^^^^^^^
Here is something on smoothing



