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
import shutil
import setuptools

PARENT = os.path.dirname(os.path.realpath(__file__))
DEST = os.path.join(PARENT, "pv")
SRC = os.path.join(os.path.dirname(PARENT), "src", "pv")

long_description = """
# Piano Video

A Python api for https://github.com/HuangPatrick16777216/piano_video

`pip install piano_video`

Inspired by Blender's API.

This module is provided on PyPI for autocomplete and type hinting when developing,
and does not need to be installed by pip to run Piano Video.
The latest API module is included in every release of the program.
""".strip()

with open(os.path.join(os.path.dirname(PARENT), "requirements.txt"), "r") as file:
    requirements = file.read().strip().split("\n")

if os.path.isdir(DEST):
    if input(f"Destination {DEST} exists. Remove permanently? (y/N) ").lower().strip() == "y":
        shutil.rmtree(DEST)
    else:
        exit()
shutil.copytree(SRC, DEST)

setuptools.setup(
    name="piano_video",
    version=os.path.basename(os.environ["PYPI_VERSION"]),
    author="Patrick Huang",
    author_email="huangpatrick16777216@gmail.com",
    description="Python API for https://github.com/HuangPatrick16777216/piano_video",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HuangPatrick16777216/piano_video",
    py_modules=["pv"],
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: OS Independent",
    ],
)

shutil.rmtree(DEST)
