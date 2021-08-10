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

import pv
from pv.props import FloatProp
from pvkernel import Video
from pvkernel.lib import *
from pvkernel.utils import CUDA

if CUDA and False:
    NotImplemented
else:
    LIB.glare.argtypes = (IMG, I32, I32, F64, F64, AR_UCH, UCH, F64, F64)


class GLARE_PT_Props(pv.types.PropertyGroup):
    idname = "glare_props"

    intensity = FloatProp(
        name="Intensity",
        description="Glare brightness multiplier.",
        default=0.5,
    )

    radius = FloatProp(
        name="Radius",
        description="Glare radius in pixels.",
        default=150,
    )


class GLARE_OT_Apply(pv.types.Operator):
    group = "glare_ops"
    idname = "apply"
    label = "Apply Glare"
    description = "Render glare on the render image."

    def execute(self, video: Video) -> None:
        pass


class GLARE_JT_Job(pv.types.Job):
    idname = "glare_job"
    ops = ("glare_ops.apply")


classes = (
    GLARE_PT_Props,
    GLARE_OT_Apply,
    GLARE_OT_Apply,
)

def register():
    for cls in classes:
        pv.utils.register_class(cls)
