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

import shutil
import random
import argparse
import json
from constants import *
from export import export
from blocks import init as blocks_init
from piano import init as video_init, preview_crop, interactive_preview
from compile import compile_cpp


def main():
    parser = argparse.ArgumentParser(description=f"Piano Video {VERSION}: Visualize a piano performance")
    parser.add_argument("-s", "--settings", help="set the json settings file path", type=str, required=False)
    parser.add_argument("-o", "--output", help="output file path (WILL overwrite without prompt)", type=str, required=False)
    parser.add_argument("-m", "--mode", help="mode of usage", type=str, required=False)
    parser.add_argument("-f", "--frame", help="frame to use in modes where applicable", type=int, required=False)
    parser.add_argument("--no-copy", help="don't backup copy output video", action="store_true")
    parser.add_argument("--cache-path", help="set the cache path (default \"piano_video_cache\")", type=str, required=False)
    parser.add_argument("--no-cache", help="don't re-cache", action="store_true")
    parser.add_argument("--random", help="manually set random seed (string)", type=str, required=False)
    args = parser.parse_args()

    if args.settings is None and args.output is None:
        print(f"Piano Video {VERSION}: Type \"pvid --help\" for help.")
        return

    settings = DEFAULT_SETTINGS.copy()
    if args.settings:
        if not os.path.isfile(args.settings):
            print(f"No file: {args.settings}")
            return

        with open(args.settings, "r") as file:
            user_settings = json.load(file)
        for key in user_settings:
            settings[key] = user_settings[key]

    output = os.path.realpath(args.output) if args.output is not None else ""
    settings["files.output"] = output
    settings["files.cache"] = os.path.realpath("piano_video_cache") if args.cache_path is None else os.path.realpath(args.cache_path)
    settings["other.frame"] = args.frame if args.frame is not None else 0
    settings["other.random"] = DEFAULT_RANDOM if args.random is None else args.random
    if settings["blocks.style"] in ("VERTICAL_GRADIENT", "HORIZONTAL_GRADIENT"):
        settings["blocks.color"].sort(key=lambda x: x[0])

    if args.mode != "COMPILE":
        random.seed(settings["other.random_seed"])
        os.makedirs(settings["files.cache"], exist_ok=True)
        video_init(settings)
        blocks_init(settings)

    if args.mode is None or args.mode == "EXPORT":
        export(settings, (not args.no_cache))
        if not args.no_copy:
            shutil.copy(output, os.path.join(os.path.dirname(output), "backup_"+os.path.basename(output)))
    elif args.mode == "PREVIEW_CROP":
        preview_crop(settings)
    elif args.mode == "INTERACTIVE_PREVIEW":
        interactive_preview(settings)
    elif args.mode == "COMPILE":
        compile_cpp()


main()
