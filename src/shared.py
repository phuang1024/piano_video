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

"""
Constant GUI values (eg. mouse_pos, keys_pressed)
that are updated every loop by main.

You can import this and access these values.
"""

import pygame
from typing import Dict, Tuple
pygame.init()

mouse_pos: Tuple[int, int]
mouse_pressed: Tuple[bool, bool, bool]
keys_pressed: Dict[int, bool]    # Actually is pygame.key.ScancodeWrapper
