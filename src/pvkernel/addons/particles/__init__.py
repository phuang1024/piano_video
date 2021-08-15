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
Particle effects.
"""

import pv
from pv.props import FloatProp
from pvkernel import Video


class PTCLS_PT_Props(pv.PropertyGroup):
    idname = "ptcls"

    intensity = FloatProp(
        name="Intensity",
        description="Particle brightness multiplier.",
        default=1,
    )

    attraction = FloatProp(
        name="Attraction",
        description="Multiplier for how much particles clump up",
        default=1,
    )

    pps = FloatProp(
        name="Particles/Second",
        description="Amount of particles to emit per second per note.",
        default=40,
    )


class PTCLS_OT_Apply(pv.Operator):
    group = "ptcls"
    idname = "apply"
    label = "Apply Particles"
    description = "Render particles on the render image."

    def execute(self, video: Video) -> None:
        pass


class PTCLS_JT_Job(pv.Job):
    idname = "ptcls"
    ops = ("ptcls.apply",)


class PTCLS_CT_Cache(pv.Cache):
    idname = "ptcls"
    depends = ("ptcls.attraction", "ptcls.pps")


classes = (
    PTCLS_PT_Props,
    PTCLS_OT_Apply,
    PTCLS_JT_Job,
    PTCLS_CT_Cache,
)

def register():
    for cls in classes:
        pv.utils.register_class(cls)
