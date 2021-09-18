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
"""

pv_info = {
    "idname": "blocks",
    "name": "Blocks",
    "description": "Built-in block rendering.",
    "author": "Patrick Huang",
    "version": (0, 1, 0),
    "pv": (0, 4, 0),
    "url": "https://github.com/phuang1024/piano_video",
}

import numpy as np
import pv
from pv.props import BoolProp, FloatProp, ListProp, StrProp
from pvkernel import Video
from .solid import draw_block_solid


class BUILTIN_PT_Blocks(pv.PropertyGroup):
    idname = "blocks"

    speed = FloatProp(
        name="Block Speed",
        description="Screens per second speed.",
        default=0.2,
    )

    style = StrProp(
        name="Style",
        description="Block style.",
        default="SOLID",
        choices=["SOLID"],
    )

    x_offset = FloatProp(
        name="X Offset",
        description="Horizontal offset of blocks.",
        default=0,
    )

    dim_top = BoolProp(
        name="Dim Top",
        description="Whether to dim pixels near the top of the screen",
        default=True,
    )

    octave_lines = BoolProp(
        name="Octave Lines",
        description="Whether to draw vertical lines at each octave.",
        default=True,
    )


class BUILTIN_PT_BlocksSolid(pv.PropertyGroup):
    idname = "blocks_solid"

    rounding = FloatProp(
        name="Rounding",
        description="Corner rounding radius in pixels.",
        default=8,
    )

    border = FloatProp(
        name="Border",
        description="Border thickness in pixels.",
        default=0.5,
    )

    glow = BoolProp(
        name="Glow",
        description="Whether to add glow to the blocks.",
        default=True,
    )

    color = ListProp(
        name="Inside Color",
        description="RGBA color of the inside of the block.",
        default=[195, 165, 50, 255],
    )

    border_color = ListProp(
        name="Border Color",
        description="RGBA color of the border.",
        default=[220, 210, 210, 255],
    )

    glow_color = ListProp(
        name="Glow Color",
        description="Color of the glow.",
        default=[255, 220, 200, 90],
    )


class BUILTIN_OT_BlocksRender(pv.Operator):
    group = "blocks"
    idname = "render"
    label = "Render Blocks"
    description = "The operator that will be run in a job."

    def execute(self, video: Video) -> None:
        props = video.props.blocks
        half = video.resolution[1] // 2

        if props.style == "SOLID":
            draw_block_solid(video)
        else:
            raise ValueError(f"Unknown block style: {props.style}")

        if props.dim_top:
            for y in range(250):
                v = np.interp(y, [0, 250], [0.65, 1])
                video.render_img[y, ...] = video.render_img[y, ...] * v

        if props.octave_lines:
            for note in range(3, 88, 12):
                x, _ = video.data.core.key_pos[note]
                for y in range(half):
                    for ch in range(3):
                        video.render_img[y, int(x), ch] = max(video.render_img[y, int(x), ch], 55)


class BUILTIN_JT_Blocks(pv.Job):
    idname = "blocks"
    ops = ("blocks.render",)


classes = (
    BUILTIN_PT_Blocks,
    BUILTIN_PT_BlocksSolid,
    BUILTIN_OT_BlocksRender,
    BUILTIN_JT_Blocks,
)

def register():
    for cls in classes:
        pv.utils.register_class(cls)
