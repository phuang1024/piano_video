Particles
=========

*Written August 12, 2021*

*Updated August 20, 2021*

For simulating particles, we need to do something different than
`smoke <smoke.html>`__. Otherwise, the particles will just spread out evenly,
which looks boring.

Update
------

I didn't implement the algorithm described below, and instead took a different approach,
which is just simulating particles without any outer forces.

Algorithm
---------

First, we emit a invisible element while the note is pressed. It is used for reference
in intenral computations, but not rendered. Every frame or so, an (invisible) dot emits
at around the same speed as smoke. These dots join to form a 1D squiggly chain.

At the same time, we emit particles, like in smoke. However, these particles will be
bigger and there will be less of them. These particles have their own velocity, but are
also attracted to the chain. This will cause them to clump up in a fuzzy line.
