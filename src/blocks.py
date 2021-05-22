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
import cv2
import pygame
import mido
from utils import *
pygame.init()

GLOW_STEPS = 4
TOP_FADE_HEIGHT = 250
LIGHT_UP_HEIGHT = 150


class PxType:
    nfac: float   # Normal color factor
    bfac: float   # Border color factor
    gfac: float   # Glow color factor

    def __init__(self, empty=False, nfac=0, bfac=0, gfac=0):
        self.empty = empty
        self.nfac = nfac
        self.bfac = bfac
        self.gfac = gfac


def init(settings):
    parse_midis(settings)
    load_images(settings)


def load_images(settings):
    width, height = settings["output.resolution"]

    if settings["blocks.style"] == "SOLID":
        if settings["blocks.color_type"] == "IMAGE":
            path = get_image_path(settings["blocks.image"])
            grad = settings["blocks.image_gradient"]
            print(f"Loading grayscale from {path}")

            loaded_img = cv2.resize(cv2.imread(path), (width, height))
            final_img = np.empty((height, width, 3), dtype=np.float32)
            logger = ProgressLogger(f"Processing image, row", height)
            for y in range(height):
                logger.update(y)
                logger.log()

                for x in range(width):
                    col = loaded_img[y][x]
                    if len(grad) == 0:
                        final_img[y][x] = col
                    else:
                        fac = np.sum(col) / (255*3)
                        final_img[y][x] = transform_gradient(fac, grad)
            logger.finish("Finished processing image in $TIMEs")

            final_img = cv2.cvtColor(final_img, cv2.COLOR_BGR2RGB)
            settings["blocks.image_final"] = final_img


def get_image_path(name):
    if os.path.isfile(p := os.path.expanduser(os.path.realpath(name))):
        return p
    elif os.path.isfile(p := os.path.join(PARENT, "assets", name)):
        return p
    else:
        raise ValueError(f"No file or builtin image: {name}")


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


def px_info(settings, block_rect, loc) -> PxType:
    width, height = settings["output.resolution"]
    bx, by, bw, bh = block_rect
    x, y = loc
    r = settings["blocks.rounding"]
    b = settings["blocks.border"]

    if x < 0 or x > width or y < 0 or y > width:  # Out of screen
        return PxType(empty=True)
    elif x < bx-1 or x > bx+bw+1 or y < by-1 or y > by+bh+1:  # Out of block
        return PxType(empty=True)

    elif bx+r <= x <= bx+bw-r and by+r <= y <= by+bh-r:  # Center of block
        return PxType(nfac=1)

    # Check sides of block
    hlim   = (bx+r    <= x <= bx+bw-r)
    vlim   = (by+r    <= y <= by+bh-r)

    left   = (bx-1    <= x <= bx+r)    and vlim
    right  = (bx+bw-r <= x <= bx+bw+1) and vlim
    top    = (by-1    <= y <= by+r)    and hlim
    bottom = (by+bh-r <= y <= by+bh+1) and hlim

    if left or right or top or bottom:
        if left:
            diff = bx - x
        elif right:
            diff = x - (bx+bw)
        elif top:
            diff = by - y
        elif bottom:
            diff = y - (by+bh)

        # Compute color factors
        bfac = bounds(min(diff+b+1, 1-diff), 0, 1) if -b-1 <= diff <= 1 else 0
        nfac = 1 if diff <= 0 else bounds(1-diff, 0, 1)
        return PxType(nfac=nfac, bfac=bfac)

    # Check corners
    ul = (bx-1    <= x <= bx+r)    and (by-1    <= y <= by+r)
    bl = (bx-1    <= x <= bx+r)    and (by+bh-r <= y <= by+bh+1)
    ur = (bx+bw-r <= x <= bx+bw+1) and (by-1    <= y <= by+r)
    br = (bx+bw-r <= x <= bx+bw+1) and (by+bh-r <= y <= by+bh+1)
    if ul or bl or ur or br:
        if ul:
            p2 = (bx+r, by+r)
        elif bl:
            p2 = (bx+r, by+bh-r)
        elif ur:
            p2 = (bx+bw-r, by+r)
        elif br:
            p2 = (bx+bw-r, by+bh-r)
        dist = pythag_dist((x, y), p2)
        diff = dist - r

        # Compute color factors
        bfac = bounds(min(diff+b+1, 1-diff), 0, 1) if -b-1 <= diff <= 1 else 0
        nfac = 1 if diff <= 0 else bounds(1-diff, 0, 1)
        return PxType(nfac=nfac, bfac=bfac)

    return PxType(empty=True)


def col_from_info(settings, info: PxType, loc):
    width, height = settings["output.resolution"]
    x, y = loc

    ncol_input = settings["blocks.color"]
    ncol_type = settings["blocks.color_type"]
    if ncol_type == "SOLID":
        ncol = ncol_input
    elif ncol_type == "VERTICAL_GRADIENT":
        ncol = transform_gradient(y/(height/2), ncol_input)
    elif ncol_type == "HORIZONTAL_GRADIENT":
        ncol = transform_gradient(x/width, ncol_input)

    ncol = np.array(ncol) * info.nfac
    bcol = np.array(settings["blocks.border_color"]) * info.bfac
    return (ncol+bcol) / 2


def draw_block_normal(settings, surface, rect):
    bx, by, bw, bh = rect

    for x in range(int(bx)-1, int(bx+bw)+3):
        for y in range(int(by)-1, int(by+bh)+3):
            info = px_info(settings, rect, (x, y))
            if not info.empty:
                col = col_from_info(settings, info, (x, y))
                surface.set_at((x, y), col)


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
            elif settings["blocks.style"] == "SOLID":
                draw_block_normal(settings, surface, rect)
