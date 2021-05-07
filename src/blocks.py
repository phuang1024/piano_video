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


def init(settings):
    parse_midis(settings)


def parse_midis(settings):
    notes = []

    for file in settings["files.midis"]:
        midi = mido.MidiFile(file)
        tpb = midi.ticks_per_beat

        starts = [None for _ in range(88)]
        tempo = 500000
        curr_frame = -1 * settings["output.fps"] * settings["blocks.time_offset"]
        for msg in midi.tracks[0]:
            curr_frame += msg.time / tpb * tempo / 1000000 * settings["output.fps"]
            if msg.is_meta and msg.type == "set_tempo":
                tempo = msg.tempo
            elif msg.type in ("note_on", "note_off"):
                note, velocity = msg.note-21, msg.velocity
                if velocity == 0 or msg.type == "note_off":
                    end = max(curr_frame, starts[note]+5)
                    notes.append((note, starts[note], end))
                else:
                    starts[note] = curr_frame

    settings["blocks.notes"] = notes


def draw_glow_1px(settings, surface, rect, cx, cy):
    width, height = settings["output.resolution"]
    x, y, w, h = map(int, rect)
    r = settings["blocks.rounding"]
    glow_col = settings["blocks.glow_color"]

    if r <= cx <= w-r and r <= cy <= r:   # Point is inside the block
        dist = 0
    elif r <= cx <= w-r:                  # Point is above or below block
        dist = min(abs(cy), abs(cy-h))
    elif r <= cy <= h-r:                  # Point is to the side of the block
        dist = min(abs(cx), abs(cx-w))
    else:                                 # Point is in one of the corners
        # Right triangle hypotenuse (pythagorean) - rounding radius
        dx = min(abs(r-cx), abs(w-r-cx))
        dy = min(abs(r-cy), abs(h-r-cy))
        dist = (dx**2 + dy**2) ** 0.5 - r

    fac = (r-dist) / r
    fac = max(min(fac, 1), 0)
    if fac > 0 and dist != 0:
        if 0 <= x+cx < width and 0 <= y+cy < height:
            color = mix_colors(surface.get_at((x+cx, y+cy)), glow_col, fac)
            surface.set_at((x+cx, y+cy), color)


def draw_glow(settings, surface, rect):
    width, height = settings["output.resolution"]
    x, y, w, h = map(int, rect)
    rounding = settings["blocks.rounding"]

    for cy in range(-rounding, h+1+rounding):
        if cy+y < 0 or cy+y > height/2:
            continue
        for cx in range(-rounding, w+1+rounding):
            draw_glow_1px(settings, surface, rect, cx, cy)


def draw_block_solid(settings, surface, rect):
    width, height = settings["output.resolution"]
    x, y, w, h = map(int, rect)

    rounding = settings["blocks.rounding"]
    base_col = settings["blocks.color"]

    # Draw glow
    if settings["blocks.glow"]:
        draw_glow(settings, surface, rect)

    for cy in range(h+1):
        if cy+y < 0 or cy+y > height/2:
            continue

        # px_col is the color for this current pixel.
        px_col = base_col
        if settings["blocks.style"] == "VERTICAL_GRADIENT":
            px_col = transform_gradient((cy+y) / (height/2), base_col)

        # Compute rounding
        if rounding == 0:
            offset = 0
        else:
            if cy < rounding:
                offset = rounding - (rounding**2 - (rounding-cy)**2) ** 0.5
            elif cy > h-rounding:
                offset = rounding - (rounding**2 - (rounding-(h-cy))**2) ** 0.5
            else:
                offset = 0

        # Draw main block
        for cx in range(w+1):
            dist_to_block = min(abs(cx-offset), abs(cx-(w-offset)))
            if offset <= cx <= w-offset:
                color = px_col
            elif dist_to_block <= 1:
                color = [i/2 for i in px_col]
            else:
                continue

            # Fade in dark
            curr_col = color
            abs_y = cy + y
            if settings["blocks.fade_top"]:
                if abs_y <= TOP_FADE_HEIGHT:
                    fac = (abs_y + TOP_FADE_HEIGHT*2) / (TOP_FADE_HEIGHT*3)
                    curr_col = [i*fac for i in color]

            # Light up when playing
            light_up_start = height/2 - LIGHT_UP_HEIGHT
            if y+h >= height/2:
                if abs_y >= light_up_start:
                    fac = (abs_y-light_up_start) / (height/2-light_up_start)
                    fac = max(min(fac, 1), 0)
                    curr_col = mix_colors(color, (255, 255, 255), fac)

            surface.set_at((cx+x, cy+y), curr_col)


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
                draw_block_solid(settings, surface, rect)


def compute_length(settings):
    max_frame = max(settings["blocks.notes"], key=lambda x: x[2])
    return int(max_frame[2]) + settings["output.ending_pause"]*settings["output.fps"]
