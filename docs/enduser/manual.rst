User Manual
===========

Recording
---------

Set up a camera and a piano keyboard capable of MIDI recording. Record a video
and MIDI file. This tutorial assumes they are titled ``midi.mid`` and ``video.mp4``.

You might want to save these in a new folder dedicated to this piano recording.


Your First Video
----------------

First, `install <install.html>`__ Piano Video.

Import the ``pvkernel`` library, which will give us to the ``Video`` class.
The default resolution and fps are ``(1920, 1080)``, and ``30`` respectively.

.. code-block:: python

    import pvkernel

    resolution = (1920, 1080)
    fps = 30
    video = pvkernel.Video(resolution, fps)

Now that we have our video initialized, we can start adding MIDIs.
We add them by modifying the *property* (explained later) ``midi.paths``.
To add MIDIs, run:

.. code-block:: python

    video.props.midi.paths = "your/midi/path.mid"

This adds your MIDI file into the paths that the kernel will render.
To seperate multiple MIDIs, use just a colon with no spaces. There
are example MIDIs all ready inside the examples folder.

Almost done! We just have to export the video using the code

.. code-block:: python

    video.export("video.mp4")

Hooray! You have your first video exported! With the default settings, this can take
a few minutes.


Properties
----------

Each video class instance has it's own collection of property values. The available
properties are defined by *add-ons* (covered below). Detailed property documentation
can be found `here <options.rst>`__.

Let's change the block color to blue (add this line before the export):

.. code-block:: python

    video.props.blocks_solid.color = (100, 100, 200)
