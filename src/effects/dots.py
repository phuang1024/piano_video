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

RAY_FAC_MAX = 1.25
RAY_DIST_MAX = 0.14


def cache_dots(settings):
    if not settings["effects.dots"]:
        return

    path = os.path.join(settings["files.cache"], "dots")
    os.makedirs(path, exist_ok=True)

    width, height = settings["output.resolution"]
    notes = settings["blocks.notes"]
    dot_time_inc = settings["effects.dots.dps"] / settings["output.fps"]

    logger = ProgressLogger("Caching dots", len(notes))
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

                num_dots = int((end-start) * dot_time_inc)
                file.write(struct.pack("<I", num_dots))

                for j in range(num_dots):
                    curr_time = start+1/dot_time_inc*j + random.randint(-2, 2)
                    simulate_dot(settings, file, curr_time, x_loc, height/2, key_width)

    logger.finish(f"Finished caching {len(notes)} smoke dots in $TIMEs")

def simulate_dot(settings, file, frame, start_x, start_y, x_width):
    width, height = settings["output.resolution"]
    lifetime = settings["effects.dots.lifetime"]*settings["output.fps"] + random.randint(-10, 10)
    lifetime = int(lifetime)
    style = settings["effects.dots.style"]

    file.write(struct.pack("<H", lifetime))

    x = start_x + random.randint(int(x_width/-2), int(x_width/2))/5
    y = start_y
    x_vel = random.uniform(-0.3, 0.3)
    y_vel = -6

    if style == "FLOATING":
        simulate_dot_floating(file, frame, (width, height), (x, y), (x_vel, y_vel), lifetime)
    elif style == "BOUNCING":
        simulate_dot_dropping(file, frame, (width, height), (x, y), (x_vel, y_vel), lifetime)

def simulate_dot_floating(file, frame, size, loc, vel, lifetime):
    width, height = size
    x, y = loc
    x_vel, y_vel = vel

    for f in range(lifetime):
        file.write(struct.pack("<H", int(frame+f)))
        file.write(struct.pack("<H", bounds(int(x), 0, width-1)))
        file.write(struct.pack("<H", bounds(int(y), 0, height-1)))

        x_vel += random.uniform(-0.25, 0.25)
        y_vel += random.uniform(-0.04, 0.12)
        x += x_vel
        y += y_vel
        x = max(x, 0)

def simulate_dot_dropping(file, frame, size, loc, vel, lifetime):
    width, height = size
    x, y = loc
    x_vel = random.uniform(-3, 3)
    y_vel = random.uniform(-12, -8)

    for f in range(lifetime):
        file.write(struct.pack("<H", int(frame+f)))
        file.write(struct.pack("<H", bounds(int(x), 0, width-1)))
        file.write(struct.pack("<H", bounds(int(y), 0, height-1)))

        if x_vel > 0:
            x_vel -= 0.04
        else:
            x_vel += 0.04
        y_vel += 1
        x += x_vel
        y += y_vel

        x = max(x, 0)
        if y >= height/2:
            y_vel *= -1


def render_dots(settings, surface, frame):
    if not settings["effects.dots"]:
        return

    cache_path = os.path.join(settings["files.cache"], "dots")
    max_life = settings["effects.dots.lifetime"]*settings["output.fps"] + 10

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
                num_dots = struct.unpack("<I", file.read(4))[0]

                if start <= frame <= end+max_life:
                    for i in range(num_dots):
                        # Iterate through all dots for current note
                        lifetime = struct.unpack("<H", file.read(2))[0]
                        first_frame = None

                        prev_x, prev_y = None, None
                        for j in range(lifetime):
                            # Search until found current frame for current dot

                            curr_frame = struct.unpack("<H", file.read(2))[0]
                            if first_frame is None:
                                first_frame = curr_frame

                            x = struct.unpack("<H", file.read(2))[0] + settings["blocks.x_offset"]
                            y = struct.unpack("<H", file.read(2))[0]
                            if curr_frame == frame:
                                value = (first_frame+lifetime-curr_frame) / lifetime * 255
                                if prev_x is None:
                                    pygame.draw.circle(surface, [value]*3, (x, y), 1)
                                else:    # Motion blur
                                    x1 = (x+prev_x) / 2
                                    y1 = (y+prev_y) / 2
                                    pygame.draw.line(surface, [value]*3, (x1, y1), (x, y))
                                if settings["effects.dots.glow"]:
                                    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                                        surface.set_at((x+dx, y+dy), [value*0.6]*3)
                                    for dx, dy in ((-1, -1), (-1, 1), (1, -1), (1, 1)):
                                        surface.set_at((x+dx, y+dy), [value*0.3]*3)

                            prev_x = x
                            prev_y = y
