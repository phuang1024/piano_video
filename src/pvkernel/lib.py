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
import ctypes
import numpy as np
from typing import Callable

I32 = ctypes.c_int32
F32 = ctypes.c_float
IMG = np.ctypeslib.ndpointer(dtype=np.uint8, ndim=3, flags="aligned, c_contiguous")


class Library:
    """
    A library wrapper for a Shared Object file.
    """

    def __init__(self, path: str) -> None:
        self.path = path
        self.lib = ctypes.CDLL(os.path.realpath(path))

    def __getattr__(self, name: str) -> Callable:
        return getattr(self.lib, name)


class LibSwitch:
    """
    Switch between Python, C++, and Cuda libraries
    depending on env variables.
    """

    def __init__(self, py_lib, cpp_lib, cuda_lib) -> None:
        self.py = py_lib
        self.cpp = cpp_lib
        self.cuda = cuda_lib

    def __getattr__(self, name: str) -> Callable:
        if "PV_USE_CUDA" in os.environ and self.cuda is not None:
            return getattr(self.cuda, name)
        elif "PV_USE_CPP" in os.environ and self.cpp is not None:
            return getattr(self.cpp, name)
        else:
            return getattr(self.py, name)
