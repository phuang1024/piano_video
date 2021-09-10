#
#  Piano Video
#  A free piano visualizer.
#  Copyright Patrick Huang 2021
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import os
from deb import PyDeb
from whl import Wheel

VERSION = "0.3.2"

PARENT = os.path.dirname(os.path.realpath(__file__))
with open(os.path.realpath(os.path.join(PARENT, "..", "requirements.txt")), "r") as fp:
    REQS = fp.read().strip().split("\n")


PACKAGES = (
    Wheel("pv", "Piano Video API.", "src/pv"),
    Wheel("pvkernel", "Piano Video Kernel.", "src/pvkernel"),
    PyDeb("pvid", "A free piano visualizer", "src/pvgui", VERSION),
)

for pkg in PACKAGES:
    with pkg:
        pkg.build(VERSION, REQS)
