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
import pv
import shared
from gui_utils import *
pygame.init()


class Properties:
    tab_size = 30
    tab_spacing = 3
    tab_col_idle = 42
    tab_col_selected = 96
    tab_col_hovered = 60

    def __init__(self):
        self.tab = 0

    def draw(self, surface, rect):
        x, y, w, h = rect
        mx, my = shared.mouse_pos

        pygame.draw.rect(surface, (28, 28, 28), rect)

        # Draw tabs
        spacing = self.tab_spacing
        size = self.tab_size
        hovering = None
        if (x+spacing <= mx <= x+spacing+size):
            tmp_y = my
            while (tmp_y > 2*spacing+size):
                tmp_y -= (spacing+size)
            if tmp_y < spacing+size:
                hovering = (my-spacing) // (spacing+size)

        cy = y + spacing
        for i, section in enumerate(pv.context.ui_sections):
            color = self.tab_col_selected if self.tab == i else \
                (self.tab_col_hovered if hovering == i else self.tab_col_idle)
            pygame.draw.rect(surface, (color,)*3, (x+spacing, cy, size, size),
                border_top_left_radius=5, border_bottom_left_radius=5)
            cy += size + spacing
