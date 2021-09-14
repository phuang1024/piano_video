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

import sys
import os
import argparse

try:
    import pv
    import pvkernel
except ModuleNotFoundError:
    print("pvgui: error importing one or more of \"pv\", \"pvkernel\"")
    print("pvgui: exiting")
    sys.exit(1)

from cli import cli
from gui import gui

VERSION = "0.4.0"


def main():
    parser = argparse.ArgumentParser(description="Piano Video GUI.")
    parser.add_argument("-c", "--cli", action="store_true", help="Launch CLI mode.")
    args = parser.parse_args()

    if args.cli:
        cli()
    else:
        gui()


main()
