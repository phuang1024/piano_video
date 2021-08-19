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
    "AR_CH",
    "AR_UCH",
    "AR_DBL",
    "I32",
    "I64",
    "F32",
    "F64",
    "IMG",

    "LIB",
    "CULIB",

    "cpath",
)

import os
import ctypes
import numpy as np
from .utils import CUDA, PARENT

UCH = ctypes.c_uint8
AR_CH = np.ctypeslib.ndpointer(dtype=np.int8, ndim=1, flags="aligned, c_contiguous")
AR_UCH = np.ctypeslib.ndpointer(dtype=np.uint8, ndim=1, flags="aligned, c_contiguous")
AR_DBL = np.ctypeslib.ndpointer(dtype=np.float64, ndim=1, flags="aligned, c_contiguous")
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


def cpath(path: str) -> np.ndarray:
    """Get the C path of a string (numpy array of chars, null terminated)."""
    data = [x for x in path.encode()]
    data.append(0)
    return np.array([x for x in data], dtype=np.int8)
