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
from blocks import render_blocks
from midi import parse_midis
from videomix import generate_mask, render_piano
pygame.init()


def compute_info(settings):
    """
    Computes information required for rendering and stores it in settings.
    Saves re-computations each frame.
    """

    width, height = settings["output.resolution"]
    keys_total_width = width - 2*(1-settings["layout.border_fac"])
    keys_offset = settings["layout.border_fac"] * width

    px_per_frame = settings["blocks.speed"] * height / settings["output.fps"]
    middle = settings["layout.middle_fac"] * height

    black_fac = settings["piano.black_width_fac"]
    white_width = keys_total_width / TOTAL_KEYS
    black_width = white_width * black_fac

    settings["computed.keys_total_width"] = keys_total_width
    settings["computed.keys_offset"] = keys_offset

    settings["computed.px_per_frame"] = px_per_frame
    settings["computed.middle"] = middle

    settings["computed.white_width"] = white_width
    settings["computed.black_width"] = black_width


def detect_length(settings, notes):
    max_frame = max(notes, key=lambda x: x[2])
    return int(max_frame[2]) + settings["output.ending_pause"]*settings["output.fps"]


def render(settings, notes, frame, piano_video, mask):
    surface = pygame.Surface(settings["output.resolution"])
    render_blocks(settings, surface, notes, frame)
    render_piano(settings, surface, mask, piano_video, 0, frame, None)
    return surface


def export_video(settings, length, notes):
    video = cv2.VideoWriter(settings["output.path"], cv2.VideoWriter_fourcc(*"MPEG"),
        settings["output.fps"], settings["output.resolution"])

    piano_video = cv2.VideoCapture(settings["files.video"])
    piano_mask = generate_mask(settings)
    for frame in range(length):
        log(f"Exporting frame {frame+1} of {length}", clear=True)

        img = surf_to_array(render(settings, notes, frame, piano_video, piano_mask))
        video.write(img)

    log(f"Finished exporting {length} frames", clear=True, new=True)
    video.release()


def export_images(settings, length, notes):
    os.makedirs(settings["output.path"], exist_ok=True)

    piano_video = cv2.VideoCapture(settings["files.video"])
    piano_mask = generate_mask(settings)
    for frame in range(length):
        img = render(settings, notes, frame, piano_video, piano_mask)
        path = os.path.join(settings["output.path"], f"{frame}.jpg")
        pygame.image.save(img, path)


def export(settings):
    compute_info(settings)

    notes = parse_midis(settings)
    length = settings["output.length"] if settings["output.length"] != "autodetect" \
        else detect_length(settings, notes)

    if settings["output.format"] == "video":
        export_video(settings, length, notes)
    elif settings["output.format"] == "images":
        export_images(settings, length, notes)
