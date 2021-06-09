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
    tab_size = 35
    tab_spacing = 5
    tab_col_idle = 42
    tab_col_selected = 72
    tab_col_hovered = 54

    props_height = 24
    props_bg = 42

    def __init__(self):
        self.tab = 0
        self.tab_hovering = None
        self.prop_hovering = None

        self.queue = []
        self.elements = []   # List of elements that have been drawed as props

    def redraw(self, surface, rect):
        pygame.draw.rect(surface, (28, 28, 28), rect)
        self.queue.append({"type": "DRAW_TABS"})
        self.queue.append({"type": "DRAW_PROPS"})
        self.draw(surface, rect)

    def draw(self, surface, rect):
        spacing = self.tab_spacing
        size = self.tab_size
        x, y, w, h = rect
        props_rect = (x+spacing+size, y, w-spacing-size, h)

        self.update(rect, props_rect)
        while len(self.queue) > 0:
            task = self.queue.pop(0)
            if task["type"] == "DRAW_TABS":
                self.draw_tabs(surface, rect)
            elif task["type"] == "DRAW_PROPS":
                self.draw_props(surface, props_rect)

    def draw_tabs(self, surface, rect):
        x, y, w, h = rect
        spacing = self.tab_spacing
        size = self.tab_size

        for num in range(len(pv.context.ui_sections)):
            # Draw tab
            cy = (y+spacing) + num*(size+spacing)
            color = self.tab_col_selected if self.tab == num else \
                (self.tab_col_hovered if self.tab_hovering == num else self.tab_col_idle)
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
        height = self.props_height
        bg = self.props_bg
        self.elements = []

        pygame.draw.rect(surface, (bg,)*3, rect)

        grid_y = 0
        for panel in pv.context.ui_sections[self.tab].panels:
            # Draw header
            cy = grid_y*height + y
            pygame.draw.rect(surface, (72,)*3, (x, cy, w, height-1))
            pygame.draw.circle(surface, (255,)*3, (x+height/2, cy+height/2), 7, (0 if panel.expanded else 1))
            self.draw_text(surface, rect, panel.label, grid_y, x_offset=height)
            self.elements.append({"type": "HEADER", "idname": panel.idname})
            grid_y += 1

            if panel.expanded:
                panel.layout.elements = []
                panel.draw()

                # Draw panel elements
                for element in panel.layout.elements:
                    cy = grid_y*height + y
                    hov = (self.prop_hovering == grid_y)
                    pygame.draw.rect(surface, (54,)*3, (x, cy, w, height))

                    if element["type"] == "LABEL":
                        self.draw_text(surface, rect, element["text"], grid_y)
                        self.elements.append({"type": "LABEL"})

                    elif element["type"] == "PROP":
                        self.elements.append(element)
                        group, name = element["idpath"].split(".")
                        prop = getattr(getattr(pv.context.scene, group), name)

                        if isinstance(prop, pv.props.BoolProp):
                            text = prop.label if element["text"] is None else element["text"]
                            self.draw_text(surface, rect, text, grid_y)

                            color = ((67, 180, 255) if hov else (61, 159, 255)) if prop.value else \
                                ((96,)*3 if hov else (54,)*3)
                            pygame.draw.circle(surface, color, (x+w/1.5, cy+height/2), 7)
                            pygame.draw.circle(surface, (255,)*3, (x+w/1.5, cy+height/2), 7, 1)

                    grid_y += 1

    def draw_text(self, surface, rect, text, grid_y, color=240, x_offset=0, y_offset=0):
        height = self.props_height

        surf = FONT.render(text, 1, (color,)*3)
        y = grid_y*height + rect[1]
        w, h = surf.get_size()
        margin = height - h

        surface.blit(surf, (rect[0]+margin+x_offset, y+margin/2+y_offset))

    def update(self, rect, props_rect):
        self.update_tabs(rect)
        self.update_props(props_rect)

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

        if hovering != self.tab_hovering:
            self.queue.append({"type": "DRAW_TABS"})
        if tab != self.tab:
            self.queue.append({"type": "DRAW_TABS"})
            self.queue.append({"type": "DRAW_PROPS"})

        self.tab_hovering = hovering
        self.tab = tab

    def update_props(self, rect):
        x, y, w, h = rect
        mx, my = shared.mpos
        grid = (my-y) // self.props_height
        edited = False

        hovering = grid if (x <= mx <= x+w) else None
        if hovering != self.prop_hovering:
            self.prop_hovering = hovering
            if hovering is not None:
                edited = True

        if 1 in shared.mdowns:
            if 0 <= grid < len(self.elements):
                edited = True
                element = self.elements[grid]

                if element["type"] == "HEADER":
                    panel = pv.utils.get(pv.context.ui_sections[self.tab].panels, element["idname"], raise_error=False)
                    if panel is not None:
                        panel.expanded = (not panel.expanded)

                elif element["type"] == "PROP":
                    group, name = element["idpath"].split(".")
                    prop = getattr(getattr(pv.context.scene, group), name)

                    if isinstance(prop, pv.props.BoolProp):
                        prop.value = (not prop.value)

        if edited:
            self.queue.append({"type": "DRAW_PROPS"})
