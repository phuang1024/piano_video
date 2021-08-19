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
Actually does the setting up.
Will be called through subprocess because setuptools
can only handle one call per process.
"""

import os
import sys
import setuptools
import glob

PARENT = os.path.dirname(os.path.realpath(__file__))

non_py_extensions = ("*.cpp", "*.hpp", "*.cu", "*.cuh", "Makefile")
non_py_files = [glob.iglob(os.path.join(PARENT, f"**/{ext}"), recursive=True) for ext in non_py_extensions]
non_py_files = [path for gl in non_py_files for path in gl]

name = sys.argv[3]
description = sys.argv[4]
version = sys.argv[5]
reqs = sys.argv[6:]

del sys.argv[3:]

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
