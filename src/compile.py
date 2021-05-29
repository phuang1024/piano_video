#
#  Piano Video
#  Piano MIDI visualizer
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
import subprocess
from constants import *

PATHS = [
    "effects/glare"
]


def compile_cpp():
    for p in PATHS:
        path = os.path.join(PARENT, p+".cpp")
        out = os.path.join(PARENT, p+".out")

        cmd = ["g++", "-O3", "-Wall", path, "-o", out]
        print(" ".join(cmd))
        subprocess.Popen(cmd).wait()
