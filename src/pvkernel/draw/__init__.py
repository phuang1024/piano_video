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

import numpy as np
from typing import Tuple
from ..lib import *
from ..utils import rgba

LIB.draw_circle.argtypes = [IMG, I32, I32, *[F64 for _ in range(8)]]
LIB.draw_rect.argtypes = [IMG, I32, I32, *[F64 for _ in range(14)]]


def circle(img: np.ndarray, color: Tuple[float, ...], center: Tuple[float, float],
        radius: float, border: float = 0):
    """
    Draws a circle.

    :param img: Image.
    :param color: RGB or RGBA color.
    :param center: (X, Y) center.
    :param radius: Radius.
    :param border: Border thickness. Set to 0 for no border.
    """
    assert img.dtype == np.uint8
    color = rgba(color)
    LIB.draw_circle(img, img.shape[1], img.shape[0], *center, radius, border, *color)


def rect(img: np.ndarray, color: Tuple[float, ...], dims: Tuple[float, float, float, float],
        border: float = 0, border_radius: float = 0, tl_rad: float = -1, tr_rad: float = -1,
        bl_rad: float = -1, br_rad: float = -1) -> None:
    """
    Draws a rectangle.

    :param img: Image.
    :param color: RGB or RGBA color.
    :param dims: (X, Y, W, H) dimensions.
    :param border: Border thickness.
    :param border_radius: Corner rounding radius.
    :param tl_rad: Top left corner radius.
    :param tr_rad: Top right corner radius.
    :param bl_rad: Bottom left corner radius.
    :param br_rad: Bottom right corner radius.
    """
    assert img.dtype == np.uint8
    color = rgba(color)
    LIB.draw_rect(img, img.shape[1], img.shape[0], *dims, border, border_radius, tl_rad, tr_rad, bl_rad, br_rad, *color)
