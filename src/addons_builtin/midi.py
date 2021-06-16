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

pv_info = {
    "name": "Core MIDI",
    "description": "MIDI parsing properties.",
    "author": "Patrick Huang",
}

import pv
from pv.props import *


class MIDI_PT_Props(pv.types.PropertyGroup):
    idname = "midi"

    props = [
        IntProp(
            idname="offset",
            label="Offset",
            description="Offset in frames of MIDI. Increase this value to make MIDI play later.",
            default=0,
        ),
    ]


class MIDI_UT_Section(pv.types.UISection):
    idname = "midi"
    label = "MIDI"
    description = "Settings for MIDI"
    icon = "midi.png"


classes = (
    MIDI_PT_Props,
    MIDI_UT_Section,
)

def register():
    for cls in classes:
        pv.utils.register_class(cls)

def unregister():
    for cls in classes:
        pv.utils.unregister_class(cls)
