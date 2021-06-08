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
from typing import Any, List
from .utils import UI32, I64, F64

NUM_MAX = 2 ** 32


class Property:
    """
    Base property class.
    All props (BoolProp, IntProp, etc...) inherit from this.
    """
    type_id: int

    idname: str
    label: str
    description: str

    default: Any
    value: Any

    def __init__(self, idname: str = "", label: str = "", description: str = "") -> None:
        self.idname = idname
        self.label = label
        self.description = description

    def dump_header(self, stream: io.BytesIO) -> None:
        stream.write(bytes([self.type_id]))
        stream.write(struct.pack(UI32, len(self.idname)))
        stream.write(self.idname.encode())

    def dump(self, stream: io.BytesIO) -> None:...

    def load(self, stream: io.BytesIO) -> None:...


class BoolProp(Property):
    """
    Boolean property.
    Type ID: 1
    """
    type_id: int = 1

    default: bool
    value: bool

    def __init__(self, idname: str = "", label: str = "", description: str = "",
            default: bool = False, value: bool = None) -> None:
        super().__init__(idname, label, description)
        self.default = default
        self.value = default if value is None else value

    def dump(self, stream: io.BytesIO) -> None:
        """
        Writes value as a byte (b"\\x00" or b"\\x01")
        """
        stream.write(bytes([self.value]))

    def load(self, stream: io.BytesIO) -> None:
        self.value = (stream.read(1) == b"\x01")


class IntProp(Property):
    """
    Integer property.
    The value is packed as a signed 64 bit integer (long long)
    Type ID: 2

    min: Minimum value (inclusive)
    max: Maximum value (inclusive)
    step: Value step (offset from default)
    """
    type_id: int = 2

    default: int
    value: int
    min: int
    max: int
    step: int

    def __init__(self, idname: str = "", label: str = "", description: str = "",
            default: int = 0, value: int = None, min: int = -NUM_MAX, max: int = NUM_MAX,
            step: int = 1) -> None:
        super().__init__(idname, label, description)
        self.default = default
        self.value = default if value is None else value
        self.max = max
        self.min = min
        self.step = step

    def dump(self, stream: io.BytesIO) -> None:
        """
        Writes value as a signed 64 bit integer.
        """
        stream.write(struct.pack(I64, self.value))

    def load(self, stream: io.BytesIO) -> None:
        self.value = struct.unpack(I64, stream.read(8))[0]


class FloatProp(Property):
    """
    Floating point property.
    The value is packed as a signed 64 bit float (double)
    Type ID: 2

    min: Minimum value (inclusive)
    max: Maximum value (inclusive)
    step: Value step (offset from default)
    """
    type_id: int = 3

    default: float
    value: float
    min: float
    max: float
    step: float

    def __init__(self, idname: str = "", label: str = "", description: str = "",
            default: float = 0, value: float = None, min: float = -NUM_MAX, max: float = NUM_MAX,
            step: float = 0.001) -> None:
        super().__init__(idname, label, description)
        self.default = default
        self.value = default if value is None else value
        self.max = max
        self.min = min
        self.step = step

    def dump(self, stream: io.BytesIO) -> None:
        """
        Writes value as a signed 64 bit float.
        """
        stream.write(struct.pack(F64, self.value))

    def load(self, stream: io.BytesIO) -> None:
        self.value = struct.unpack(F64, stream.read(8))[0]


class StringProp(Property):
    """
    String property.
    Type ID: 3

    max_len: Maximum length.
    password: Whether to display the string as asterisks (*)
    subtype: "" (normal), "FILE_PATH" (choose a file), "DIR_PATH" (choose a directory)
    """
    type_id: int = 4

    default: str
    value: str
    max_len: int
    password: bool
    subtype: str

    def __init__(self, idname: str = "", label: str = "", description: str = "",
            default: str = "", value: str = None, max_len: int = 200,
            password: bool = False, subtype: str = "") -> None:
        super().__init__(idname, label, description)
        self.default = default
        self.value = default if value is None else value
        self.max_len = max_len
        self.password = password
        self.subtype = subtype

    def dump(self, stream: io.BytesIO) -> None:
        """
        Writes length as a unsigned 32 bit integer.
        Then writes value as bytes.
        """
        stream.write(struct.pack(UI32, len(self.value)))
        stream.write(self.value.encode())

    def load(self, stream: io.BytesIO) -> None:
        length = struct.unpack(UI32, stream.read(4))[0]
        self.value = stream.read(length).decode()


class EnumProp(Property):
    """
    Enumerate Property (like a dropdown list).
    Type ID: 4

    items: List of (value, name, description) to show in the list.
    """
    type_id: int = 5

    default: str
    value: str
    items: List[List[str]]

    def __init__(self, idname: str = "", label: str = "", description: str = "",
            default: str = None, value: str = None, items: List = []) -> None:
        super().__init__(idname, label, description)
        self.default = items[0][0] if default is None else default
        self.value = self.default if value is None else value
        self.items = items

    def dump(self, stream: io.BytesIO) -> None:
        """
        Writes length of current value as a unsigned 32 bit integer.
        Then writes value as bytes.
        """
        stream.write(struct.pack(UI32, len(self.value)))
        stream.write(self.value.encode())

    def load(self, stream: io.BytesIO) -> None:
        length = struct.unpack(UI32, stream.read(4))[0]
        self.value = stream.read(length).decode()
