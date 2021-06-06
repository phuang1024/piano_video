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

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

import argparse
from gui import gui
from gui_utils import *


def setup_addons(action):
    for directory in ADDON_PATHS:
        if os.path.isdir(directory):
            sys.path.insert(0, directory)
            for file in os.listdir(directory):
                path = os.path.join(directory, file)
                if os.path.isfile(path) and path.endswith(".py"):
                    mod = __import__(os.path.splitext(file)[0])
                    if hasattr(mod, "register"):
                        getattr(mod, action)()

            sys.path.pop(0)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", action="store_true", help="Show the version of the program.")
    parser.add_argument("--test", action="store_true", help="Test API and modules. No GUI window will open.")
    args = parser.parse_args()

    if args.version:
        print(f"Piano Video v{VERSION}")
        print("Licensed under GNU GPL v3")
        return

    setup_addons("register")
    if not args.test:
        gui()
    setup_addons("unregister")


main()
