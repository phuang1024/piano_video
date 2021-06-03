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
import pygame
pygame.init()

# Global constants
VERSION = "0.1.0"
PARENT = os.path.dirname(os.path.realpath(__file__))

# GUI
WIDTH, HEIGHT = 1280, 720
FPS = 60
IMAGES = {
    "icon": pygame.image.load(os.path.join(PARENT, "assets", "icon.jpg")),
}

BLACK = (0, 0, 0)
