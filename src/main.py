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


def setup_addons(action, verbose=False):
    printer = VerbosePrinter(verbose)
    if verbose:
        printer(f"Setup add-ons: {action}")

    for directory in ADDON_PATHS:
        if os.path.isdir(directory):
            printer(f"  Searching directory {directory}")
            sys.path.insert(0, directory)

            for file in os.listdir(directory):
                printer(f"    Found {file}")
                path = os.path.join(directory, file)

                valid = (os.path.isfile(path) and path.endswith(".py")) or \
                    (os.path.isdir(path) and "__init__.py" in os.listdir(path))
                if valid:
                    printer(f"      Setting up {file}")
                    mod = __import__(os.path.splitext(file)[0])
                    if hasattr(mod, "register"):
                        getattr(mod, action)()
                else:
                    printer(f"      Skipping {file}")

            sys.path.pop(0)

    printer(f"  Exiting add-on setup")


def test_modules(verbose=False):
    printer = VerbosePrinter(verbose)
    printer("Testing dependent modules")
    for mod in DEPENDENCIES:
        printer(f"  Importing \"{mod}\"")
        __import__(mod)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", action="store_true", help="Show the version of the program.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Display more information to stdout.")
    parser.add_argument("--test", action="store_true", help="Test API and modules. No GUI window will open.")
    args = parser.parse_args()

    if args.version:
        print(f"Piano Video v{VERSION}")
        print("Licensed under GNU GPL v3")
        return

    vb = args.verbose
    setup_addons("register", verbose=vb)
    if args.test:
        test_modules(verbose=vb)
    else:
        gui(verbose=vb)
    setup_addons("unregister", verbose=vb)


main()
