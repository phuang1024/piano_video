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
import colorsys
import pygame
import aadraw
import pv
import shared
from gui_utils import *
from properties import Properties
pygame.init()


class WindowManager:
    tooltip_padding = 10
    tooltip_text_height = 18

    status_bar_height = 30
    report_time = 6
    report_time_fade = 0.5

    def __init__(self) -> None:
        self.properties = Properties()
        self.prev_size = (None, None)

    def draw(self, surface):
        width, height = surface.get_size()
        sep = int(width * 0.8)
        props_rect = (sep, 0, width-sep, height-self.status_bar_height)

        if width != self.prev_size[0] or height != self.prev_size[1]:
            self.properties.redraw(surface, props_rect)

            self.prev_size = (width, height)

        self.properties.draw(surface, props_rect)

        self.draw_tooltip(surface)
        self.draw_report(surface)

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

    def draw_report(self, surface):
        width, height = surface.get_size()
        bar_height = self.status_bar_height
        pygame.draw.rect(surface, (32, 32, 32), (0, height-bar_height, width, bar_height))

        report = pv.context.report
        report_time = pv.context.report_time
    
        if report is not None and report_time >= time.time()-self.report_time:
            h, s, v = colorsys.rgb_to_hsv(*[c/255 for c in report_color(report[0])])
            text_col = 255

            # Fade in
            if time.time() < report_time+self.report_time_fade:
                fac = 2 * (time.time()-report_time)
                s *= fac

            # Fade out
            if time.time() >= report_time+self.report_time-self.report_time_fade:
                fac = 2 * ((report_time+self.report_time) - time.time())
                v *= fac
                text_col *= fac

            color = [255*c for c in colorsys.hsv_to_rgb(h, s, v)]
            color.append(text_col)
            text = FONT_SMALL.render(report[1], True, (text_col,)*3)

            w, h = text.get_size()
            text_x = width/2 - w/2
            text_y = height - self.status_bar_height/2 - h/2
            rect_coords = (text_x-3, text_y-2, w+6, h+4)

            aadraw.rect(surface, tuple(color), rect_coords, border_radius=2)
            surface.blit(text, (text_x, text_y))


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
