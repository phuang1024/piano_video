Running the Program
===================


System Requirements
-------------------

Please read the `requirements <install.html>`__ section.


Debian Package
--------------

If you installed the Debian package, you can run
the program by typing ``pvid`` into a terminal.

A GUI window will open.


Zip File
--------

If you downloaded an archive of the program, extract
the archive first. Then, run the file ``src/main.py``
with Python: ``python3 src/main.py``

When following commands in the rest of the manual, replace ``pvid``
with ``python3 src/main.py``. Example: When you see ``pvid --help``,
type ``python3 src/main.py --help`` instead.


Testing Dependencies
--------------------

To make sure the Piano Video API and dependent Python packages
are properly installed, run ``pvid --test --verbose`` or ``pvid -Tv`
for a shorter command.

This will run a short test that will not open a GUI. You can see
Piano Video's progress in the terminal.
