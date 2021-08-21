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

* Property group ``blocks``
* Operator group ``blocks``
* Job ``blocks``
"""

import numpy as np
import pv
from pv.props import BoolProp, FloatProp, ColorProp
from pvkernel import Video
from pvkernel import draw
from utils import block_pos, first_note


class BUILTIN_PT_Blocks(pv.PropertyGroup):
    idname = "blocks"

    speed = FloatProp(
        name="Block Speed",
        description="Screens per second speed.",
        default=0.2,
    )

    rounding = FloatProp(
        name="Rounding",
        description="Corner rounding radius in pixels.",
        default=5,
    )

    border = FloatProp(
        name="Border",
        description="Border thickness in pixels.",
        default=1,
    )

    glow = BoolProp(
        name="Glow",
        description="Whether to add glow to the blocks.",
        default=True,
    )

    color = ColorProp(
        name="Inside Color",
        description="Color of the inside of the block.",
        default=[128, 200, 218, 255],
    )

    border_color = ColorProp(
        name="Border Color",
        description="Color of the border.",
        default=[255, 255, 255, 255],
    )

    glow_color = ColorProp(
        name="Glow Color",
        description="Color of the glow.",
        default=[255, 255, 255, 150],
    )


class BUILTIN_OT_BlocksRender(pv.Operator):
    group = "blocks"
    idname = "render"
    label = "Render Blocks"
    description = "The operator that will be run in a job."

    def execute(self, video: Video) -> None:
        height = video.resolution[1]
        threshold = height / 2
        first = first_note(video)

        for note in video.data.midi.notes:
            top, bottom = block_pos(video, note, first)
            if not (bottom < 0 or top > threshold):
                x, width = video.data.core.key_pos[note.note]
                bottom = min(bottom, threshold+10)
                draw_block(video, (x, top, width, bottom-top))


class BUILTIN_JT_Blocks(pv.Job):
    idname = "blocks"
    ops = ("blocks.render",)


def draw_block(video: Video, rect):
    props = video.props.blocks
    rounding = props.rounding

    if props.glow:
        new_rect = (rect[0]-2, rect[1]-2, rect[2]+4, rect[3]+4)
        draw.rect(video.render_img, props.glow_color, new_rect, border_radius=rounding)
    draw.rect(video.render_img, props.color, rect, border_radius=rounding)
    if props.border > 0:
        draw.rect(video.render_img, props.border_color, rect, border=props.border, border_radius=rounding)


classes = (
    BUILTIN_PT_Blocks,
    BUILTIN_OT_BlocksRender,
    BUILTIN_JT_Blocks,
)

def register():
    for cls in classes:
        pv.utils.register_class(cls)
