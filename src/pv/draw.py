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

import pygame
from typing import Tuple
pygame.init()


def bounds(v: float, vmin: float = 0, vmax: float = 1) -> float:
    """
    Bound a number between a min and max.
    :param v: Number
    :param vmin: Minimum value
    :param vmax: Maximum value
    """
    return min(max(v, vmin), vmax)


def mix(c1: Tuple, c2: Tuple, fac: float):
    """
    Mixes two RGB colors.
    :param c1: Color 1
    :param c2: Color 2
    :param fac: Factor of the second color.
    """
    color = [c1[i]*(1-fac) + c2[i]*fac for i in range(3)]
    color = [int(bounds(0, 255, x)) for x in color]
    return color


def pythag(x, y):
    return (x**2 + y**2) ** 0.5


def circle(img: pygame.Surface, color: Tuple[float, float, float], center: Tuple[float, float],
        radius: float, border: float = 0) -> None:
    cx, cy = center
    width, height = img.get_size()

    color = color[:3]
    out_thres = radius
    in_thres = 0 if border == 0 else (radius-border)

    x_min = max(0, int(cx-radius)-1)
    x_max = min(width, int(cx+radius)+2)
    y_min = max(0, int(cy-radius)-1)
    y_max = min(height, int(cy+radius)+2)
    for x in range(x_min, x_max):
        for y in range(y_min, y_max):
            dist = pythag(x-cx, y-cy)
            out_fac = bounds(out_thres-dist+1)
            in_fac = bounds(dist-in_thres+1)
            col = mix(img.get_at((x, y)), color, out_fac*in_fac)
            img.set_at((x, y), col)
