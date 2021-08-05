Building
========

As mentioned in the `plan <blog/plan.html`__, Piano Video comes in three parts.
Each part is built to separate binary files.

Build instructions:

.. code-block:: bash

    git clone https://github.com/phuang1024/piano_video.git
    cd ./piano_video
    make dist

This will generate files in the ``build`` directory.

The distributable binaries are:

* ``build/pvid_x.x.x.deb``: The GUI, as a Debian package.
* ``build/dist/pv-...whl``: The API, as a Python library.
* ``build/dist/pvkernel-...whl``: The Kernel, as a Python library.

To install, see `Installation <enduser/install.html>`__.
