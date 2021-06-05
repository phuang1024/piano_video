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

    def __getattr__(self, attr: str) -> Property:
        if hasattr(self, attr):
            return getattr(self, attr)

        for prop in self.props:
            if prop.idname == attr:
                return prop
        raise ValueError(f"PropertyGroup {self.idname} has no property {attr}")

    def dump(self, stream: io.BytesIO) -> None:
        """
        Writes number of props as unsigned 32 bit integer.
        Then, writes header and data for each prop.
        """
        stream.write(struct.pack(UI32, len(self.props)))
        for prop in self.props:
            prop.dump_header(stream)
            prop.dump(stream)

    def load(self, stream: io.BytesIO) -> None:
        """
        Loads number of props.
        Then reads header and calls load on each corresponding prop.
        Will raise ValueError if a type ID is incorrect.
        """
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


class UILayout:
    pass


class UIPanel:
    idname: str
    label: str
    description: str

    layout: UILayout

    def __init__(self):
        self.layout = UILayout()


class UISection:
    idname: str
    label: str
    description: str
    icon: str

    panels: List[UIPanel]


class Scene:
    pgroups: List[PropertyGroup]

    def __init__(self) -> None:
        self.pgroups = []

    def __getattr__(self, attr: str) -> PropertyGroup:
        if hasattr(self, attr):
            return getattr(self, attr)

        for group in self.pgroups:
            if group.idname == attr:
                return group
        raise ValueError(f"Scene has no PropertyGroup {attr}")


class Context:
    scene: Scene

    def __init__(self) -> None:
        self.scene = Scene()
