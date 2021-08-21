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

"""
Core properties and operators.

Will register:

* Property group ``keyboard``
"""

import pv
from pv.props import FloatProp, StrProp
from pvkernel import Video


class KEYBOARD_PT_Props(pv.PropertyGroup):
    idname = "keyboard"

    left_offset = FloatProp(
        name="Left Offset",
        description="Piano left side pixel offset.",
        default=0,
    )

    right_offset = FloatProp(
        name="Right Offset",
        description="Piano right side pixel offset",
        default=0,
    )

    black_width_fac = FloatProp(
        name="Black Width Factor",
        description="Black key width factor respective to white key.",
        default=0.5,
    )

    video_path = StrProp(
        name="Path",
        description="Video file path",
    )

    video_start = FloatProp(
        name="Video Start",
        description="Time you start playing in the video in seconds",
    )


class KEYBOARD_OT_Render(pv.Operator):
    group = "keyboard"
    idname = "render"
    label = "Render"
    description = "Render keyboard on render image."

    def execute(self, video: Video) -> None:
        pass


class KEYBOARD_JT_Init(pv.Job):
    idname = "keyboard_init"

    def execute(self, video: Video) -> None:
        pass


classes = (
    KEYBOARD_PT_Props,
)

def register():
    for cls in classes:
        pv.utils.register_class(cls)
