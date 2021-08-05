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

from typing import Any, Callable, List, Sequence, Type
from pv.types import DataGroup, PropertyGroup

_dgroups: List[Type[DataGroup]] = []
_dgroup_callback: List[Callable] = []
_pgroups: List[Type[PropertyGroup]] = []
_pgroup_callback: List[Callable] = []


def register_class(cls: Type) -> None:
    """
    Register a class to "apply" it to the kernel.
    """
    if issubclass(cls, PropertyGroup):
        _pgroups.append(cls)
        for func in _pgroup_callback:
            func(cls)

    elif issubclass(cls, DataGroup):
        _dgroups.append(cls)
        for func in _dgroup_callback:
            func(cls)

    else:
        raise ValueError(f"Cannot register {cls}")

def add_callback(func: Callable, classes: Sequence[str]) -> None:
    """
    Add a callback function when a class is registered.
    The function will be passed one argument, the class.

    :param func: Function to call.
    :param classes: A list of strings indicating which types of classes to listen for.
        Valid values:

        * "dgroup": DataGroup
        * "pgroup": PropertyGroup
    """
    classes = [s.lower() for s in classes]

    if "pgroup" in classes:
        _pgroup_callback.append(func)
    elif "dgroup" in classes:
        _dgroup_callback.append(func)


def get_exists(objs: Sequence[Any], idname: str) -> bool:
    """
    Check whether there is an object with idname ``idname``.
    """
    for o in objs:
        if o.idname == idname:
            return True
    return False

def get_index(objs: Sequence[Any], idname: str) -> int:
    """
    Return the index of the object in ``objs`` with idname ``idname``.
    """
    for i, o in enumerate(objs):
        if o.idname == idname:
            return i
    raise ValueError(f"No object with idname {idname}")

def get(objs: Sequence[Any], idname: str) -> Any:
    """
    Return the object in ``objs`` with idname ``idname``.
    """
    return objs[get_index(objs, idname)]


def _get_pgroups() -> List[Type[PropertyGroup]]:
    return _pgroups

def _get_dgroups() -> List[Type[DataGroup]]:
    return _dgroups
