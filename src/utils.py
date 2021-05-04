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

import numpy as np
import pygame
from constants import TOTAL_KEYS, WHITE_KEYS
pygame.init()


def surf_to_array(surf: pygame.Surface) -> np.ndarray:
    return pygame.surfarray.array3d(surf).swapaxes(0, 1)

def array_to_surf(array: np.ndarray) -> pygame.Surface:
    return pygame.image.frombuffer(array.tobytes(), array.shape[1::-1], "RGB")


def is_white_key(key):
    return (key-3) % 12 not in (1, 3, 6, 8, 10)

def key_x_loc(width, key, black_fac):
    white_width = width / WHITE_KEYS
    num_white_before = [is_white_key(k) for k in range(key)].count(True)

    loc = num_white_before * white_width
    if not is_white_key(key):
        loc -= white_width * black_fac

    return loc
