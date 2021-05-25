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
import cv2
from utils import *
from text import add_text, blur_fade
from blocks import compute_length, render_blocks
from piano import LB_HEIGHT, VideoReader, render_frame as crop_piano, render_top
from effects.glare import cache_glare, render_glare
from effects.dots import cache_dots, render_dots
from effects.stars import cache_stars, render_stars
pygame.init()


def render_piano(settings, surface, piano_video, frame):
    piano = array_to_surf(crop_piano(settings, piano_video, frame))
    piano = pygame.transform.scale(piano, list(map(int, settings["piano.computed_crop"][4][:2])))

    y = settings["output.resolution"][1]/2
    if settings["piano.top"] == "LIGHT_BAR":
        y += LB_HEIGHT

    width, height = settings["output.resolution"]
    hfac = settings["piano.height_fac"]
    if hfac != 1:
        size = (width, int(hfac*height))
        piano = pygame.transform.scale(piano, size)

    surface.blit(piano, (0, y))


def render(settings, piano_video, frame):
    width, height = settings["output.resolution"]
    surface = pygame.Surface(settings["output.resolution"])

    if settings["piano.octave_lines"]:
        note = 3
        while note < 88:
            x = int(key_position(settings, note)[0] + settings["blocks.x_offset"])
            pygame.draw.line(surface, (20, 20, 20), (x-1, 0), (x-1, height))
            pygame.draw.line(surface, (75, 75, 75), (x, 0), (x, height))
            pygame.draw.line(surface, (20, 20, 20), (x+1, 0), (x+1, height))
            note += 12

    render_dots(settings, surface, frame)
    render_stars(settings, surface, frame)
    render_blocks(settings, surface, frame)
    pygame.draw.rect(surface, (0, 0, 0), (0, height/2, width, height))
    render_piano(settings, surface, piano_video, frame)
    render_top(settings, surface, frame)
    render_glare(settings, surface, frame)

    return surface


def export(settings, cache):
    output = settings["files.output"]
    res = settings["output.resolution"]
    fps = settings["output.fps"]
    shape = (*res[::-1], 3)

    if cache:
        cache_glare(settings)
        cache_dots(settings)
        cache_stars(settings)

    video = cv2.VideoWriter(output, cv2.VideoWriter_fourcc(*"mp4v"),
        settings["output.fps"], tuple(settings["output.resolution"]))

    if settings["text.show_intro"]:
        add_text(video, fps, res, settings["text.intro"], settings["text.font"])

    piano_video = VideoReader(settings["files.video"])
    length = compute_length(settings)

    logger = ProgressLogger("Rendering", length)
    for frame in range(length):
        logger.update(frame)
        logger.log()

        img = surf_to_array(render(settings, piano_video, frame))
        if frame < fps:
            img = blur_fade(img, shape, frame/fps)
        elif frame > length-fps:
            img = blur_fade(img, shape, (length-frame)/fps)
        video.write(img)
    logger.finish(f"Finished exporting {length} frames in $TIMEs")

    if settings["text.show_ending"]:
        add_text(video, fps, res, settings["text.ending"], settings["text.font"])

    video.release()
