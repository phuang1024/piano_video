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
import subprocess
import time
import pygame
import cv2
from utils import *
from blocks import compute_length, render_blocks
from video import VideoReader, render_frame as crop_piano
from glare import render_glare, cache_glare
from smoke import cache_smoke_dots, render_dots
pygame.init()


def render_piano(settings, surface, piano_video, frame):
    piano = array_to_surf(crop_piano(settings, piano_video, frame))
    piano = pygame.transform.scale(piano, list(map(int, settings["piano.computed_crop"][4][:2])))
    surface.blit(piano, (0, settings["output.resolution"][1]/2))


def render(settings, piano_video, frame):
    surface = pygame.Surface(settings["output.resolution"])

    render_dots(settings, surface, frame)
    render_blocks(settings, surface, frame)
    render_piano(settings, surface, piano_video, frame)
    render_glare(settings, surface, frame)

    return surface


def export(settings):
    fmat = settings["output.format"]
    output = settings["files.output"]
    images_output = output+".images"

    cache_glare(settings)
    cache_smoke_dots(settings)

    if fmat == "images":
        os.makedirs(images_output, exist_ok=True)
    elif fmat == "video":
        video = cv2.VideoWriter(output, cv2.VideoWriter_fourcc(*"mp4v"),
            settings["output.fps"], tuple(settings["output.resolution"]))

    piano_video = VideoReader(settings["files.video"])
    length = compute_length(settings)

    logger = ProgressLogger("Rendering", length)
    for frame in range(length):
        logger.update(frame)
        logger.log()

        img = render(settings, piano_video, frame)
        if fmat == "video":
            video.write(surf_to_array(img))
        elif fmat == "images":
            path = os.path.join(images_output, f"{frame}.jpg")
            pygame.image.save(img, path)

    logger.finish(f"Finished exporting {length} frames")

    if fmat == "video":
        video.release()
    else:
        subprocess.Popen(["ffmpeg", "-y", "-i", os.path.join(images_output, "%d.jpg"), "-c:v", "libx264", "-framerate",
            str(settings["output.fps"]), output], stdin=subprocess.PIPE, stdout=subprocess.PIPE).wait()
