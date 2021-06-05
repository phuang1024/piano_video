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
import pygame
pygame.init()


def register_addons():
    for directory in ADDON_PATHS:
        if os.path.isdir(directory):
            sys.path.insert(0, directory)
            for file in os.listdir(directory):
                path = os.path.join(directory, file)
                if os.path.isfile(path) and path.endswith(".py"):
                    mod = __import__(os.path.splitext(file)[0])
                    if hasattr(mod, "register"):
                        mod.register()

            sys.path.pop(0)


# Global constants
VERSION = "0.1.0"
PARENT = os.path.dirname(os.path.realpath(__file__))
ADDON_PATHS = (
    os.path.join(PARENT, "addons_builtin"),
    os.path.join(PARENT, "addons_installed"),
)

# GUI
WIDTH, HEIGHT = 1280, 720
FPS = 60
IMAGES = {
    "icon": pygame.image.load(os.path.join(PARENT, "assets", "icon.jpg")),
}

BLACK = (0, 0, 0)
