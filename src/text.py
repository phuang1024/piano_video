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


def blur_fade(surface, shape, fac):
    radius = RADIUS*(1-fac)
    mask = np.full(shape, fac, np.float32)

    if isinstance(surface, pygame.Surface):
        image = surf_to_array(surface)
    else:
        image = surface

    image = np.array(Image.fromarray(image).filter(ImageFilter.GaussianBlur(radius))) * mask
    return image.astype(np.uint8)


def render_text_elements(res, text, font_path, spacing):
    width, height = res

    surface = pygame.Surface(res)
    y = spacing
    for string, size, brightness in text:
        if os.path.isfile(font_path):
            font = pygame.font.Font(font_path, size)
        else:
            font = pygame.font.SysFont(font_path, size)

        surf = font.render(string, 1, [brightness*255]*3)
        curr_x = width/2 - surf.get_width()/2
        curr_y = y - surf.get_height()/2
        surface.blit(surf, (curr_x, curr_y))

        y += spacing

    return surface


def add_text(video, fps, res, text, font_path):
    width, height = res
    shape = (height, width, 3)

    spacing = height
    for string, size, brightness in text:
        spacing -= size
    spacing /= len(text) + 1

    progress = ProgressLogger("Rendering text", fps*7)
    total_frames = 0

    # Black
    image = np.zeros(shape, dtype=np.uint8)
    for frame in range(int(fps/2)):
        progress.update(total_frames)
        progress.log()
        total_frames += 1

        video.write(image)

    # Fade in
    for frame in range(fps):
        progress.update(total_frames)
        progress.log()
        total_frames += 1

        fac = frame/fps

        surface = render_text_elements(res, text, font_path, spacing)
        image = blur_fade(surface, shape, fac)
        video.write(image)

    # Normal
    image = surf_to_array(render_text_elements(res, text, font_path, spacing))
    for frame in range(4*fps):
        progress.update(total_frames)
        progress.log()
        total_frames += 1

        video.write(image)

    # Fade out
    for frame in range(fps):
        progress.update(total_frames)
        progress.log()
        total_frames += 1

        fac = 1 - (frame/fps)

        surface = render_text_elements(res, text, font_path, spacing)
        image = blur_fade(surface, shape, fac)
        video.write(image)

    # Black
    image = np.zeros(shape, dtype=np.uint8)
    for frame in range(int(fps/2)):
        progress.update(total_frames)
        progress.log()
        total_frames += 1

        video.write(image)

    progress.finish("Finished rendering text in $TIMEs")
