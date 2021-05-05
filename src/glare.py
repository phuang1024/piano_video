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
import random
import numpy as np
import pygame
from constants import *
from utils import *


def cache_glare(settings):
    if not settings["effects.glare"]:
        return

    path = os.path.join(CACHE, "glare")
    os.makedirs(path, exist_ok=True)

    width, height = settings["output.resolution"]
    glare_width, glare_height = settings["effects.glare_size"]
    notes = settings["blocks.notes"]

    logger = ProgressLogger("Caching glare", len(notes))
    with open(os.path.join(path, "info.bin"), "wb") as infofile:
        for i, (note, start, end) in enumerate(notes):
            logger.update(i)
            logger.log()

            infofile.write(struct.pack("<I", i))

            with open(os.path.join(path, f"{i}.bin"), "wb") as file:
                file.write(bytes([note]))
                file.write(struct.pack("f", start))
                file.write(struct.pack("f", end))

                x_loc, key_width = key_position(settings, note)
                x_loc += key_width/2
                file.write(struct.pack("<I", int(x_loc-glare_width/2)))
                file.write(struct.pack("<I", int((height-glare_height)/2)))

                glare = np.empty((glare_height, glare_width), dtype=np.float32)
                for x in range(glare_width):
                    for y in range(glare_height):
                        x_fac = min(x, glare_width-x) / (glare_width/2)
                        y_fac = min(y, glare_height-y) / (glare_height/2)
                        glare[y, x] = x_fac*y_fac

                data = glare.tobytes()
                file.write(struct.pack("<I", len(data)))
                file.write(data)

    logger.finish(f"Finished caching {len(notes)} glares")


def add_glare(settings, surface, frame):
    if not settings["effects.glare"]:
        return

    cache_path = os.path.join(CACHE, "glare")
    glare_width, glare_height = settings["effects.glare_size"]

    with open(os.path.join(cache_path, "info.bin"), "rb") as infofile:
        while True:
            num = infofile.read(4)
            if len(num) < 4:
                break

            num = struct.unpack("<I", num)[0]
            path = os.path.join(cache_path, f"{num}.bin")
            with open(path, "rb") as file:
                file.read(1)    # Read byte containing note, not needed now.
                start = struct.unpack("f", file.read(4))[0]
                end = struct.unpack("f", file.read(4))[0]
                x_loc = struct.unpack("<I", file.read(4))[0]
                y_loc = struct.unpack("<I", file.read(4))[0]

                if start <= frame <= end:
                    fac = random.uniform(0.9, 1.1)
                    glare = np.frombuffer(file.read(struct.unpack("<I", file.read(4))[0]), dtype=np.float32).reshape((glare_height, glare_width))
                    for y_val in range(glare_height):
                        for x_val in range(glare_width):
                            x = x_loc + x_val
                            y = y_loc + y_val
                            curr_fac = max(min(glare[y_val][x_val]*fac, 1), 0)
                            surface.set_at((x, y), mix_colors(surface.get_at((x, y))[:3], (255, 255, 255), curr_fac))
