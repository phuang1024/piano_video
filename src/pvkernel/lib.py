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
Loads library but does not provide any callable wrappers.
Import the ``LIB`` variable in specific modules and define wrappers.
"""

__all__ = (
    "UCH",
    "AR_UCH",
    "I32",
    "I64",
    "F32",
    "F64",
    "IMG",

    "LIB",
    "CULIB",
)

import os
import ctypes
import numpy as np
from .utils import CUDA, PARENT

UCH = ctypes.c_uint8
AR_UCH = np.ctypeslib.ndpointer(dtype=np.uint8, ndim=1, flags="aligned, c_contiguous")
I32 = ctypes.c_int32
I64 = ctypes.c_int64
F32 = ctypes.c_float
F64 = ctypes.c_double

IMG = np.ctypeslib.ndpointer(dtype=np.uint8, ndim=3, flags="aligned, c_contiguous")

LIB: ctypes.CDLL
CULIB: ctypes.CDLL

LIB = ctypes.CDLL(os.path.join(PARENT, "libpvkernel.so"))
if CUDA:
    CULIB = ctypes.CDLL(os.path.join(PARENT, "libpvkernel.cu.so"))
else:
    CULIB = None
