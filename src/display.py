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

import numpy as np
import cv2
import pygame
import pv
from gui_utils import *
pygame.init()


class GuiDisplay:
    def __init__(self):
        self.prev_size = None

    def redraw(self, surface, rect):
        self.draw(surface, rect)

    def draw(self, surface, rect):
        x, y, w, h = rect
        if (w, h) != self.prev_size:
            pv.disp.image = np.zeros((h, w, 3), dtype=np.uint8)
        self.prev_size = (w, h)

        pv.disp.draw()

        img = pv.disp.image
        img = cv2.resize(img, (w, h))
        img = array_to_surf(img)
        surface.blit(img, (x, y))
