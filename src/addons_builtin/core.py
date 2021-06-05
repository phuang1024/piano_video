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
Contains core properties, operators, and UI,
such as output properties.
"""

import pv
from pv.props import *


class OUTPUT_PT_Props(pv.types.PropertyGroup):
    idname = "output"

    props = [
        IntProp(
            idname="res_x",
            label="X Resolution",
            description="Resolution (pixels) of output X",
            default=1920, min=1, max=65536,
        ),

        IntProp(
            idname="res_y",
            label="Y Resolution",
            description="Resolution (pixels) of output Y",
            default=1080, min=1, max=65536,
        ),

        IntProp(
            idname="fps",
            label="FPS",
            description="Output frames per second",
            default=30, min=1, max=1000,
        )
    ]


class OUTPUT_UT_Section(pv.types.UISection):
    idname = "output"
    label = "Output"
    description = "Output parameters"


class OUTPUT_UT_Dimensions(pv.types.UIPanel):
    idname = "dimensions"
    label = "Dimensions"
    description = "Dimensions of the output (both spatial and temporal)"
    section_id = "output"

    def draw(self) -> None:
        layout = self.layout
        layout.prop("output.res_x")
        layout.prop("output.res_y")
        layout.prop("output.fps")


classes = (
    OUTPUT_PT_Props,
    OUTPUT_UT_Section,
    OUTPUT_UT_Dimensions,
)

def register():
    for cls in classes:
        pv.utils.register_class(cls)

def unregister():
    for cls in classes:
        pv.utils.unregister_class(cls)
