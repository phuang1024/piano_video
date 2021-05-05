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
import struct
import numpy as np
import pygame
from constants import *
from utils import *


def cache_glare(settings):
    path = os.path.join(CACHE, "glare")
    os.makedirs(path, exist_ok=True)

    with open(os.path.join(path, "info.bin"), "wb") as infofile:
        for i, (note, start, end) in enumerate(settings["blocks.notes"]):
            infofile.write(struct.pack("<I", i))

            with open(os.path.join(path, f"{i}.bin"), "wb") as file:
                file.write(bytes([note]))
                file.write(struct.pack("f", start))
                file.write(struct.pack("f", end))

                x_loc, width = key_position(settings, note)
                x_loc += width/2


def add_glare(settings, surface, frame):
    if not settings["effects.glare"]:
        return

    random = settings["other.random"]
