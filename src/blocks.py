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

import pygame
from constants import *
from utils import *
pygame.init()


def render_blocks(settings, surface, notes, frame):
    width, height = settings["output.resolution"]
    middle = settings["computed.middle"]
    px_per_frame = settings["computed.px_per_frame"]

    keys_total_width = settings["computed.keys_total_width"]
    offset = settings["computed.keys_offset"]
    black_fac = settings["piano.black_width_fac"]
    black_width = settings["computed.black_width"]
    white_width = settings["computed.white_width"]

    for note, start, end in notes:
        start_y = middle - px_per_frame*(start-frame)
        end_y = middle - px_per_frame*(end-frame)

        if not (start_y < 0 or end_y > height):   # Don't draw if out of bounds
            x = key_x_loc(keys_total_width, note, black_fac) + offset
            curr_width = white_width if is_white_key(note) else black_width
            pygame.draw.rect(surface, settings["blocks.color"], (x, end_y, curr_width, start_y-end_y))
