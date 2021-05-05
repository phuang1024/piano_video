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
import cv2
from utils import *
from video import VideoReader, render_frame as render_piano
pygame.init()


def render(settings, piano_video, frame):
    surf = pygame.Surface(settings["output.resolution"])

    piano = array_to_surf(render_piano(settings, piano_video, frame))
    piano = pygame.transform.scale(piano, list(map(int, settings["piano.computed_crop"][4][:2])))
    surf.blit(piano, (0, settings["output.resolution"][1]/2))

    return surf


def export(settings):
    video = cv2.VideoWriter(settings["files.output"], cv2.VideoWriter_fourcc(*"mp4v"),
        settings["output.fps"], tuple(settings["output.resolution"]))
    piano_video = VideoReader(settings["files.video"])

    for frame in range(1000):
        print(frame)

        img = surf_to_array(render(settings, piano_video, frame))
        video.write(img)

    video.release()
