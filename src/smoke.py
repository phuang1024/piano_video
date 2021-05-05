import os
import math
import struct
import random
import numpy as np
from constants import *
from utils import *

RAY_FAC_MAX = 1.25
RAY_DIST_MAX = 0.14


def cache_smoke_dots(settings):
    if not settings["effects.smoke.dots"]:
        return

    path = os.path.join(CACHE, "smoke.dots")
    os.makedirs(path, exist_ok=True)

    width, height = settings["output.resolution"]
    notes = settings["blocks.notes"]
    dot_time_inc = settings["effects.smoke.dots.dps"] / settings["output.fps"]

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
                    simulate_dot(settings, file, start+1/dot_time_inc*j, x_loc, height/2, key_width)

    logger.finish(f"Finished caching {len(notes)} smoke dots")


def simulate_dot(settings, file, frame, start_x, start_y, x_width):
    lifetime = settings["effects.smoke.dots.lifetime"]*settings["output.fps"] + random.randint(-10, 10)
    file.write(struct.pack("<H", lifetime))

    x = start_x + random.randint(int(x_width/-2), int(x_width/2))
    y = start_y
    x_vel = 0
    y_vel = -2.5
    for f in range(lifetime):
        file.write(struct.pack("<H", int(frame+f)))
        file.write(struct.pack("<H", int(x)))
        file.write(struct.pack("<H", int(y)))

        x_vel += random.uniform(-0.2, 0.2)
        y_vel += random.uniform(-0.08, 0.08)
        x += x_vel
        y += y_vel
        x = max(x, 0)


def render_dots(settings, surface, frame):
    if not settings["effects.smoke.dots"]:
        return

    cache_path = os.path.join(CACHE, "smoke.dots")
    max_life = settings["effects.smoke.dots.lifetime"]*settings["output.fps"] + 10

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
                        lifetime = struct.unpack("<H", file.read(2))[0]
                        first_frame = None
                        for j in range(lifetime):
                            curr_frame = struct.unpack("<H", file.read(2))[0]
                            if first_frame is None:
                                first_frame = curr_frame

                            if curr_frame == frame:
                                x = struct.unpack("<H", file.read(2))[0] + settings["blocks.x_offset"]
                                y = struct.unpack("<H", file.read(2))[0]
                                value = (first_frame+lifetime-curr_frame) / lifetime * 255
                                pygame.draw.circle(surface, (value, value, value), (x, y), 1)
                            else:
                                file.read(4)   # Read x and y locs
