API Tutorial
============


Installation
------------

The module is provided on PyPI, and can be installed with Pip.
However, you do NOT need to install the module, as it is contained
in every release.

``pip install piano-video``

.. code-block:: python

    import pv
    print(pv.__version__)


Piano Video Structure
---------------------

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
