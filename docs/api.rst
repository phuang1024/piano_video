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

3. The Add-ons: These are scripts that use the Piano Video module.
These scripts run **all** the core functionality in Piano Video.
**An add-on is defined as any script that extends the functionality
of Piano Video in any way, including core functionality.** It should
not be thought of as a script that adds a little to the GUI.

Piano Video has a few built-in add-ons, such as MIDI parsing and
rendering the blocks. These built-in add-ons are enough for general
use. If you would like to customize the program, such as
creating your own blocks, you would do this through the API.
