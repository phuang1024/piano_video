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

    logger = ProgressLogger("Caching smoke dots", len(notes))
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

                num_dots = (end-start) * dot_time_inc
                file.write(struct.pack("<I", num_dots))

                for j in range(num_dots):
                    simulate_dot(settings, file, start+dot_time_inc*j, x_loc, height/2, key_width)

    logger.finish(f"Finished caching {len(notes)} glares")


def simulate_dot(settings, file, frame, start_x, start_y, x_width):
    lifetime = settings["effects.smoke.dots.lifetime"] * settings["output.fps"] + random.uniform()
    file.write(struct.pack(lifetime, "<H"))

    x = start_x + random.randint(x_width/-2, x_width/2)
    y = start_y
    x_vel = 2
    y_vel = 0
    for f in range(lifetime):
        file.write(struct.pack("<H", frame+f))
        file.write(struct.pack("<H", int(x)))
        file.write(struct.pack("<H", int(y)))

        x_vel -= random.uniform(0, 0.025)
        y_vel += random.uniform(-0.01, 0.01)
        x += x_vel
        y += y_vel
