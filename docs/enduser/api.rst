API
===

The API is a python module named ``pv`` that allows users to modify
the kernel's behavior.

Properties
----------

Properties are just variables, but they can be interpreted by the GUI and
displayed properly.

.. autoclass:: pv.Property
    :members:

.. autoclass:: pv.BoolProp

.. autoclass:: pv.IntProp

.. autoclass:: pv.FloatProp

.. autoclass:: pv.StrProp

.. autoclass:: pv.ListProp

A PropertyGroup is a collection of properties.

.. autoclass:: pv.PropertyGroup
    :members: _get_prop

Data and Cache
--------------

The API has a few classes for storing and accessing data.

.. autoclass:: pv.DataGroup

.. autoclass:: pv.Cache

Operators
---------

Operators are functions that operate on a video and can be displayed in the GUI.

.. autoclass:: pv.Operator

Jobs
----

Jobs modify the rendering process.

.. autoclass:: pv.Job

Utilities
---------

.. autofunction:: pv.utils.register_class

.. autofunction:: pv.utils.add_callback

.. autofunction:: pv.utils.get

.. autofunction:: pv.utils.get_index

.. autofunction:: pv.utils.get_exists
