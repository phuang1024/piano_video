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

"""
Scripts to generate the builtin icons in /src/pv/icons
Requires pygame
All icons are licensed as Creative Commons 0 (CC0)

Running this file will not execute any of the generating functions.
You must either edit this file (add a function call)
or import it from a console and call a function.

Each function will return a pygame surface which can be saved with
pygame.image.save(surface, "/path/to/save")
Image dimensions are (128, 128) with RGBA channels.
"""

import pygame
from math import cos, radians
pygame.init()


def gen_piano(w=180, b=65):
    img = pygame.Surface((128, 128), pygame.SRCALPHA)

    pygame.draw.polygon(img, (w, w, w), ((20, 20), (35, 20), (35, 85), (47, 85), (47, 110), (20, 110)))
    pygame.draw.polygon(img, (b, b, b), ((40, 20), (40, 80), (55, 80), (55, 20)))
    pygame.draw.polygon(img, (w, w, w), ((60, 20), (70, 20), (70, 85), (77, 85), (77, 110), (53, 110), (53, 85), (60, 85)))
    pygame.draw.polygon(img, (b, b, b), ((75, 20), (75, 80), (90, 80), (90, 20)))
    pygame.draw.polygon(img, (w, w, w), ((110, 20), (95, 20), (95, 85), (83, 85), (83, 110), (110, 110)))

    return img


def gen_output(color=(160, 30, 45)):
    img = pygame.Surface((128, 128), pygame.SRCALPHA)
    d = 20
    c = cos(radians(60))

    pygame.draw.rect(img, color, (15, 30, 98, 68))
    pygame.draw.rect(img, (0, 0, 0, 0), (0, 38, 128, 6))
    pygame.draw.rect(img, (0, 0, 0, 0), (0, 82, 128, 6))
    pygame.draw.polygon(img, (0, 0, 0, 0), ((64+d/2, 64), (64-d/2, 64+c*d), (64-d/2, 64-c*d)))

    return img
