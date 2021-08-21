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

__all__ = (
    "Property",
    "BoolProp",
    "IntProp",
    "FloatProp",
    "StrProp",
    "ListProp",
)

from typing import Any, List, Type


class Property:
    """
    Base property class.

    Inherit and define:

    * ``type``: Type.
    * ``set(value)``: Set the property's value. Default just sets it,
      but you may need to check requirements.

    **Call** ``super().__init__()`` **AFTER initializing** ``self.default``
    """
    type: Type
    name: str
    description: str

    default: Any
    value: Any

    def __init__(self):
        self.value = self.default

    def set(self, value: Any) -> None:
        """
        Sets the property's value.

        :param value: Any value. Will be casted with ``self.type``.
        :return: None
        """
        self.value = self.type(value)


class BoolProp(Property):
    """
    Boolean property.
    """
    type = bool

    def __init__(self, name: str = "", description: str = "", default: bool = False) -> None:
        self.name = name
        self.description = description
        self.default = default

        super().__init__()


class IntProp(Property):
    """
    Integer property.
    """
    type = int
    min: int
    max: int

    def __init__(self, name: str = "", description: str = "", default: int = 0,
            min: int = ..., max: int = ...) -> None:
        self.name = name
        self.description = description
        self.default = default
        self.min = min
        self.max = max

        super().__init__()

    def set(self, value: Any) -> None:
        self.value = max(min(self.type(value), self.max), self.min)


class FloatProp(Property):
    """
    Float property.
    """
    type = float
    min: float
    max: float

    def __init__(self, name: str = "", description: str = "", default: float = 0,
            min: float = ..., max: float = ...) -> None:
        self.name = name
        self.description = description
        self.default = default
        self.min = min
        self.max = max

        super().__init__()

    def set(self, value: Any) -> None:
        self.value = max(min(self.type(value), self.max), self.min)


class StrProp(Property):
    """
    String property.
    """
    type = bool
    max_len: int

    def __init__(self, name: str = "", description: str = "", default: str = "",
            max_len: int = 1000) -> None:
        self.name = name
        self.description = description
        self.default = default
        self.max_len = max_len

        super().__init__()

    def set(self, value: Any) -> None:
        self.value = self.type(value)[:self.max_len]


class ListProp(Property):
    """
    List property. Use this for color.
    May contain a list of lists.
    """
    type = list

    def __init__(self, name: str = "", description: str = "", default: List[int] = [0, 0, 0, 0]):
        self.name = name
        self.description = description
        self.default = default

        super().__init__()
