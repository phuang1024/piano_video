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


def cache_geosmoke(settings):
    if not settings["effects.geosmoke"]:
        return

    notes = settings["blocks.notes"]
    path = os.path.join(settings["files.cache"], "geosmoke")
    os.makedirs(path, exist_ok=True)

    with open(os.path.join(path, "info.bin"), "wb") as infofile:
        for i in range(len(notes)):
            infofile.write(struct.pack(I32, i))

    logger = ProgressLogger("Caching GeoSmoke", len(notes))
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

    logger.finish(f"Finished caching {len(notes)} GeoSmoke in $TIMEs")

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

        dpf = settings["effects.geosmoke.dps"] / fps
        lifetime = settings["effects.geosmoke.lifetime"] * fps

        dots = []  # List of [x, y, x_vel, y_vel, frames_lived]
        frame = 0
        while True:
            if frame <= end-start:
                # Add more dots
                for _ in range(int(dpf*frame-len(dots))):
                    dots.append([x_loc+random.randint(-10, 10), height//2, random.uniform(-1.5, 1.5),
                        random.uniform(-7, -5), 0])

            dots = [d for d in dots if d[4] <= lifetime]
            for d in dots:
                d[0] += d[2]
                d[1] += d[3]
                d[4] += 1

            # Write dots
            file.write(struct.pack(I32, len(dots)))
            for d in dots:
                x, y = d[:2]
                file.write(struct.pack(I16, x))
                file.write(struct.pack(I16, y))

            frame += 1
