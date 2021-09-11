Kernel
======

This is the core rendering engine. The kernel can be further split into two parts:
Rendering System and Built-in Add-ons.

The rendering system is relatively simple. All it does is call the rendering functions
in order and put together the final video. This is written in Python.

The built-in add-ons are complex. They are the actual implementations of the effects.
They use Python to access the API, but may optionally call C++ libraries for a speed
improvement.

The rendering system can be found in ``/src/pvkernel``.
The add-ons are at ``/src/pvkernel/addons``.

Most optimization or minor improvements are welcome. If your patch greatly changes the
appearance, please receive feedback from some people about it.

If you would like to create a new add-on bundled with the kernel, please discuss with
me first. Thanks!

However, you can develop your own add-ons and install them through the GUI.
