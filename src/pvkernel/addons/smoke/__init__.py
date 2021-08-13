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
from pv.props import BoolProp, FloatProp
from pvkernel import Video
from pvkernel.lib import *
from pvkernel.utils import CUDA

sim_args = (F64, I32, I32, AR_DBL, AR_DBL, *[F64 for _ in range(5)], AR_CH, AR_CH, I32, I32)
render_args = (IMG, I32, I32, AR_CH, F64)
if CUDA and False:
    CULIB.smoke_sim.argtypes = sim_args
    CULIB.smoke_render.argtypes = render_args
    sim_func = CULIB.smoke_sim
    render_func = CULIB.smoke_render
else:
    LIB.smoke_sim.argtypes = sim_args
    LIB.smoke_render.argtypes = render_args
    sim_func = LIB.smoke_sim
    render_func = LIB.smoke_render


class SMOKE_PT_Props(pv.PropertyGroup):
    idname = "smoke"

    intensity = FloatProp(
        name="Intensity",
        description="Smoke opacity multiplier.",
        default=0.25,
    )

    pps = FloatProp(
        name="Particles/Second",
        description="Amount of smoke particles to emit per second per note.",
        default=20000,
    )

    diffusion = BoolProp(
        name="Diffusion",
        description="Whether to simulate diffusion. Will be slow.",
        default=False,
    )


class SMOKE_OT_Apply(pv.Operator):
    group = "smoke"
    idname = "apply"
    label = "Apply Smoke"
    description = "Render smoke on the render image."

    def execute(self, video: Video) -> None:
        simulate(video)
        render(video)


class SMOKE_JT_Job(pv.Job):
    idname = "smoke"
    ops = ("smoke.apply",)


class SMOKE_CT_Cache(pv.Cache):
    idname = "smoke"
    depends = ("smoke.pps",)


def get_cpath(cache: pv.Cache, frame, default="", check_exist=True):
    if check_exist:
        path = cache.frame_path(frame) if cache.frame_exists(frame) else default
    else:
        path = cache.frame_path(frame)
    path = path.encode() + b"\x00"
    path = np.array([x for x in path], dtype=np.int8)
    return path


def simulate(video: Video):
    """Call smoke simulation library."""
    cache: pv.Cache = video.caches.smoke
    frame = video.frame

    in_path = get_cpath(cache, frame-1)
    out_path = get_cpath(cache, frame, check_exist=False)
    cache.fp_frame("w").close()

    ppf = int(video.props.smoke.pps / video.fps)

    key_starts = []
    key_ends = []
    for note in video.data.midi.notes_playing:
        x, width = video.data.core.key_pos[note]
        key_starts.append(x+5)
        key_ends.append(x+width-5)
    key_starts = np.array(key_starts, dtype=np.float64)
    key_ends = np.array(key_ends, dtype=np.float64)

    sim_func(video.fps, ppf, key_starts.shape[0], key_starts, key_ends, video.resolution[1]/2,
        -10, 10, -75, -50, in_path, out_path, *video.resolution, video.props.smoke.diffusion)


def render(video: Video):
    """Call smoke render library."""
    cache: pv.Cache = video.caches.smoke
    frame = video.frame

    path = get_cpath(cache, frame)
    render_func(video.render_img, *video.resolution, path, video.props.smoke.intensity)


classes = (
    SMOKE_PT_Props,
    SMOKE_OT_Apply,
    SMOKE_JT_Job,
    SMOKE_CT_Cache,
)

def register():
    for cls in classes:
        pv.utils.register_class(cls)
