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
Output properties
"""

import pv
from pv.props import *


class KEYBOARD_UT_Section(pv.types.UISection):
    idname = "keyboard"
    label = "Keyboard"
    description = "Settings for the keyboard"
    icon = "piano.png"


classes = (
    KEYBOARD_UT_Section,
)

def register():
    for cls in classes:
        pv.utils.register_class(cls)

def unregister():
    for cls in classes:
        pv.utils.unregister_class(cls)
