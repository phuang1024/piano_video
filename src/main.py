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
from constants import *
from export import export
from video import init as video_init, preview_crop, interactive_preview


def main():
    parser = argparse.ArgumentParser(description="Creates a video from a piano MIDI.")
    parser.add_argument("-s", "--settings", help="set the json settings file path", type=str, required=True)
    parser.add_argument("-o", "--output", help="output file path (WILL overwrite without prompt)", type=str, required=True)
    parser.add_argument("-m", "--mode", help="mode of usage", type=str, required=False)
    parser.add_argument("-f", "--frame", help="frame to use in modes where applicable", type=int, required=False)
    args = parser.parse_args()

    if not os.path.isfile(args.settings):
        print(f"No file: {args.settings}")
        return

    with open(args.settings, "r") as file:
        user_settings = json.load(file)
    settings = DEFAULT_SETTINGS.copy()
    for key in user_settings:
        settings[key] = user_settings[key]
    settings["files.output"] = args.output
    settings["other.frame"] = args.frame if args.frame is not None else 0

    video_init(settings)

    if args.mode is None or args.mode == "EXPORT":
        export(settings)
    elif args.mode == "PREVIEW_CROP":
        preview_crop(settings)
    elif args.mode == "INTERACTIVE_PREVIEW":
        interactive_preview(settings)


main()