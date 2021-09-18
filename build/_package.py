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
This file is invoked by package.py

This file does the actual building. Setuptools can only build once
per process, so that is why a separate file is needed.

Run package.py instead
"""

import os
import setuptools
import glob

name = os.environ["PV_NAME"]
description = os.environ["PV_DESCRIPTION"]
version = os.environ["PV_VERSION"]
reqs = os.environ["PV_REQS"].strip().split()

PARENT = os.path.dirname(os.path.realpath(__file__))
PKG_PATH = os.path.join(PARENT, name)

non_py_extensions = ("*.cpp", "*.hpp", "*.cu", "*.cuh", "Makefile")
non_py_files = [glob.iglob(os.path.join(PKG_PATH, f"**/{ext}"), recursive=True) for ext in non_py_extensions]
non_py_files = [path for gl in non_py_files for path in gl]
non_py_files = list(set(non_py_files))

setuptools.setup(
    name=name,
    version=version,
    author="Patrick Huang",
    author_email="huangpatrick16777216@gmail.com",
    description=description,
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/phuang1024/piano_video",
    py_modules=[name],
    packages=setuptools.find_packages(),
    install_requires=reqs,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    package_data={"": non_py_files},
)
