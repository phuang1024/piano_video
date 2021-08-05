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
import shutil
import subprocess

PARENT = os.path.dirname(os.path.realpath(__file__))
START_DATA = """
#!/usr/bin/python3.8
import sys
import os
cmd = "python {} "
for a in sys.argv[1:]:
    cmd += a
    cmd += " "
os.system(cmd.strip())
""".strip()


class PyDeb:
    """
    Python-activated debian package.
    """

    def __init__(self, name: str, description: str, src: str, version: str) -> None:
        parts = version.split(".")
        self.version = ".".join(parts[:-1]) + "-" + parts[-1]

        self.real_name = name
        self.name = f"{name}_{self.version}"
        self.description = description
        self.src = os.path.realpath(os.path.join(PARENT, "..", src))
        self.dest = os.path.join(PARENT, self.name)


    def __enter__(self):
        if os.path.isdir(self.dest):
            shutil.rmtree(self.dest)

        os.makedirs(os.path.join(self.dest, "usr", "local", "bin"), exist_ok=True)
        os.makedirs(os.path.join(self.dest, "DEBIAN"), exist_ok=True)

        self.write_ctrl()
        self.write_start()

        shutil.copytree(self.src, os.path.join(self.dest, "usr", "local", "bin", "pvid_utils"))
        return self

    def __exit__(self, *args):
        shutil.rmtree(self.dest)

    def write_ctrl(self):
        with open(os.path.join(self.dest, "DEBIAN", "control"), "w") as fp:
            fp.write(f"Package: {self.real_name}\n")
            fp.write(f"Description: {self.description}\n")
            fp.write(f"Version: {self.version}\n")
            fp.write(f"Section: base\n")
            fp.write(f"Priority: optional\n")
            fp.write(f"Architecture: i386\n")
            fp.write(f"Maintainer: Patrick Huang <huangpatrick16777216@gmail.com>\n")

    def write_start(self):
        path = os.path.join(self.dest, "usr", "local", "bin", "pvid")
        real_path = os.path.join("/usr", "local", "bin", "pvid_utils", "main.py")
        with open(path, "w") as fp:
            fp.write(START_DATA.format(real_path))

        subprocess.Popen(["chmod", "+x", path]).wait()

    def build(self, version, reqs):
        args = ["dpkg-deb", "--build", self.name]
        subprocess.Popen(args, cwd=PARENT).wait()
