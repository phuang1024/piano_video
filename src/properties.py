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
import pygame.gfxdraw
import pv
import shared
from gui_utils import *
pygame.init()


class Properties:
    tab_size = 35
    tab_spacing = 5
    tab_col_idle = 42
    tab_col_selected = 72
    tab_col_hovered = 54

    props_height = 24
    props_bg = 42
    props_header = 72

    def __init__(self):
        self.tab = 0
        self.hovering = None
        self.queue = []
        self.elements = []   # List of elements that have been drawed as props

    def redraw(self, surface, rect):
        pygame.draw.rect(surface, (28, 28, 28), rect)
        self.draw_tabs(surface, rect)
        self.draw_props(surface, rect)

    def draw(self, surface, rect):
        self.update(rect)

        while len(self.queue) > 0:
            task = self.queue.pop(0)
            if task["type"] == "DRAW_TABS":
                self.draw_tabs(surface, rect)
            elif task["type"] == "DRAW_PROPS":
                self.draw_props(surface, rect)

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
                icon = cv2.resize(section.icon_img, (size-6,)*2, interpolation=cv2.INTER_AREA)
                icon = array_to_surf(icon)
                icon.set_colorkey((0, 0, 0))
                surface.blit(icon, (x+spacing+3, cy+3))

    def draw_props(self, surface, rect):
        x, y, w, h = rect
        x += self.tab_spacing+self.tab_size   # Account for tab margin
        w -= self.tab_spacing+self.tab_size
        rect = (x, y, w, h)

        height = self.props_height
        bg = self.props_bg
        header = self.props_header
        self.elements = []

        pygame.draw.rect(surface, (bg,)*3, rect)

        grid_y = 0
        for panel in pv.context.ui_sections[self.tab].panels:
            # Draw header
            cy = grid_y*height + y
            pygame.draw.rect(surface, (header,)*3, (x, cy, w, height))
            pygame.draw.circle(surface, (255,)*3, (x+height/2, cy+height/2), 7, (0 if panel.expanded else 1))
            self.draw_text(surface, rect, panel.label, grid_y, x_offset=height)
            self.elements.append({"type": "HEADER", "idname": panel.idname})
            grid_y += 1

            if panel.expanded:
                # Draw panel elements
                pass

    def draw_text(self, surface, rect, text, grid_y, color=240, x_offset=0, y_offset=0):
        height = self.props_height

        surf = FONT.render(text, 1, (color,)*3)
        y = grid_y*height + rect[1]
        w, h = surf.get_size()
        margin = height - h

        surface.blit(surf, (rect[0]+margin+x_offset, y+margin/2+y_offset))

    def update(self, rect):
        self.update_tabs(rect)
        self.update_props(rect)

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

        if hovering != self.hovering:
            self.queue.append({"type": "DRAW_TABS"})
        if tab != self.tab:
            self.queue.append({"type": "DRAW_TABS"})
            self.queue.append({"type": "DRAW_PROPS"})

        self.hovering = hovering
        self.tab = tab

    def update_props(self, rect):
        x, y, w, h = rect

        grid = (shared.mpos[1]-y) // self.props_height
        edited = False
        if 0 <= grid < len(self.elements):
            element = self.elements[grid]
            if element["type"] == "HEADER":
                if 1 in shared.mdowns:
                    panel = pv.utils.get(pv.context.ui_sections[self.tab].panels, element["idname"], raise_error=False)
                    if panel is not None:
                        panel.expanded = (not panel.expanded)
                        edited = True

        if edited:
            self.queue.append({"type": "DRAW_PROPS"})
