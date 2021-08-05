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
import shutil
import subprocess

PARENT = os.path.dirname(os.path.realpath(__file__))


class Wheel:
    """
    Build a wheel distutils package.
    """

    def __init__(self, name: str, description: str, src: str) -> None:
        """
        Initializes the wheel object.

        :param name: Package name.
        :param src: Source directory. Relative path from "piano_video".
        """
        self.name = name
        self.description = description
        self.src = os.path.realpath(os.path.join(PARENT, "..", src))
        self.dest = os.path.join(PARENT, name)

    def __enter__(self):
        sys.argv.extend(("bdist_wheel", "sdist"))

        if os.path.isdir(self.dest):
            shutil.rmtree(self.dest)
        shutil.copytree(self.src, self.dest)

        return self

    def __exit__(self, *args):
        sys.argv.remove("bdist_wheel")
        sys.argv.remove("sdist")
        shutil.rmtree(self.dest)

    def build(self, version, reqs):
        args = ["python", os.path.join(PARENT, "whl_build.py"), "bdist_wheel", "sdist",
            self.name, self.description, version, *reqs]
        subprocess.Popen(args).wait()
