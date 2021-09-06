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

import numpy as np
import pv
from pv.props import FloatProp
from pvkernel import Video
from pvkernel.lib import *

sim_args = (F64, I32, I32, I32, AR_DBL, AR_DBL, F64, AR_CH, AR_CH, I32, I32)
render_args = (IMG, I32, I32, AR_CH, F64)
LIB.ptcl_sim.argtypes = sim_args
LIB.ptcl_render.argtypes = render_args
sim_func = LIB.ptcl_sim
render_func = LIB.ptcl_render


class PTCLS_PT_Props(pv.PropertyGroup):
    idname = "ptcls"

    intensity = FloatProp(
        name="Intensity",
        description="Particle brightness multiplier.",
        default=1,
    )

    attraction = FloatProp(   # currently not used
        name="Attraction",
        description="Multiplier for how much particles clump up",
        default=1,
    )

    pps = FloatProp(
        name="Particles/Second",
        description="Amount of particles to emit per second per note.",
        default=200,
    )


class PTCLS_OT_Apply(pv.Operator):
    group = "ptcls"
    idname = "apply"
    label = "Apply Particles"
    description = "Render particles on the render image."

    def execute(self, video: Video) -> None:
        simulate(video)
        render(video)


class PTCLS_JT_Job(pv.Job):
    idname = "ptcls"
    ops = ("ptcls.apply",)


class PTCLS_CT_Cache(pv.Cache):
    idname = "ptcls"
    depends = ("ptcls.attraction", "ptcls.pps")


def get_cpath(cache: pv.Cache, frame, default="", check_exist=True):
    if check_exist:
        path = cache.frame_path(frame) if cache.frame_exists(frame) else default
    else:
        path = cache.frame_path(frame)
    return cpath(path)

def simulate(video: Video):
    """Call ptcls simulation library."""
    cache: pv.Cache = video.caches.ptcls
    frame = video.frame

    in_path = get_cpath(cache, frame-1)
    out_path = get_cpath(cache, frame, check_exist=False)
    cache.fp_frame("w").close()

    ppf = int(video.props.ptcls.pps / video.fps)

    key_starts = []
    key_ends = []
    for note in video.data.midi.notes_playing:
        x, width = video.data.core.key_pos[note]
        key_starts.append(x+5)
        key_ends.append(x+width-5)
    key_starts = np.array(key_starts, dtype=np.float64)
    key_ends = np.array(key_ends, dtype=np.float64)

    sim_func(video.fps, video.frame, ppf, key_starts.shape[0], key_starts, key_ends, video.resolution[1]/2,
        in_path, out_path, *video.resolution)


def render(video: Video):
    """Call ptcls render library."""
    cache: pv.Cache = video.caches.ptcls
    frame = video.frame

    path = get_cpath(cache, frame)
    render_func(video.render_img, *video.resolution, path, video.props.ptcls.intensity*0.7)


classes = (
    PTCLS_PT_Props,
    PTCLS_OT_Apply,
    PTCLS_JT_Job,
    PTCLS_CT_Cache,
)

def register():
    for cls in classes:
        pv.utils.register_class(cls)
