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
Apply glare when a key is pressed.
"""

import numpy as np
import pv
from pv.props import BoolProp, FloatProp
from pvkernel import Video
from pvkernel.lib import *

LIB.glare.argtypes = (IMG, I32, I32, F64, F64, AR_UCH, UCH, F64, F64, F64)


class GLARE_PT_Props(pv.PropertyGroup):
    idname = "glare"

    intensity = FloatProp(
        name="Intensity",
        description="Glare brightness multiplier.",
        default=1,
    )

    radius = FloatProp(
        name="Radius",
        description="Glare radius in pixels.",
        default=75,
    )

    jitter = FloatProp(
        name="Jitter",
        description="Amount to randomize intensity by.",
        default=0.1,
    )


class GLARE_OT_Apply(pv.Operator):
    group = "glare"
    idname = "apply"
    label = "Apply Glare"
    description = "Render glare on the render image."

    def execute(self, video: Video) -> None:
        width, height = video.resolution
        props = video.props.glare

        start = video.props.keyboard.left_offset
        end = video.props.keyboard.right_offset + width
        intensity = props.intensity
        radius = props.radius
        notes = np.array(video.data.midi.notes_playing, dtype=np.uint8)

        LIB.glare(video.render_img, width, height, intensity/2, radius,
            notes, notes.shape[0], start, end, props.jitter)


class GLARE_JT_Job(pv.Job):
    idname = "glare"
    ops = ("glare.apply",)


classes = (
    GLARE_PT_Props,
    GLARE_OT_Apply,
    GLARE_JT_Job,
)

def register():
    for cls in classes:
        pv.utils.register_class(cls)
