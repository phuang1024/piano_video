Introduction
============

Thanks for considering contributing to Piano Video!

As outlined in the `plan <../blog/plan.html>`__, Piano Video comes in three
sections:

GUI
---

This is the interface for most end users. Currently, it does nothing, and I
will likely not accept contributions to this area for now.

It will probably be written in Python, with GUI libraries like Tkinter or Pygame.

API
---

This is a pure Python library that doesn't do much computationally, but must
be easy and intuitive for add-on developers.

The API cannot be changed without prior notice in the docs, so if you intend to
improve this area, you will most likely be doing docstrings, type hinting, etc.

Kernel
------

This is the core rendering engine. The kernel can be further split into two parts:
Rendering System and Built-in Add-ons.

The rendering system is relatively simple. All it does is call the rendering functions
in order and put together the final video. This is written in Python.

The built-in add-ons are complex. They are the actual rendering functions. They
use Python to access the API, but may optionally call C++ libraries for a speed
improvement.
