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

"""
Read and write scene.
"""

import struct
import pv
from pv.props import *


class FILEIO_OT_SaveScene(pv.types.Operator):
    idname = "io.save_scene"
    label = "Save Scene"
    description = "Save scene as a binary file"

    args = [
        StringProp(
            idname="path",
            label="File Path",
            description="Path to save scene"
        )
    ]

    def poll(self):
        return isinstance(pv.context.scene, pv.types.Scene)

    def execute(self) -> str:
        try:
            with open(self.path, "wb") as file:
                for pgroup in pv.context.scene.pgroups:
                    file.write(struct.pack("<I", len(pgroup.idname)))
                    file.write(pgroup.idname.encode())
                    pgroup.dump(file)

        except FileNotFoundError:
            return "CANCELLED"

        return "FINISHED"


classes = (
    FILEIO_OT_SaveScene,
)

def register():
    for cls in classes:
        pv.utils.register_class(cls)

def unregister():
    for cls in classes:
        pv.utils.unregister_class(cls)
