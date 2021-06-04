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
from typing import Literal
from .utils import *


class Property:
    type_id: int

    idname: str
    label: str
    description: str

    def __init__(self, idname: str = "", label: str = "", description: str = "") -> None:
        self.idname = idname
        self.label = label
        self.description = description

    def check_type_id(self, stream: io.BytesIO) -> None:
        assert stream.read(1)[0] == self.type_id, f"Type ID for BoolProp must be {self.type_id}"

    def dump(self, stream: io.BytesIO) -> None:...

    def load(self, stream: io.BytesIO) -> None:...


class BoolProp(Property):
    type_id: Literal[1] = 1

    default: bool
    value: bool

    def __init__(self, idname: str = "", label: str = "", description: str = "",
            default: bool = False, value: bool = None) -> None:
        super().__init__(idname, label, description)
        self.default = default
        self.value = default if value is None else value

    def dump(self, stream: io.BytesIO) -> None:
        stream.write(bytes([self.type_id, self.value]))

    def load(self, stream: io.BytesIO) -> None:
        self.check_type_id(stream)
        self.value = (stream.read(1) == b"\x01")


class IntProp(Property):
    type_id: Literal[2] = 2

    default: int
    value: int
    min: int
    max: int
    step: int

    def __init__(self, idname: str = "", label: str = "", description: str = "",
            default: int = False, value: int = None, min: int = None, max: int = None,
            step: int = 1) -> None:
        super().__init__(idname, label, description)
        self.default = default
        self.value = default if value is None else value
        self.max = max
        self.min = min
        self.step = step

    def dump(self, stream: io.BytesIO) -> None:
        stream.write(bytes([self.type_id]))
        stream.write(struct.pack(I64, self.value))

    def load(self, stream: io.BytesIO) -> None:
        self.check_type_id(stream)
        self.value = struct.unpack(I64, stream.read(8))[0]


class FloatProp(Property):
    type_id: Literal[2] = 2

    default: float
    value: float
    min: float
    max: float
    step: float

    def __init__(self, idname: str = "", label: str = "", description: str = "",
            default: float = False, value: float = None, min: float = None, max: float = None,
            step: float = 0.001) -> None:
        super().__init__(idname, label, description)
        self.default = default
        self.value = default if value is None else value
        self.max = max
        self.min = min
        self.step = step

    def dump(self, stream: io.BytesIO) -> None:
        stream.write(bytes([self.type_id]))
        stream.write(struct.pack(F64, self.value))

    def load(self, stream: io.BytesIO) -> None:
        self.check_type_id(stream)
        self.value = struct.unpack(F64, stream.read(8))[0]
