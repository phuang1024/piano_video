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
import shared
from gui_utils import *
from properties import Properties
pygame.init()


class WindowManager:
    def __init__(self) -> None:
        self.properties = Properties()

    def draw(self, surface):
        width, height = surface.get_size()
        sep = int(width * 0.8)

        # Draw properties
        self.properties.draw(surface, (sep, 0, width-sep, height))


def gui(verbose=False):
    printer = VerbosePrinter(verbose)
    printer("Starting GUI")

    printer("  Setting up window")
    surface = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    pygame.display.set_caption(f"Piano Video {VERSION}")
    pygame.display.set_icon(IMAGES["icon"])

    width, height = WIDTH, HEIGHT
    resized = True

    wm = WindowManager()

    printer("  Starting GUI loop")
    while get_run():
        clock.tick(FPS)
        pygame.display.update()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                set_run(False)

            elif event.type == pygame.VIDEORESIZE:
                surface.fill(BLACK)
                width, height = event.w, event.h
                resized = True

        shared.mouse_pos = pygame.mouse.get_pos()
        shared.mouse_pressed = pygame.mouse.get_pressed()
        shared.keys_pressed = pygame.key.get_pressed()
        wm.draw(surface)

    pygame.quit()
    printer("  Exiting GUI")
