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
from typing import Literal


class Property:
    type_id: int

    idname: str
    label: str
    description: str

    def __init__(self, idname: str = "", label: str = "", description: str = "") -> None:
        self.idname = idname
        self.label = label
        self.description = description

    def dump(self, stream: io.BytesIO) -> None:...

    def load(self, stream: io.BytesIO) -> None:...


class BoolProp(Property):
    type_id: Literal[0] = 0

    default: bool
    value: bool

    def __init__(self, idname: str = "", label: str = "", description: str = "",
            default: bool = False, value: bool = False) -> None:
        super().__init__(idname, label, description)
        self.default = default
        self.value = default if value is None else value

    def dump(self, stream: io.BytesIO) -> None:
        stream.write(bytes([self.type_id, self.value]))

    def load(self, stream: io.BytesIO) -> None:
        assert stream.read(1)[0] == self.type_id, f"Type ID for BoolProp must be {self.type_id}"
        self.value = (stream.read(1) == b"\x01")
