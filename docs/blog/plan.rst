Plan
====

*Written on August 4, 2021*

*Updated August 5, 2021*

Currently, I have the plan to develop Piano Video in three sections:

* ``pvkernel``: This is a Python library (probably with C++) that handles
  all rendering, effects, MIDI parsing, etc.
  The kernel also contains built-in add-ons, which use the API (below) to
  add functionality to the kernel. They will be considered part of the kernel.

* ``pv``: This is a Python library which provides an API to the kernel.

* ``pvgui``: This is a Python GUI application (with Tkinter) that most end users
  will launch. It provides a graphical interface to the API and kernel.
  **Invoked through the command** ``pvid``.
