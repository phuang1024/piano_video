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

import io
import struct
from typing import List
from .utils import UI32
from .props import Property


class PropertyGroup:
    idname: str
    props: List[Property]

    def dump(self, stream: io.BytesIO) -> None:
        stream.write(struct.pack(UI32, len(self.idname)))
        stream.write(self.idname.encode())
        stream.write(struct.pack(UI32, len(self.props)))
        for prop in self.props:
            prop.dump(stream)

    def load(self, stream: io.BytesIO) -> None:
        num_props = struct.unpack(UI32, stream.read(4))[0]
        for _ in range(num_props):
            type_id = stream.read(1)[0]
            idname = stream.read(struct.unpack(UI32, stream.read(4))[0]).decode()
            for prop in self.props:
                if prop.idname == idname:
                    if prop.type_id != type_id:
                        raise ValueError(f"Incorrect type ID on {self.idname}.{idname}:" + \
                            f"Expected {prop.type_id}, got {type_id} from stream.")
                    prop.load(stream)
                    break
