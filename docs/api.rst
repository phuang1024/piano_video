Piano Video API
==================

*Version 0*

**THIS API IS SUBJECT TO CHANGE WITHOUT PREVIOUS NOTICE
The API will be considered secure when v1 is released.**

Piano Video has a Python API in the form of a module.
The API allows you to add features into the GUI.

The API is inspired by `Blender's <https://blender.org>`__ API.


Installation
------------

The module is provided on PyPI, and can be installed with Pip.
However, you do NOT need to install the module, as it is contained
in every release.

``pip install piano-video``

.. code-block:: python

    import pv
    print(pv.__version__)


Basics of the API
-----------------

The whole Piano Video program is made up of three parts:

1. The GUI: This is the part that opens the display and shows
everything to you on a screen.

2. The API: This is the Python module that allows you to easily
customize and add features to Piano Video.

3. The Add-ons: These are scripts that use the API module.
The add-ons give Piano Video all of it's functionality, including
core features like MIDI parsing.

Piano Video has built-in add-ons, such as MIDI parsing and
rendering the blocks. These add-ons are enough for general
use. If you would like to customize the program, such as
creating your own blocks, you would write your own add-on
in Python using API.


The PV Module
-------------

The API module, called PV (Piano Video), is structured as follows:


``pv.context``
**************

Contains the current state of the GUI, such as the current settings
and registered UI sections.


``pv.props``
************

Property classes for display on the GUI.


``pv.types``
************

Classes that can be registered onto the GUI.


``pv.utils``
************

Utilities for PV, such as registering and unregistering a class.
