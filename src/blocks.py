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

import mido
from utils import *

GLOW_STEPS = 4
TOP_FADE_HEIGHT = 250
LIGHT_UP_HEIGHT = 150


class PxTypes:
    NONE = 0       # Pixel is completely unrelated to the block
    INSIDE = 1     # Pixel is used to draw the inside of the block
    AA = 2         # Pixel is used to antialias block inside (when there is no border)
    BORDER = 3     # Pixel is on the border
    AABORDER = 4   # Pixel is used to antialias border


def init(settings):
    parse_midis(settings)


def parse_midis(settings):
    stabilize = settings["blocks.stabilize_fast"]
    stabilize_max = settings["blocks.stabilize_max_time"]
    stabilize_new = settings["blocks.stabilize_new_time"]

    notes = []
    for file in settings["files.midis"]:
        midi = mido.MidiFile(file)
        tpb = midi.ticks_per_beat

        starts = [None for _ in range(88)]
        tempo = 500000
        curr_frame = -1 * settings["output.fps"] * settings["blocks.time_offset"]
        for msg in midi.tracks[0]:
            curr_frame += msg.time / tpb * tempo / 1000000 * settings["output.fps"] / settings["blocks.time_mult"]
            if msg.is_meta and msg.type == "set_tempo":
                tempo = msg.tempo
            elif msg.type in ("note_on", "note_off"):
                note, velocity = msg.note-21, msg.velocity
                if velocity == 0 or msg.type == "note_off":
                    end = curr_frame
                    if stabilize and curr_frame-starts[note] <= stabilize_max:  # Stabilize sixteenth notes
                            end = stabilize_new+starts[note]
                    notes.append((note, starts[note], end))
                else:
                    starts[note] = curr_frame

    settings["blocks.notes"] = notes

def compute_length(settings):
    max_frame = max(settings["blocks.notes"], key=lambda x: x[2])
    return int(max_frame[2]) + settings["output.ending_pause"]*settings["output.fps"]


def px_info(settings, block_rect, loc):
    # Assumes block is a rect with no rounding for now.
    width, height = settings["output.resolution"]
    bx, by, bw, bh = block_rect
    x, y = loc
    r = settings["blocks.rounding"]

    # Pixel is out of screen
    if x < 0 or x > width or y < 0 or y > width:
        return {"type": PxTypes.NONE}

    # Pixel is out of block and its aa
    if x <= bx-1 or x >= bx+bw+1 or y <= by-1 or y >= by+bh+1:
        return {"type": PxTypes.NONE}

    # Edge antialiasing
    elif bx-1 <= x <= bx:  # Left side
        return {"type": PxTypes.AA, "aafac": 1-abs(x-bx)}
    elif bx+bw <= x <= bx+bw+1:  # Right side
        return {"type": PxTypes.AA, "aafac": 1-abs(x-(bx+bw))}
    elif by-1 <= y <= by:  # Left side
        return {"type": PxTypes.AA, "aafac": 1-abs(y-by)}
    elif by+bh <= y <= by+bh+1:  # Right side
        return {"type": PxTypes.AA, "aafac": 1-abs(y-(by+bh))}

    # Normal pixel
    elif bx <= x <= bx+bw and by <= y <= by+bw:
        return {"type": PxTypes.INSIDE}


def render_blocks(settings, surface, frame):
    width, height = settings["output.resolution"]
    middle = height / 2

    px_per_frame = settings["blocks.speed"] * height / settings["output.fps"]

    for note, start, end in settings["blocks.notes"]:
        start_y = middle - px_per_frame*(start-frame)
        end_y = middle - px_per_frame*(end-frame)

        if not (start_y < 0 or end_y > height):   # Don't draw block if out of bounds
            x, curr_width = key_position(settings, note)
            x += settings["blocks.x_offset"]
            rect = (x, end_y, curr_width, start_y-end_y)

            if settings["blocks.style"] == "PREVIEW":
                pygame.draw.rect(surface, (255, 255, 255), rect)
            elif settings["blocks.style"] in ("SOLID_COLOR", "HORIZONTAL_GRADIENT", "VERTICAL_GRADIENT"):
                pass
