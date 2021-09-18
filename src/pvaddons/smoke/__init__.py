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

pv_info = {
    "idname": "smoke",
    "name": "Smoke",
    "description": "Built-in smoke rendering.",
    "author": "Patrick Huang",
    "version": (0, 1, 0),
    "pv": (0, 4, 0),
    "url": "https://github.com/phuang1024/piano_video",
}

import numpy as np
import pv
from pv.props import BoolProp, FloatProp, ListProp
from pvkernel import Video
from pvkernel.lib import *
from pvkernel.utils import CUDA

sim_args = (F64, I32, I32, I32, AR_DBL, AR_DBL, *[F64 for _ in range(5)], AR_CH, AR_CH, I32, I32)
render_args = (IMG, I32, I32, AR_CH, F64, UCH, UCH, UCH)
LIB.smoke_sim.argtypes = sim_args
LIB.smoke_render.argtypes = render_args
sim_func = LIB.smoke_sim
render_func = LIB.smoke_render


class SMOKE_PT_Props(pv.PropertyGroup):
    idname = "smoke"

    on = BoolProp(
        name="Smoke On",
        description="Whether to use smoke effects",
        default=True,
    )

    intensity = FloatProp(
        name="Intensity",
        description="Smoke opacity multiplier.",
        default=1,
    )

    pps = FloatProp(
        name="Particles/Second",
        description="Amount of smoke particles to emit per second per note.",
        default=5500,
    )

    diffusion = BoolProp(
        name="Diffusion",
        description="Whether to simulate diffusion. Will be slow.",
        default=False,
    )

    color = ListProp(
        name="Smoke Color",
        description="RGB color of smoke.",
        default=[255, 255, 255],
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
    return cpath(path)


def simulate(video: Video):
    """Call smoke simulation library."""
    if not video.props.smoke.on:
        return

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

    sim_func(video.fps, video.frame, ppf, key_starts.shape[0], key_starts, key_ends, video.resolution[1]/2,
        -10, 10, -125, -100, in_path, out_path, *video.resolution, video.props.smoke.diffusion)


def render(video: Video):
    """Call smoke render library."""
    if not video.props.smoke.on:
        return

    cache: pv.Cache = video.caches.smoke
    frame = video.frame

    path = get_cpath(cache, frame)
    render_func(video.render_img, *video.resolution, path, video.props.smoke.intensity/7, *video.props.smoke.color)


classes = (
    SMOKE_PT_Props,
    SMOKE_OT_Apply,
    SMOKE_JT_Job,
    SMOKE_CT_Cache,
)

def register():
    for cls in classes:
        pv.utils.register_class(cls)
