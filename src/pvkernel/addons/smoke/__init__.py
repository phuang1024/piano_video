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

if CUDA and False:
    pass
else:
    LIB.smoke_sim.argtypes = (F64, I32, I32, AR_DBL, AR_DBL, *[F32 for _ in range(5)], AR_CH, AR_CH)
    sim_func = LIB.smoke_sim


class SMOKE_PT_Props(pv.PropertyGroup):
    idname = "smoke"

    intensity = FloatProp(
        name="Intensity",
        description="Smoke opacity multiplier.",
        default=1,
    )

    pps = FloatProp(
        name="Particles/Second",
        description="Amount of smoke particles to emit per second per note.",
        default=3000,
    )


class SMOKE_OT_Apply(pv.Operator):
    group = "smoke"
    idname = "apply"
    label = "Apply Smoke"
    description = "Render smoke on the render image."

    def execute(self, video: Video) -> None:
        cache: pv.Cache = video.caches.smoke
        frame = video.frame

        in_path = cache.frame_path(frame-1) if cache.frame_exists(frame-1) else ""
        out_path = cache.frame_path(frame)
        in_path = in_path.encode() + b"\x00"
        out_path = out_path.encode() + b"\x00"
        in_path = np.array([x for x in in_path], dtype=np.int8)
        out_path = np.array([x for x in out_path], dtype=np.int8)
        cache.fp_frame("w").close()

        ppf = int(video.props.smoke.pps / video.fps)

        key_starts = []
        key_ends = []
        for note in video.data.midi.notes_playing:
            x, width = video.data.core.key_pos[note]
            key_starts.append(x)
            key_ends.append(x+width)
        key_starts = np.array(key_starts, dtype=np.float64)
        key_ends = np.array(key_ends, dtype=np.float64)

        sim_func(video.fps, ppf, key_starts.shape[0], key_starts, key_ends, video.resolution[1]/2,
            -2, 2, -5, -8, in_path, out_path)


class SMOKE_JT_Job(pv.Job):
    idname = "smoke"
    ops = ("smoke.apply",)


class SMOKE_CT_Cache(pv.Cache):
    idname = "smoke"
    depends = ("smoke.pps",)


classes = (
    SMOKE_PT_Props,
    SMOKE_OT_Apply,
    SMOKE_JT_Job,
    SMOKE_CT_Cache,
)

def register():
    for cls in classes:
        pv.utils.register_class(cls)
