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
Block rendering.

Will register:

* Property group ``blocks_props``
* Operator group ``blocks_ops``
* Job ``blocks_job``
"""

import numpy as np
import pv
from pv.props import FloatProp
from pvkernel import Video
from pvkernel import draw


class BUILTIN_PT_Blocks(pv.types.PropertyGroup):
    idname = "blocks_props"

    block_speed = FloatProp(
        name="Block Speed",
        description="Screens per second speed.",
        default=0.2
    )


class BUILTIN_OT_BlocksRender(pv.types.Operator):
    group = "blocks_ops"
    idname = "render"
    label = "Render Blocks"
    description = "The operator that will be run in a job."

    def execute(self, video: Video) -> None:
        frame = video.frame
        height = video.resolution[1]
        threshold = height / 2
        speed = video.blocks_props.block_speed * height / video.fps

        first_note = min(video.midi_data.notes, key=lambda n: n.start).start
        for note in video.midi_data.notes:
            start = note.start - first_note - frame
            end = note.end - first_note - frame
            top = threshold - end*speed
            bottom = threshold - start*speed

            if not (bottom < 0 or top > threshold):
                x, width = video.core_data.key_pos[note.note]
                bottom = min(bottom, threshold+10)
                draw_block(video.render_img, (x, top, width, bottom-top))


class BUILTIN_JT_Blocks(pv.types.Job):
    idname = "blocks_job"
    ops = ("blocks_ops.render",)


def draw_block(img: np.ndarray, rect):
    draw.rect(img, (255, 255, 255, 200), rect, border_radius=5)
    draw.rect(img, (255, 255, 255, 255), rect, border_radius=5, border=3)


classes = (
    BUILTIN_PT_Blocks,
    BUILTIN_OT_BlocksRender,
    BUILTIN_JT_Blocks,
)

def register():
    for cls in classes:
        pv.utils.register_class(cls)
