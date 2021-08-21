Render Jobs
===========

*Written August 6, 2021*

*Updated August 10, 2021*

In order to be easily extensible, I will develop the rendering process with *jobs*:
Jobs will be included in *Job Slots*, which are specific to each Video class instance.

* ``init``: Prepare for rendering
* ``intro``: Text introduction
* ``frame_init``: Initialize variables specific to a frame.
* ``frame``: Rendering the actual video (individual jobs can do a part of it)
* ``frame_deinit``: Free memory (if applicable) for each frame.
* ``outro``: Text outroduction
* ``modifiers``: Modifies the whole image
* ``deinit``: Free memory (if applicable), close files, etc.

API
---

Jobs are a collection of operator idnames to run.

Some job slots can have multiple jobs (e.g. effects), and some can only have one job
(e.g. piano).

The graphical job operators should modify the input image at ``video.render_img``

**ALL INPUT AND OUTPUT IMAGES WILL HAVE THREE CHANNELS, RGB.**
