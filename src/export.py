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
import cv2
import pygame
from constants import *
from utils import *
from midi import parse_midis
pygame.init()


def detect_length(settings, notes):
    max_frame = max(notes, key=lambda x: x[2])
    return int(max_frame[2]) + settings["output.ending_pause"]*settings["output.fps"]


def render(settings, frame):
    return pygame.Surface(settings["output.resolution"])


def export_video(settings, length):
    video = cv2.VideoWriter(settings["output.path"], cv2.VideoWriter_fourcc(*"MPEG"),
        settings["output.fps"], settings["output.resolution"])

    for frame in range(length):
        img = surf_to_array(render(settings, frame))
        video.write(img)

    video.release()


def export_images(settings, length):
    os.makedirs(settings["output.path"], exist_ok=True)
    for frame in range(length):
        print(frame)
        img = render(settings, frame)
        path = os.path.join(settings["output.path"], f"{frame}.jpg")
        pygame.image.save(img, path)


def export(settings):
    notes = parse_midis(settings)
    length = settings["output.length"] if settings["output.length"] != "autodetect" \
        else detect_length(settings, notes)

    if settings["output.format"] == "video":
        export_video(settings, length)
    elif settings["output.format"] == "images":
        export_images(settings, length)
