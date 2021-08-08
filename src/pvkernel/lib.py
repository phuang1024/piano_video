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
