#
#  Piano Video
#  Piano MIDI visualizer
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


class RENDER_DT_Preview(pv.types.DispDrawer):
    idname = "preview"

    def draw(self):
        pv.draw.circle(pv.disp.image, (255, 255, 255), (100, 100), 35)


classes = (
    RENDER_DT_Preview,
)

def register():
    for cls in classes:
        pv.utils.register_class(cls)
    pv.disp.current_drawer = "preview"

def unregister():
    for cls in classes:
        pv.utils.unregister_class(cls)
