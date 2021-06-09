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
from typing import Dict, List, Tuple, Union
pygame.init()

mpos: Tuple[int, int]             # Mouse pos
mdowns: List[int]                 # MOUSEBUTTONDOWN events
mpress: Tuple[bool, bool, bool]   # Mouse pressed
mtime: float                      # Seconds the mouse has been in the current pos

kdowns: List[int]                 # KEYDOWN events
kpress: Dict[int, bool]           # Keys pressed, actually is pygame.key.ScancodeWrapper

tooltip: Union[Tuple[Tuple[int, int], str, str], None]   # [[mx, my], header, text]

tooltip = None
