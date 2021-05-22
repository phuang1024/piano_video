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
import shutil

VERSION = "0.0-3"

PARENT = os.path.dirname(os.path.realpath(__file__))
SRC = os.path.join(os.path.dirname(PARENT), "src")
PKG_NAME = f"pvid_{VERSION}"
PKG = os.path.join(PARENT, PKG_NAME)

BIN = os.path.join(PKG, "usr", "local", "bin", "pvid_utils")
START = os.path.join(PKG, "usr", "local", "bin", "pvid")
CONTROL = os.path.join(PKG, "DEBIAN", "control")

DATA = {
    "Package": "pvid",
    "Version": VERSION,
    "Section": "base",
    "Priority": "optional",
    "Architecture": "i386",
    "Maintainer": "Patrick Huang <huangpatrick16777216@gmail.com>",
    "Description": "Video editor with a Python API."
}

START_DATA = """
#!/usr/bin/python3.8

import sys
import os

cmd = "python3.8 /usr/local/bin/pvid_utils/main.py "
for a in sys.argv[1:]:
    cmd += a
    cmd += " "
os.system(cmd.strip())
""".strip()


os.makedirs(BIN)
os.makedirs(os.path.dirname(CONTROL))

dirs = [""]
while len(dirs) > 0:
    for f in os.listdir(os.path.join(SRC, d:=dirs.pop())):
        relpath = os.path.join(d, f)
        abspath = os.path.join(SRC, relpath)
        if "__pycache__" in abspath:
            continue

        dst = os.path.join(BIN, relpath)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if os.path.isfile(abspath) and (".py" in abspath or "assets" in abspath) and (not "__pycache__" in abspath):
            shutil.copy(abspath, dst)
        elif os.path.isdir(abspath):
            dirs.append(relpath)

with open(CONTROL, "w") as file:
    for key in DATA:
        file.write("{}: {}\n".format(key, DATA[key]))

with open(START, "w") as file:
    file.write(START_DATA)
os.system(f"chmod +x {START}")

subprocess.Popen(["dpkg-deb", "--build", PKG_NAME], cwd=PARENT).wait()
shutil.rmtree(PKG)
