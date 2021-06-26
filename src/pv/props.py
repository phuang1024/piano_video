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
from typing import Any, IO, List, Tuple, Type, Union
from .utils import UI32, I64, F64

NUM_MAX = 2 ** 32
SUPPORTED_COLLECTION_TYPES = (
    bool,
    int,
    float,
    str,
)


class Property:
    """
    Base property class.
    All props (BoolProp, IntProp, etc...) inherit from this.
    """
    type_id: int
    builtin_type: type

    idname: str
    label: str
    description: str

    default: Any
    value: Any

    def __init__(self, idname: str = "", label: str = "", description: str = "") -> None:
        self.idname = idname
        self.label = label
        self.description = description

    def dump_header(self, stream: IO[bytes]) -> None:
        stream.write(bytes([self.type_id]))
        stream.write(struct.pack(UI32, len(self.idname)))
        stream.write(self.idname.encode())

    def dump(self, stream: IO[bytes]) -> None:...

    def load(self, stream: IO[bytes]) -> None:...


class BoolProp(Property):
    """
    Boolean property.
    Type ID: 1
    """
    type_id: int = 1
    builtin_type: type = bool

    default: bool
    value: bool

    def __init__(self, idname: str = "", label: str = "", description: str = "",
            default: bool = False) -> None:
        super().__init__(idname, label, description)
        self.default = default
        self.value = default

    def dump(self, stream: IO[bytes]) -> None:
        """
        Writes value as a byte (b"\\x00" or b"\\x01")
        """
        stream.write(bytes([self.value]))

    def load(self, stream: IO[bytes]) -> None:
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
    builtin_type: type = int

    default: int
    value: int
    min: int
    max: int
    step: int

    def __init__(self, idname: str = "", label: str = "", description: str = "",
            default: int = 0, min: int = -NUM_MAX, max: int = NUM_MAX,
            step: int = 1) -> None:
        super().__init__(idname, label, description)
        self.default = default
        self.value = default
        self.max = max
        self.min = min
        self.step = step

    def dump(self, stream: IO[bytes]) -> None:
        """
        Writes value as a signed 64 bit integer.
        """
        stream.write(struct.pack(I64, self.value))

    def load(self, stream: IO[bytes]) -> None:
        self.value = struct.unpack(I64, stream.read(8))[0]


class FloatProp(Property):
    """
    Floating point property.
    The value is packed as a signed 64 bit float (double)
    Type ID: 3

    min: Minimum value (inclusive)
    max: Maximum value (inclusive)
    step: Value step (offset from default)
    """
    type_id: int = 3
    builtin_type: type = float

    default: float
    value: float
    min: float
    max: float
    step: float

    def __init__(self, idname: str = "", label: str = "", description: str = "",
            default: float = 0, min: float = -NUM_MAX, max: float = NUM_MAX,
            step: float = 0.001) -> None:
        super().__init__(idname, label, description)
        self.default = default
        self.value = default
        self.max = max
        self.min = min
        self.step = step

    def dump(self, stream: IO[bytes]) -> None:
        """
        Writes value as a signed 64 bit float.
        """
        stream.write(struct.pack(F64, self.value))

    def load(self, stream: IO[bytes]) -> None:
        self.value = struct.unpack(F64, stream.read(8))[0]


class StringProp(Property):
    """
    String property.
    Type ID: 4

    max_len: Maximum length.
    password: Whether to display the string as asterisks (*)
    subtype: "" (normal), "FILE_PATH" (choose a file), "DIR_PATH" (choose a directory)
    """
    type_id: int = 4
    builtin_type: type = str

    default: str
    value: str
    max_len: int
    password: bool
    subtype: str

    def __init__(self, idname: str = "", label: str = "", description: str = "",
            default: str = "", max_len: int = 200,
            password: bool = False, subtype: str = "") -> None:
        super().__init__(idname, label, description)
        self.default = default
        self.value = default
        self.max_len = max_len
        self.password = password
        self.subtype = subtype

    def dump(self, stream: IO[bytes]) -> None:
        """
        Writes length as a unsigned 32 bit integer.
        Then writes value as bytes.
        """
        stream.write(struct.pack(UI32, len(self.value)))
        stream.write(self.value.encode())

    def load(self, stream: IO[bytes]) -> None:
        length = struct.unpack(UI32, stream.read(4))[0]
        self.value = stream.read(length).decode()


class EnumProp(Property):
    """
    Enumerate Property (like a dropdown list).
    Type ID: 5

    items: List of (value, name, description) to show in the list.
    """
    type_id: int = 5
    builtin_type: type = tuple

    default: str
    value: str
    items: List[Tuple[str, str, str]]

    def __init__(self, idname: str = "", label: str = "", description: str = "",
            default: str = None, items: List[Tuple[str, str, str]] = []) -> None:
        super().__init__(idname, label, description)
        self.default = items[0][0] if default is None else default
        self.value = self.default
        self.items = items

    def dump(self, stream: IO[bytes]) -> None:
        """
        Writes length of current value as a unsigned 32 bit integer.
        Then writes value as bytes.
        """
        stream.write(struct.pack(UI32, len(self.value)))
        stream.write(self.value.encode())

    def load(self, stream: IO[bytes]) -> None:
        length = struct.unpack(UI32, stream.read(4))[0]
        self.value = stream.read(length).decode()


class CollectionProp(Property):
    """
    A collection of items.
    Type ID: 6

    item_type: The item type. Can either be builtin (int) or pv type (IntProp)
    items: List of stored items. Can be altered by the GUI.
    extendable: Whether the length can be changed by the user.
    ordered: Whether the collection is ordered.
    """
    type_id: int = 6
    builtin_type: type = list

    item_type: Type
    items: List[Any]
    extendable: bool
    ordered: bool

    def __init__(self, idname: str = "", label: str = "", description: str = "",
            item_type: Union[type, Property] = str, items: List[Any] = [], extendable: bool = True,
            ordered: bool = True) -> None:
        raise NotImplementedError("CollectionProp is not ready yet.")
        super().__init__(idname, label, description)
        self.item_type = item_type.builtin_type if isinstance(item_type, Property) else item_type
        self.items = items
        self.extendable = extendable
        self.ordered = ordered

        assert (not isinstance(item_type, EnumProp)), "Cannot have collection of EnumProps."
        assert (item_type in SUPPORTED_COLLECTION_TYPES or isinstance(item_type, Property)), \
            f"Collection type must be in {SUPPORTED_COLLECTION_TYPES}"
