Installation
============

Requirements
------------

* The GNU Compiler Collection
* GNU Make
* Python 3.8
* `Python packages <https://github.com/phuang1024/piano_video/blob/main/requirements.txt>`__

GNU/Linux
---------

Pre-Built
^^^^^^^^^

The latest release can be found
`here <https://github.com/phuang1024/piano_video/releases/latest>`__.

All releases (starting from ``v0.2.0``) have pre-built binaries.
There will be a Debian package for Ubuntu and Debian, and two Python wheel files.

If you are unable to install one or more of those, please see the "From Source"
section below.

To install the Debian package:

.. code-block:: bash

    sudo dpkg -i pvid_x.x.x.deb

To install the wheel files:

.. code-block:: bash

    pip install pv_...whl
    pip install pvkernel_...whl

File names vary.

From Source
^^^^^^^^^^^

First build the files. Instructions are `here <../dev/build.html>`__

Then, install the files as above.

Windows and Mac
---------------

If you are using Windows or MacOS, switch to GNU/Linux and
`give yourself some freedom <https://gnu.org/philosophy/free-sw.html>`__

Piano Video is developed and tested on GNU/Linux and may or may not work on other
operating systems.

Old Versions
------------

Piano Video has had two previous versions before ``v0.2.0``.

The first was a CLI version which was difficult to use. Unfortunately, the
documentation does not exist anymore. You can find the program on the ``cli-old``
branch.

The second is an unfinished GUI version, similar in design to the current version.
It can be found on the branch ``gui-old`` and sphinx documentation is in the
``/docs`` folder.
