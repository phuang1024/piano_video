Built-in Options
================

This page provides reference to the built-in options you can use.

General
-------

* ``core.pause_start``: Number of seconds before the first note starts.
* ``core.pause_end``: Number of seconds after the last note ends.

* ``keyboard.left_offset``: Pixel offset between the left of the screen and the
  left of the piano.
* ``keyboard.right_offset``: Pixel offset between the right of the screen and the
  right of the piano.
* ``keyboard.black_width_fac``: Black key width factor respective to white key.
* ``keyboard.video_path``: Path to video file.
* ``keyboard.video_start``: Time you start playing the first note in seconds.
* ``keyboard.crop``: List of locations of the corner of the keys starting from
  top left and going clockwise.
* ``keyboard.height_fac``: Keyboard height multiplier for rendered image.
* ``keyboard.mask``: Amount of space to show under the keyboard in pixels.
* ``keyboard.sub_dim``: Subtractive dimming from 0 to 255.
* ``keyboard.mult_dim``: Multiplicative dimming.
* ``keyboard.rgb_mod``: ``[R, G, B]`` intensity factors.

* ``lighting.on``: Whether to use CG lighting.
* ``lighting.piano_width``: Width of all of the piano keys combined in meters.
* ``lighting.lights``: List of lights. See `lighting <lighting.html>`__ for more info.

* ``midi.paths``: MIDI file paths. Separate multiple with pathsep (``:``).
* ``midi.min_len``: Minimum note length in seconds.
* ``midi.reverse``: If True, notes go up from the keyboard.

* ``blocks.speed``: Speed in screens per second.
* ``blocks.rounding``: Corner rounding radius in pixels.
* ``blocks.border``: Border thickness in pixels.
* ``blocks.color``: RGB color of the center of the block.
* ``blocks.border_color``: RGB color of the border of the block.

* ``glare.intensity``: Brightness multiplier.
* ``glare.radius``: Glare radius in pixels.
* ``glare.jitter``: Amount to randomize intensity by.

* ``ptcls.intensity``: Particle brightness multiplier.
* ``ptcls.pps``: Particles per second per note.

* ``smoke.intensity``: Brightness multiplier
* ``smoke.pps``: Particles per second per note.
