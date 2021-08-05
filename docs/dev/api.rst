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

A PropertyGroup is a collection of properties.

.. autoclass:: pv.PropertyGroup
    :members: _get_prop
