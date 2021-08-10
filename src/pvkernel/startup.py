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

import sys
import os
from subprocess import DEVNULL, PIPE, Popen, STDOUT
from .utils import ADDON_PATHS

PARENT = os.path.dirname(os.path.realpath(__file__))


def register_addons():
    for path in ADDON_PATHS:
        sys.path.insert(0, path)
        for file in os.listdir(path):
            if file != "__pycache__":
                mod = __import__(file.split(".")[0])
                if hasattr(mod, "register"):
                    mod.register()
        sys.path.pop(0)


def build():
    p1 = Popen(["make", "cpp"], cwd=PARENT, stdin=DEVNULL, stdout=DEVNULL, stderr=DEVNULL)
    p1.wait()
    if p1.returncode != 0:
        print("pvkernel: c++ compilation failed.")

    if "PV_USE_CUDA" in os.environ:
        p2 = Popen(["make", "cuda"], cwd=PARENT, stdin=DEVNULL, stdout=DEVNULL, stderr=DEVNULL)
        p2.wait()
        if p2.returncode != 0:
            print("pvkernel: cuda compilation failed.")

    p3 = Popen(["make", "clean"], cwd=PARENT, stdin=DEVNULL, stdout=DEVNULL, stderr=DEVNULL)
    p3.wait()
