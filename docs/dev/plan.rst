Plan
====

*Written on August 4, 2021*

Currently, I have the plan to develop Piano Video in three modules:

* ``pvkernel``: This is a Python library (probably with C++) that handles
  all rendering, effects, MIDI parsing, etc.

* ``pv``: This is a Python library which provides an API to the kernel.

* ``pvgui``: This is a Python GUI application (with Tkinter) that most users
  will launch. It provides a graphical interface to the API and kernel.
  **Invoked through the command** ``pvid``.
