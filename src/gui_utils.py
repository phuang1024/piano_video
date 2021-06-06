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

import os
import pygame
import cv2
import numpy as np
from copy import deepcopy
pygame.init()


class ContextCompare:
    def __init__(self, attrs):
        self.attrs = attrs
        self.prev = {a: None for a in attrs}

    def compare(self, obj):
        """
        Returns whether they are a match.
        """
        for a in self.attrs:
            if self.prev[a] != getattr(obj, a):
                return False
        return True

    def update(self, obj):
        for a in self.attrs:
            self.prev[a] = deepcopy(getattr(obj, a))


class VerbosePrinter:
    """
    Takes "verbose" argument at init, and won't do anything if verbose is False.
    This will make the code cleaner (no "if verbose: print()" required)
    """

    def __init__(self, verbose):
        self.verbose = verbose

    def __call__(self, msg):
        if self.verbose:
            print(msg)


def get_run():
    return RUN

def set_run(v):
    global RUN
    RUN = v


def surf_to_array(surf: pygame.Surface) -> np.ndarray:
    array = pygame.surfarray.array3d(surf).swapaxes(0, 1)
    array = cv2.cvtColor(array, cv2.COLOR_BGR2RGB)
    return array

def array_to_surf(array: np.ndarray) -> pygame.Surface:
    array = array.astype(np.float32)
    array = cv2.cvtColor(array, cv2.COLOR_BGR2RGB)
    array = array.astype(np.int8)
    return pygame.image.frombuffer(array.tobytes(), array.shape[1::-1], "RGB")


# Global constants
VERSION = "0.1.0"
PARENT = os.path.dirname(os.path.realpath(__file__))
ADDON_PATHS = (
    os.path.join(PARENT, "addons_builtin"),
    os.path.join(PARENT, "addons_installed"),
)

DEPENDENCIES = (
    "cv2",
    "mido",
    "numpy",
    "PIL",
    "pygame",
)

# GUI
WIDTH, HEIGHT = 1280, 720
FPS = 60
IMAGES = {
    "icon": pygame.image.load(os.path.join(PARENT, "assets", "icon.jpg")),
}

RUN = True   # Whether still running. Threads end when this is false. Access with get_run(), set_run()

BLACK = (0, 0, 0)
GRAY_DARK = (64, 64, 64)
GRAY = (128, 128, 128)
GRAY_LIGHT = (192, 192, 192)
WHITE = (255, 255, 255)
