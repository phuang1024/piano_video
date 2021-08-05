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

from typing import Any, Union
from .props import BoolProp, Property


class PropertyGroup:
    """
    A collection of Properties.

    When creating your own PropertyGroup, you will inherit a class from
    this base class. Then, define:
    
    * ``idname``: The unique idname of this property group.
    * properties: Define each property as a static attribute (shown below).

    .. code-block:: py

        class MyProps(pv.types.PropertyGroup):
            prop1 = pv.props.BoolProp(name="hi")
    """

    def __getattribute__(self, name: str) -> Union[Property, Any]:
        attr = object.__getattribute__(self, name)
        if isinstance(attr, Property):
            return attr.value
        else:
            return attr
