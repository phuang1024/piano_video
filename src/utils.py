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

import sys
import numpy as np
import cv2
import pygame
from constants import *
pygame.init()

LOGGER_CLEAR_LEN = 75


def distance(x1, y1, x2, y2):
    return ((x1-x2)**2 + (y1-y2)**2) ** 0.5


def surf_to_array(surf: pygame.Surface) -> np.ndarray:
    array = pygame.surfarray.array3d(surf).swapaxes(0, 1)
    array = cv2.cvtColor(array, cv2.COLOR_BGR2RGB)
    return array

def array_to_surf(array: np.ndarray) -> pygame.Surface:
    array = array.astype(np.float32)
    array = cv2.cvtColor(array, cv2.COLOR_BGR2RGB)
    array = array.astype(np.int8)
    return pygame.image.frombuffer(array.tobytes(), array.shape[1::-1], "RGB")


def is_white_key(key):
    return (key-3) % 12 not in (1, 3, 6, 8, 10)

def key_position(settings, key):
    """
    Returns (x_location, x_size)
    """
    white_width = settings["output.resolution"][0] / WHITE_KEYS
    num_white_before = [is_white_key(k) for k in range(key)].count(True)

    loc = num_white_before * white_width
    is_white = is_white_key(key)
    if not is_white:
        loc -= white_width * settings["blocks.black_width_fac"] / 2

    width = white_width if is_white else white_width * settings["blocks.black_width_fac"]

    return (loc, width)


def log(msg, clear=False, new=False, flush=True):
    if clear:
        clearline(flush=False)
    sys.stdout.write(msg)
    if flush and not new:
        sys.stdout.flush()
    if new:
        newline(flush=flush)

def clearline(flush=True):
    sys.stdout.write("\r")
    sys.stdout.write(" "*LOGGER_CLEAR_LEN)
    sys.stdout.write("\r")
    if flush:
        sys.stdout.flush()

def newline(flush=True):
    sys.stdout.write("\n")
    if flush:
        sys.stdout.flush()
