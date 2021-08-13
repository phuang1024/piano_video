Introduction
============

Thanks for considering contributing to Piano Video!

As outlined in the `plan <../blog/plan.html>`__, Piano Video comes in three
sections:

* `GUI <gui.html>`__
* `API <api.html>`__
* `Kernel <kernel.html>`__

Documentation on the sections can be found in their respective pages.


General
-------

Most typo or conspicuous bug fixes are accepted. If you propose an incompatible API
change or a major feature, please discuss with me first.

Do not make patches for Windows or MacOS support. I will not support
`malware <https://www.gnu.org/proprietary/proprietary.html>`__ in this project.

If you would like Windows or MacOS support, please fork the project and edit your own
copy.

To start working on a task, please either look through the
`projects <https://github.com/phuang1024/piano_video/projects>`__ or
`issues <https://github.com/phuang1024/piano_video/issues>`__ on GitHub and choose
one that interests you.


File Structure
--------------

The Piano Video repository contains these folders:

.. list-table:: File Structure
    :widths: 25 75
    :header-rows: 1

    * - Path
      - Description
    * - ``/.github``
      - GitHub workflows for testing.
    * - ``/build``
      - Build scripts for ``deb`` and ``whl``.
    * - ``/docs``
      - Documentation (mainly Sphinx).
    * - ``/examples``
      - Example MIDI and videos. They are licensed as CC0.
    * - ``/src``
      - Source code. Contains a few subdirectories.
    * - ``/src/pv``
      - `API <api.html>`__ source code.
    * - ``/src/pvgui``
      - `GUI <gui.html>`__ source code.
    * - ``/src/pvkernel``
      - `Kernel <kernel.html>`__ source code.
    * - ``/tests``
      - Testing scripts.
