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
import random
from constants import *
from utils import *


def cache_smoke(settings):
    if not settings["effects.smoke"]:
        return

    notes = settings["blocks.notes"]
    path = os.path.join(settings["files.cache"], "smoke")
    os.makedirs(path, exist_ok=True)

    with open(os.path.join(path, "info.bin"), "wb") as infofile:
        for i in range(len(notes)):
            infofile.write(struct.pack(I32, i))

    logger = ProgressLogger("Caching smoke", len(notes))
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
        for i, note in enumerate(notes):
            logger.update(i)
            logger.log()
            cache_single_note(settings, path, i, note)

    logger.finish(f"Finished caching {len(notes)} smoke in $TIMEs")

def cache_portion(settings, path, notes, frames):
    for f in frames:
        cache_single_note(settings, path, f, notes[f])

def cache_single_note(settings, path, i, note_info):
    width, height = settings["output.resolution"]
    fps = settings["output.fps"]
    note, start, end, special = note_info

    with open(os.path.join(path, f"{i}.bin"), "wb") as file:
        file.write(bytes([note]))
        file.write(struct.pack(F32, start))
        file.write(struct.pack(F32, end))

        x_loc, key_width = key_position(settings, note)
        x_loc += key_width/2

        dpf = settings["effects.smoke.dps"] / fps
        lifetime = settings["effects.smoke.lifetime"] * fps

        dots = []  # List of [x, y, x_vel, y_vel, frames_lived]
        y_min = height//2
        y_max = height//2
        x_min = x_loc
        x_max = x_loc
        frame = 0
        while True:
            frame += 1
            if frame <= end-start:
                # Add more dots
                for _ in range(math.ceil(dpf*frame-len(dots))):
                    dots.append([x_loc+random.randint(-10, 10), height//2, random.uniform(-0.4, 0.4),
                        random.uniform(-3, -1.5), 0])

            dots = [d for d in dots if d[4] <= lifetime]
            if len(dots) == 0:
                break

            out_of_screen = []
            for i, d in enumerate(dots):
                d[0] += d[2]
                d[1] += d[3]
                d[4] += 1
                x_min = min(x_min, d[0])
                x_max = max(x_max, d[0])
                y_min = min(y_min, d[1])
                y_max = max(y_max, d[1])
                if not (0 <= d[0] < width and 0 <= d[1] < height):
                    out_of_screen.append(i)

            out_of_screen.sort(reverse=True)
            for i in out_of_screen:
                dots.pop(i)

            file.write(struct.pack(I32, int(frame+start)))

            # Write


def render_smoke(settings, surface, frame):
    if not settings["effects.smoke"]:
        return

    cache_path = os.path.join(settings["files.cache"], "smoke")
    with open(os.path.join(cache_path, "info.bin"), "rb") as infofile:
        while True:
            num = infofile.read(4)
            if len(num) < 4:
                break

            num = struct.unpack(I32, num)[0]
            path = os.path.join(cache_path, f"{num}.bin")
            with open(path, "rb") as file:
                file.read(1)   # Read not needed data
                start = struct.unpack("f", file.read(4))[0]
                end = struct.unpack("f", file.read(4))[0]
                if frame < start:
                    continue

                while True:
                    d = file.read(4)
                    if len(d) < 4:
                        break
                    f = struct.unpack(I32, d)[0]

                    if f >= frame:
                        # TODO

                        break

                    # Read not needed data
                    # TODO
