Smoke Simulation
================

*Written August 10, 2021*

*Updated August 12, 2021*

When a note is pressed, smoke will emit out of it.
This is different to "Particles" which are small dots of light that
also emit out of the note.

Screenshot
----------

.. image:: smoke.png
    :width: 300

This is the smoke simulation algorithm on August 12.
The default setting uses 20000 new smoke particles per second, which exports at about
20 fps on my computer.

The smoke starts rectangular, and then disperses into an amorphous shape. This kind of
"echoes" the notes in the smoke, which I think is pretty cool.

Method 1
--------

The first method is fast but not very accurate. It keeps track of a collection
of verticies which represent the outer boundary of the smoke area.

This presents a few problems:

* Currently, there is no polygon draw function implemented.
* If verticies cross (e.g. a vertex previously on top is now lower than another),
  we need to figure out what order to draw the mesh in.
* Real smoke does not have a surface mesh, and is instead many particles in it's
  volume.

Method 2
--------

This is similar to `Brownian Motion <https://en.wikipedia.org/wiki/Brownian_Motion>`__.
The program will simulate possibly millions of particles moving around, and use
the density to determine the smoke intensity.

This will be computationally costly.

We need to implement a few rules and parameters:

* Diffusion: Particles repel each other (will also cause the smoke to expand outwards).
* Inertia: How fast particles are affected by outer forces. Parameter called mass.
* Air Resistance: Particles slow down over time.

We can ignore gravity because smoke particles are light.
