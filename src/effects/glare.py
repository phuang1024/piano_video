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
import math
import struct
import multiprocessing
import random
import numpy as np
from constants import *
from utils import *

RAY_FAC_MAX = 1.25
RAY_DIST_MAX = 0.14


def cache_glare(settings):
    if not settings["effects.glare"]:
        return

    notes = settings["blocks.notes"]
    path = os.path.join(settings["files.cache"], "glare")
    os.makedirs(path, exist_ok=True)


    with open(os.path.join(path, "info.bin"), "wb") as infofile:
        for i in range(len(notes)):
            infofile.write(struct.pack("<I", i))

    logger = ProgressLogger("Caching glare", len(notes))
    if settings["other.use_mc"]:
        portions = partition(range(len(notes)), settings["other.cores"])
        processes = []
        for portion in portions:
            p = multiprocessing.Process(target=cache_portion, args=(settings, path, notes, portion))
            p.start()
            processes.append(p)

        while any([p.is_alive() for p in processes]):
            time.sleep(0.05)
            done = len(os.listdir(path)) - 1    # Minus 1 so don't count "info.bin"
            logger.update(done)
            logger.log()

    else:
        for i, note_data in enumerate(notes):
            logger.update(i)
            logger.log()
            cache_single_glare(settings, path, i, *note_data)

    logger.finish(f"Finished caching {len(notes)} glares in $TIMEs")

def cache_portion(settings, path, notes, frames):
    for f in frames:
        cache_single_glare(settings, path, f, *notes[f])

def cache_single_glare(settings, path, i, note, start, end):
    width, height = settings["output.resolution"]
    glare_width, glare_height = settings["effects.glare_size"]

    with open(os.path.join(path, f"{i}.bin"), "wb") as file:
        file.write(bytes([note]))
        file.write(struct.pack("f", start))
        file.write(struct.pack("f", end))

        x_loc, key_width = key_position(settings, note)
        x_loc += key_width/2
        file.write(struct.pack("<H", int(x_loc-glare_width/2)))
        file.write(struct.pack("<H", int((height-glare_height)/2)))

        glare = np.empty((glare_height, glare_width), dtype=np.float16)
        glare_rays = [random.uniform(0, 2*math.pi) for _ in range(random.randint(2, 5))]
        for x in range(glare_width):
            for y in range(glare_height):
                x_fac = min(x, glare_width-x) / (glare_width/2)
                y_fac = min(y, glare_height-y) / (glare_height/2)

                dx = x - glare_width/2
                dy = y - glare_height/2
                angle = math.atan2(dy, dx)
                min_diff = float("inf")
                for ray in glare_rays:
                    diff = min(abs(ray-angle), abs(ray-angle+360), abs(ray-angle-360))
                    min_diff = min(min_diff, diff)
                ray_fac = RAY_FAC_MAX - (RAY_FAC_MAX-1)/RAY_DIST_MAX*min_diff
                ray_fac = max(ray_fac, 1)

                glare[y, x] = x_fac*y_fac*ray_fac

        data = glare.tobytes()
        file.write(struct.pack("<I", len(data)))
        file.write(data)


def render_glare(settings, surface, frame):
    if not settings["effects.glare"]:
        return

    cache_path = os.path.join(settings["files.cache"], "glare")
    glare_width, glare_height = settings["effects.glare_size"]

    with open(os.path.join(cache_path, "info.bin"), "rb") as infofile:
        while True:
            num = infofile.read(4)
            if len(num) < 4:
                break

            num = struct.unpack("<I", num)[0]
            path = os.path.join(cache_path, f"{num}.bin")
            with open(path, "rb") as file:
                file.read(1)  # Don't need note data
                start = struct.unpack("f", file.read(4))[0]
                end = struct.unpack("f", file.read(4))[0]
                x_loc = struct.unpack("<H", file.read(2))[0]
                y_loc = struct.unpack("<H", file.read(2))[0]

                if start <= frame <= end:
                    fac = random.uniform(0.65, 0.8)
                    glare = np.frombuffer(file.read(struct.unpack("<I", file.read(4))[0]), dtype=np.float16).reshape((glare_height, glare_width))
                    for y_val in range(glare_height):
                        for x_val in range(glare_width):
                            x = int(x_loc + x_val + settings["blocks.x_offset"])
                            y = y_loc + y_val
                            if in_surface(surface, (x, y)):
                                curr_fac = max(min(glare[y_val][x_val]*fac, 1), 0)
                                surface.set_at((x, y), mix_colors(surface.get_at((x, y))[:3], (255, 255, 255), curr_fac))
