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

"""
Run this file for a one-line command to build a wheel package.

python package.py "name" "description" "version"
"""

import sys
import os
from subprocess import Popen

PARENT = os.path.dirname(os.path.realpath(__file__))
PKG = os.path.join(PARENT, "_package.py")


def main():
    with open("../requirements.txt", "r") as fp:
        reqs = fp.read()

    env = os.environ.copy()
    env["PV_NAME"] = sys.argv[1]
    env["PV_DESCRIPTION"] = sys.argv[2]
    env["PV_VERSION"] = sys.argv[3]
    env["PV_REQS"] = reqs
    Popen(["python", PKG, "bdist_wheel", "sdist"], env=env).wait()


main()
