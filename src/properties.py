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
    tab_spacing = 5
    tab_col_idle = 42
    tab_col_selected = 96
    tab_col_hovered = 60

    def __init__(self):
        self.tab = 0
        self.hovering = None
        self.queue = []

    def redraw(self, surface, rect):
        pygame.draw.rect(surface, (28, 28, 28), rect)
        self.draw_tabs(surface, rect)

    def draw(self, surface, rect):
        self.update(rect)

        while len(self.queue) > 0:
            task = self.queue.pop(0)
            if task["type"] == "DRAW_TABS":
                self.draw_tabs(surface, rect)

    def draw_tabs(self, surface, rect):
        x, y, w, h = rect
        spacing = self.tab_spacing
        size = self.tab_size

        for num in range(len(pv.context.ui_sections)):
            # Draw tab
            cy = (y+spacing) + num*(size+spacing)
            color = self.tab_col_selected if self.tab == num else \
                (self.tab_col_hovered if self.hovering == num else self.tab_col_idle)
            pygame.draw.rect(surface, (color,)*3, (x+spacing, cy, size, size),
                border_top_left_radius=5, border_bottom_left_radius=5)

            # Draw icon
            section = pv.context.ui_sections[num]
            if section.icon_img is not None:
                icon = pygame.transform.scale(array_to_surf(section.icon_img), (size-6,)*2)
                icon.set_colorkey((0, 0, 0))
                surface.blit(icon, (x+spacing+3, cy+3))

    def update(self, rect):
        self.update_tabs(rect)

    def update_tabs(self, rect):
        x, y, w, h = rect
        mx, my = shared.mpos
        spacing = self.tab_spacing
        size = self.tab_size

        # Calculate tab hovering
        hovering = None
        tab = self.tab
        if (x+spacing <= mx <= x+spacing+size):
            tmp_y = my
            while (tmp_y > 2*spacing+size):
                tmp_y -= (spacing+size)
            if tmp_y < spacing+size:
                hovering = (my-spacing) // (spacing+size)
        if shared.mpress[0] and hovering is not None:
            tab = hovering

        if hovering != self.hovering or tab != self.tab:
            self.queue.append({"type": "DRAW_TABS"})

        self.hovering = hovering
        self.tab = tab
