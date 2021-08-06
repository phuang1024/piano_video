Render Jobs
===========

*Written August 6, 2021*

In order to be easily extensible, I will develop the rendering process with *jobs*:

The full video can be split into three parts: The text intro, the piano with effects,
and the text outro. The piano can be further split into the piano, the effects, and
the blocks. Additionally, we can have a "modifier" that works on the final image, e.g.
blurring. We can also have non-graphical jobs that run before and after rendering.

I will call these *Job Slots*.

* Init: Prepare for rendering
* Intro: Text introduction
* Piano: Rendering the piano (from source image)
* Blocks: Rendering the blocks
* Effects: Rendering the effects
* Outro: Text outroduction
* Modifiers: Modifies the whole image
* Deinit: Free memory (if applicable), close files, etc.

The slot idnames are the names above lowercase.

API
---

Jobs are a collection of operator idnames to run.

Some job slots can have multiple jobs (e.g. effects), and some can only have one job
(e.g. piano).

The graphical job operators will be given the input image at ``video.img_input`` and
should save the output to ``video.img_output``.
