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

import os
import pygame
import numpy as np
from PIL import Image, ImageFilter
from utils import *
pygame.init()

RADIUS = 8


def render_text_elements(res, text, font_path, spacing, fac):
    width, height = res

    surface = pygame.Surface(res)
    y = spacing
    for string, size, brightness in text:
        if os.path.isfile(font_path):
            font = pygame.font.Font(font_path, size)
        else:
            font = pygame.font.SysFont(font_path, size)

        surf = font.render(string, 1, [fac*brightness*255]*3)
        curr_x = width/2 - surf.get_width()/2
        curr_y = y - surf.get_height()/2
        surface.blit(surf, (curr_x, curr_y))

        y += spacing

    return surface


def add_text(video, fps, res, text, font_path):
    width, height = res

    spacing = height
    for string, size, brightness in text:
        spacing -= size
    spacing /= len(text) + 1

    progress = ProgressLogger("Rendering text", fps*6)

    # Fade in
    for frame in range(fps):
        progress.update(frame)
        progress.log()

        fac = frame/fps
        radius = RADIUS*(1-fac)

        image = surf_to_array(render_text_elements(res, text, font_path, spacing, fac))
        image = np.array(Image.fromarray(image).filter(ImageFilter.GaussianBlur(radius)))
        video.write(image)

    # Normal
    image = surf_to_array(render_text_elements(res, text, font_path, spacing, 1))
    for frame in range(4*fps):
        progress.update(frame+fps)
        progress.log()
        video.write(image)

    # Fade out
    for frame in range(fps):
        progress.update(frame+5*fps)
        progress.log()

        fac = 1 - (frame/fps)
        radius = RADIUS*(1-fac)

        image = surf_to_array(render_text_elements(res, text, font_path, spacing, fac))
        image = np.array(Image.fromarray(image).filter(ImageFilter.GaussianBlur(radius)))
        video.write(image)

    progress.finish("Finished rendering text in $TIMEs")
