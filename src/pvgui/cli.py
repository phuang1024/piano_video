#
#  Piano Video
#  A free piano visualizer.
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

import argparse
import shlex
import pvkernel
from termcolor import colored

BASE_CMDS = ("ls", "workon")


def cli():
    parser = argparse.ArgumentParser(description="Enter your commands to the CLI interface.")
    parser.add_argument("mode", nargs="?", choices=BASE_CMDS, help="Base command.")
    parser.add_argument("options", nargs="*", help="Options for the base command.")

    videos = [pvkernel.Video()]
    workon = 0

    while True:
        inputs = shlex.split(input(">>> "))
        args = parser.parse_args(inputs)
        mode = args.mode
        opts = args.options

        if mode == "ls":
            print(f"{len(videos)} videos in session.")
            for i, vid in enumerate(videos):
                color = "green" if i == workon else "white"
                prefix = "* " if i == workon else "  "
                print(colored(f"{prefix}{i}. fps={vid.fps}, resolution={vid.resolution}", color))

        elif mode == "workon":
            if len(opts) >= 1 and opts[0].isdigit():
                num = int(opts[0])
                if 0 <= num < len(videos):
                    workon = num
                else:
                    print("Number out of range.")
            else:
                print("Invalid argument number or format.")
