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
Smoke effects.
"""

import numpy as np
import pv
from pv.props import FloatProp
from pvkernel import Video
from pvkernel.lib import *
from pvkernel.utils import CUDA


class SMOKE_PT_Props(pv.PropertyGroup):
    idname = "smoke"

    intensity = FloatProp(
        name="Intensity",
        description="Smoke opacity multiplier.",
        default=1,
    )

    pps = FloatProp(
        name="Particles/Second",
        description="Amount of smoke particles to emit per second.",
        default=1000,
    )


class SMOKE_OT_Apply(pv.Operator):
    group = "smoke"
    idname = "apply"
    label = "Apply Smoke"
    description = "Render smoke on the render image."

    def execute(self, video: Video) -> None:
        return super().execute(video)


classes = (
    SMOKE_PT_Props,
    SMOKE_OT_Apply,
)

def register():
    for cls in classes:
        pv.utils.register_class(cls)
