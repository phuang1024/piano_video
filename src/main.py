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
from videomix import compute_crop_points, crop_piano, generate_mask
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

    x1 = settings["piano.video_crop_x1"]
    y1 = settings["piano.video_crop_y1"]
    x2 = settings["piano.video_crop_x2"]
    y2 = settings["piano.video_crop_y2"]
    x3 = settings["piano.video_crop_x3"]
    y3 = settings["piano.video_crop_y3"]
    x4 = settings["piano.video_crop_x4"]
    y4 = settings["piano.video_crop_y4"]
    x5 = settings["piano.video_crop_x5"]
    y5 = settings["piano.video_crop_y5"]
    x6 = settings["piano.video_crop_x6"]
    y6 = settings["piano.video_crop_y6"]

    color = (255, 0, 0)
    pygame.draw.line(surf, color, (x1, y1), (x2, y2))
    pygame.draw.line(surf, color, (x1, y1), (x3, y3))
    pygame.draw.line(surf, color, (x2, y2), (x4, y4))
    pygame.draw.line(surf, color, (x3, y3), (x4, y4))
    pygame.draw.line(surf, color, (x5, y5), (x6, y6))

    pygame.draw.circle(surf, color, (x1, y1), 5, width=1)
    pygame.draw.circle(surf, color, (x2, y2), 5, width=1)
    pygame.draw.circle(surf, color, (x3, y3), 5, width=1)
    pygame.draw.circle(surf, color, (x4, y4), 5, width=1)
    pygame.draw.circle(surf, color, (x5, y5), 5, width=1)
    pygame.draw.circle(surf, color, (x6, y6), 5, width=1)

    out_path = settings["output.path"]
    mask = generate_mask(settings)

    cropped = crop_piano(settings, img)
    masked = cropped * mask
    cropped_path = os.path.join(os.path.dirname(out_path), "cropped_"+os.path.basename(out_path))
    masked_path = os.path.join(os.path.dirname(out_path), "masked_"+os.path.basename(out_path))

    pygame.image.save(surf, out_path)
    cv2.imwrite(cropped_path, cropped)
    cv2.imwrite(masked_path, masked)


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

        compute_crop_points(settings)
        if not hasattr(args, "mode") or args.mode is None or args.mode == "EXPORT":
            export(settings)
        elif args.mode == "PREVIEW_CROP":
            preview_crop(settings, args.frame if (hasattr(args, "frame") and args.frame is not None) else 0)
        else:
            print(f"Invalid mode: {args.mode}")

    else:
        print(f"No file: {args.settings}")


main()
