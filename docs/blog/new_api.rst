New API
=======

After developing effects for a few weeks with the API of v0.3.x, it
became clear that some changes were needed.

Problems
--------

* The ``pv.Cache`` API is hard to use.
* Unable to access C++ utility functions from external add-ons.
* Render Jobs are weird and difficult to use
* No good way of rendering a chunk of frames (this will be useful for multicore export).

Solutions
---------

* The effects should not exist in the folder ``pvkernel/addons``. They should be in
  their own folder, but may be copied to `pvkernel/addons`` when building the wheel.
* Instead of render jobs, we will have props and operators under the namespace ``render``.
  These will handle the rendering.
* In each release, ``pvutils.hpp`` file is provided. This is the header for utility functions.
