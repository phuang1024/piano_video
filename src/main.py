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
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

import argparse
import json
import pygame
import cv2
from constants import *
from utils import *
from export import export
pygame.init()


def preview_crop(settings, frame):
    path = settings["files.video"]
    if not os.path.isfile(path):
        print("No video file: {}".format(path))
        return

    video = cv2.VideoCapture(path)
    for f in range(frame):
        rval, img = video.read()
        if not rval:
            print(f"Error decoding frame {f} of video.")
            return

    rval, img = video.read()
    surf = array_to_surf(img)
    (x1, y1), (x2, y2), height = settings["piano.video_crop"]
    slope = (y2-y1) / (x2-x1)
    x3, y3 = (x1-height*slope if slope != 0 else x1), y1+height
    x4, y4 = x3 + (x2-x1), y3 + (y2-y1)

    color = (255, 0, 0)
    pygame.draw.line(surf, color, (x1, y1), (x2, y2))
    pygame.draw.line(surf, color, (x1, y1), (x3, y3))
    pygame.draw.line(surf, color, (x2, y2), (x4, y4))
    pygame.draw.line(surf, color, (x3, y3), (x4, y4))

    pygame.draw.circle(surf, color, (x1, y1), 5, width=1)
    pygame.draw.circle(surf, color, (x2, y2), 5, width=1)
    pygame.draw.circle(surf, color, (x3, y3), 5, width=1)
    pygame.draw.circle(surf, color, (x4, y4), 5, width=1)

    pygame.image.save(surf, settings["output.path"])


def main():
    parser = argparse.ArgumentParser(description="Creates a video from a piano MIDI.")
    parser.add_argument("-s", "--settings", help="set the json settings file path", type=str, required=True)
    parser.add_argument("-o", "--output", help="output file path (WILL overwrite)", type=str, required=True)
    parser.add_argument("-m", "--mode", help="mode of usage", type=str, required=False)
    parser.add_argument("-f", "--frame", help="frame number in modes where applicable (default 0)", type=int, required=False)
    args = parser.parse_args()

    if os.path.isfile(args.settings):
        with open(args.settings, "r") as file:
            user_settings = json.load(file)
        settings = DEFAULT_SETTINGS.copy()
        for key in user_settings:
            settings[key] = user_settings[key]
        settings["output.path"] = os.path.expanduser(os.path.realpath(args.output))

        if not hasattr(args, "mode") or args.mode == "EXPORT":
            export(settings)
        elif args.mode == "PREVIEW_CROP":
            preview_crop(settings, args.frame if (hasattr(args, "frame") and args.frame is not None) else 0)
        else:
            print(f"Invalid mode: {args.mode}")

    else:
        print(f"No file: {args.settings}")


main()
