API Tutorial
============

A basic understanding of Python is required.


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


Add-on Structure
----------------

When you write an add-on for Piano Video, there are a few steps:

1. Defining new classes: You will define classes that inherit from
pre-defined classes in the ``pv`` module.

2. Registering the classes: Next, you will need to register each class,
which is like telling Piano Video that you wish to make your class part
of the GUI. Different classes have different behaviors when registered,
which will be described below.

Please read on to see how each step is achieved.


Writing an Add-on
-----------------

Now, let's go through the process of writing an add-on, step-by-step.

