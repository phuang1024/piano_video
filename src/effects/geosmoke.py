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
            infofile.write(struct.pack("<I", i))

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
    note, start, end, special = note_info

    with open(os.path.join(path, f"{i}.bin"), "wb") as file:
        file.write(bytes([note]))
        file.write(struct.pack("f", start))
        file.write(struct.pack("f", end))

        x_loc, key_width = key_position(settings, note)
        x_loc += key_width/2
