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

import numpy as np
import pv
from pv.props import BoolProp, FloatProp, ListProp
from pvkernel import Video

# Light type constants
LIGHT_POINT = 0


class KEYBOARD_PT_Studio(pv.PropertyGroup):
    idname = "lighting"

    on = BoolProp(
        name="On",
        description="Whether to use CG lighting.",
        default=True,
    )

    piano_width = FloatProp(
        name="Piano Width",
        description="Lowest key to highest key distance in meters.",
        default=1.2,
    )

    lights = ListProp(
        name="Lights",
        description="List of lights. See docs for more info.",
        default=[],
    )


def apply_point(video: Video, img: np.ndarray, x, y, z, bright):
    pass


def apply_lighting(video: Video, img: np.ndarray):
    #TODO DOCS
    props = video.props.lighting

    if not props.on:
        return

    for type, x, y, z, bright in props.lights:
        if type == 0:
            apply_point(video, img, x, y, z, bright)
        else:
            print(f"WARNING: Unrecognized light type: {type}")


classes = (
    KEYBOARD_PT_Studio,
)

def register():
    for cls in classes:
        pv.utils.register_class(cls)
