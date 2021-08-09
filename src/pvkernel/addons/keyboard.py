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

* Property group ``piano_props``
"""

import pv
from pv.props import FloatProp
from pvkernel import Video


class BUILTIN_PT_Piano(pv.types.PropertyGroup):
    idname = "piano_props"

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
        default=0.35,
    )


classes = (
    BUILTIN_PT_Piano,
)

def register():
    for cls in classes:
        pv.utils.register_class(cls)
