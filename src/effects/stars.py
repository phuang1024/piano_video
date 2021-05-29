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
from constants import *
from utils import *


def cache_stars(settings):
    if not settings["effects.stars"]:
        return

    path = os.path.join(settings["files.cache"], "stars")
    os.makedirs(path, exist_ok=True)

    width, height = settings["output.resolution"]
    notes = settings["blocks.notes"]

    logger = ProgressLogger("Caching stars", len(notes))
    with open(os.path.join(path, "info.bin"), "wb") as infofile:
        for i, (note, start, end, special) in enumerate(notes):
            logger.update(i)
            logger.log()

            if random.random() <= settings["effects.stars.probability"]:
                infofile.write(struct.pack("<I", i))

                x_loc, key_width = key_position(settings, note)
                x_loc += key_width/2

                with open(os.path.join(path, f"{i}.bin"), "wb") as file:
                    file.write(bytes([note]))
                    file.write(struct.pack("f", start))
                    file.write(struct.pack("f", end))
                    simulate_star(settings, file, start, x_loc, height/2)

    logger.finish(f"Finished caching {len(notes)} stars in $TIMEs")

def simulate_star(settings, file, frame, start_x, start_y):
    width, height = settings["output.resolution"]
    lifetime = settings["effects.stars.lifetime"]*settings["output.fps"] + random.randint(-10, 10)
    lifetime = int(lifetime)

    file.write(struct.pack("<H", lifetime))

    x = start_x
    y = start_y
    y_vel = -12
    x_vel = random.uniform(-2, 2)

    for f in range(lifetime):
        file.write(struct.pack("<H", int(frame+f)))
        file.write(struct.pack("<H", bounds(int(x), 0, width-1)))
        file.write(struct.pack("<H", bounds(int(y), 0, height-1)))

        y_vel += 0.15
        x += x_vel
        y += y_vel


def render_stars(settings, surface, frame):
    if not settings["effects.stars"]:
        return

    width, height = settings["output.resolution"]
    cache_path = os.path.join(settings["files.cache"], "stars")
    max_life = settings["effects.stars.lifetime"]*settings["output.fps"] + 10
    rad = settings["effects.stars.size"]

    with open(os.path.join(cache_path, "info.bin"), "rb") as infofile:
        while True:
            num = infofile.read(4)
            if len(num) < 4:
                break

            num = struct.unpack("<I", num)[0]
            path = os.path.join(cache_path, f"{num}.bin")
            with open(path, "rb") as file:
                file.read(1)   # Get note data, not needed
                start = struct.unpack("f", file.read(4))[0]
                end = struct.unpack("f", file.read(4))[0]

                if start <= frame <= end+max_life:
                    lifetime = struct.unpack("<H", file.read(2))[0]

                    # Search until found current frame for current star
                    for j in range(lifetime):
                        curr_frame = struct.unpack("<H", file.read(2))[0]
                        x = struct.unpack("<H", file.read(2))[0]
                        y = struct.unpack("<H", file.read(2))[0]
                        if curr_frame == frame:
                            for dx in range(-rad, rad+1):
                                for dy in range(-rad, rad+1):
                                    cx = x + dx
                                    cy = y + dy
                                    if 0 <= cx < width and 0 <= cy < height:
                                        dist = ((cx-x)**2 + (cy-y)**2) ** 0.5
                                        fac = 1 - (dist/rad)
                                        if 0 <= fac <= 1:
                                            col = [255*fac] * 3
                                            surface.set_at((cx, cy), col)
                            break
