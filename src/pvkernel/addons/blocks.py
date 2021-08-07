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

* PropertyGroup ``blocks_props``
* Operator group ``blocks_ops``
* Job ``blocks_job``
"""

import pv
from pvkernel import Video


class BUILTIN_PT_Blocks(pv.types.PropertyGroup):
    idname = "blocks_props"


class BUILTIN_OT_BlocksRender(pv.types.Operator):
    group = "blocks_ops"
    idname = "render"
    label = "Render Blocks"
    description = "The operator that will be run in a job."

    def execute(self, video: Video) -> None:
        video.render_img[:200, :200] = 255


class BUILTIN_JT_Blocks(pv.types.Job):
    idname = "blocks_job"
    ops = ("blocks_ops.render",)


classes = (
    BUILTIN_PT_Blocks,
    BUILTIN_OT_BlocksRender,
    BUILTIN_JT_Blocks,
)

def register():
    for cls in classes:
        pv.utils.register_class(cls)
