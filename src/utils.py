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
import shutil
import time
import colorsys
import numpy as np
import cv2
import pygame
from constants import *
pygame.init()


class ProgressLogger:
    def __init__(self, msg, total):
        self.msg = msg
        self.total = total
        self.frame = 0
        self.start = time.time()

    @staticmethod
    def _truncate(value, digits=4):
        s = str(value)
        parts = s.split(".")

        if len(parts[0]) > digits or len(parts[0]) == digits-1:
            return parts[0]
        return s[:digits]

    @staticmethod
    def _fit(msg, width=None):
        if width is None:
            width = shutil.get_terminal_size()[0]

        if len(msg) < width:
            return msg
        else:
            return msg[:width-4] + "..."

    def log(self):
        frame = self.frame
        total = self.total

        elapse = time.time() - self.start
        per_second = (frame+1) / elapse
        percent = (frame+1) / total * 100
        remaining = (total-frame-1) / per_second

        msg = f"{self.msg} {frame+1}/{total}, {self._truncate(per_second)} fps, {self._truncate(percent)}% done, " + \
            f"{self._truncate(elapse)}s elapsed, {self._truncate(remaining)}s remaining"
        msg = self._fit(msg)
        log(msg, clear=True)

    def finish(self, msg):
        elapse = time.time() - self.start
        log(msg.replace("$TIME", str(elapse)[:4]), clear=True, new=True)

    def update(self, frame):
        self.frame = frame


def mix_colors(col1, col2, fac):
    return [col1[i]*(1-fac) + col2[i]*fac for i in range(3)]

def transform_gradient(fac, gradient):
    if fac <= gradient[0][0]:
        return [i*255 for i in colorsys.hsv_to_rgb(*gradient[0][1])]
    elif fac >= gradient[-1][0]:
        return [i*255 for i in colorsys.hsv_to_rgb(*gradient[-1][1])]
    else:
        for i in range(len(gradient)):
            if gradient[i][0] >= fac:
                idx = i
                break
        rng = gradient[idx][0] - gradient[idx-1][0]
        new_fac = (fac-gradient[idx-1][0]) / rng

        col1 = gradient[idx-1][1]
        col2 = gradient[idx][1]
        new_col = mix_colors(col1, col2, new_fac)
        new_col = colorsys.hsv_to_rgb(*new_col)

        return [i*255 for i in new_col]

def in_surface(surf, loc):
    x, y = loc
    w, h = surf.get_size()
    return 0 <= x < w and 0 <= y < h

def bounds(v, lower=float("-inf"), upper=float("inf")):
    # TODO replace max(min(v, 1), 0) with this function
    return max(min(v, upper), lower)


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
        loc -= white_width * settings["blocks.black_width_fac"] / 1.75

    width = white_width if is_white else white_width * settings["blocks.black_width_fac"]
    return (loc+2, width-4)


def log(msg, clear=False, new=False, flush=True):
    if clear:
        clearline(flush=False)
    sys.stdout.write(msg)
    if flush and not new:
        sys.stdout.flush()
    if new:
        newline(flush=flush)

def clearline(flush=True):
    width = shutil.get_terminal_size()[0]
    sys.stdout.write("\r")
    sys.stdout.write(" "*width)
    sys.stdout.write("\r")
    if flush:
        sys.stdout.flush()

def newline(flush=True):
    sys.stdout.write("\n")
    if flush:
        sys.stdout.flush()
