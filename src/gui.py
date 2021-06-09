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

import time
import pygame
import shared
from gui_utils import *
from properties import Properties
pygame.init()


class WindowManager:
    tooltip_padding = 10
    tooltip_text_height = 18

    def __init__(self) -> None:
        self.properties = Properties()
        self.prev_size = (None, None)

    def draw(self, surface):
        width, height = surface.get_size()
        sep = int(width * 0.8)
        props_rect = (sep, 0, width-sep, height)

        if width != self.prev_size[0] or height != self.prev_size[1]:
            self.properties.redraw(surface, props_rect)

            self.prev_size = (width, height)

        # Draw properties
        self.properties.draw(surface, props_rect)

        self.draw_tooltip(surface)

    def draw_tooltip(self, surface):
        width, height = surface.get_size()
        padding = self.tooltip_padding
        text_height = self.tooltip_text_height
        text_padding = (text_height-14) // 2

        if shared.tooltip is not None:
            # TODO split text by \n and render separately
            # TODO word wrap
            (x, y), header, text = shared.tooltip
            header_surf = FONT_SMALL.render(header, 1, WHITE)
            text_surf = FONT_SMALL.render(text, 1, GRAY)
            w = max(header_surf.get_width(), text_surf.get_width()) + 2*padding
            h = 2*text_height + 2*padding
            x = min(max(x, 0), width-w)
            y = min(max(y, 0), height-h)

            rect = pygame.Surface((w, h))
            rect.set_alpha(100)
            rect.fill(BLACK)
            surface.blit(rect, (x, y))
            pygame.draw.rect(surface, GRAY, (x, y, w, h), 1)

            surface.blit(header_surf, (x+padding, y+padding+text_padding))
            surface.blit(text_surf, (x+padding, y+padding+text_padding+text_height))


def gui(verbose=False):
    printer = VerbosePrinter(verbose)
    printer("Starting GUI")

    printer("  Setting up window")
    surface = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    pygame.display.set_caption(f"Piano Video {VERSION}")
    pygame.display.set_icon(IMAGES["icon"])

    wm = WindowManager()
    mouse_time_start = time.time()
    mouse_prev_pos = None

    printer("  Starting GUI loop")
    while get_run():
        clock.tick(FPS)
        pygame.display.update()

        shared.kdowns = []
        shared.mdowns = []

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                set_run(False)
            elif event.type == pygame.VIDEORESIZE:
                surface.fill(BLACK)
            elif event.type == pygame.KEYDOWN:
                # TODO key repeat when hold down
                shared.kdowns.append(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                shared.mdowns.append(event.button)

        shared.mpos = pygame.mouse.get_pos()
        shared.mpress = pygame.mouse.get_pressed()
        shared.kpress = pygame.key.get_pressed()
        shared.mtime = time.time() - mouse_time_start

        if shared.mpos != mouse_prev_pos:
            mouse_time_start = time.time()
        mouse_prev_pos = shared.mpos

        if kmod(pygame.K_q, True):
            set_run(False)

        wm.draw(surface)

    pygame.quit()
    printer("  Exiting GUI")
