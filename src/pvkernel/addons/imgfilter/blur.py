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

import pv
from pvkernel import Video


class IMGFILTER_OT_Blur(pv.Operator):
    group = "imgfilter"
    idname = "blur"
    label = "Blur"
    description = "Apply gaussian blur to the render image."

    def execute(self, video: Video) -> None:
        pass


classes = (
    IMGFILTER_OT_Blur,
)

def register():
    for cls in classes:
        pv.utils.register_class(cls)
