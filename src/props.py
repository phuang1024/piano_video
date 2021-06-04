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

import struct
from typing import Any, Literal
from utils import *


class Property:
    pass


class Property:
    type_id: int

    idname: str
    label: str
    description: str

    default: Any
    value: Any

    def __init__(self, *args) -> None:...

    def _pack_header(self) -> bytes:
        data = b""
        data += bytes([self.type_id])
        data += struct.pack(I32, len(self.idname))
        data += self.idname.encode()
        return data

    def tobytes(self) -> bytes:...
    def frombytes(cls, data: bytes) -> None:...


class BoolProp(Property):
    type_id: Literal[0] = 0
    default: bool
    value: bool

    def __init__(self, idname: str = "", label: str = "", description: str = "",
            default: bool = False, value: bool = ...) -> None:
        self.label = label
        self.description = description
        self.idname = idname

        self.default = default
        self.value = default if value is ... else value

    def tobytes(self) -> bytes:
        return bytes([self.default, self.value])

    def frombytes(self, data: bytes) -> None:
        default, value = data
        self.default = default
        self.value = value
