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

"""
Global utilities and constants for the module.
Used by components both inside the module and in third-party add-ons.
Avoid importing here, as it will likely result in a circular import.
"""

import os
import cv2
from typing import Any, Union

PARENT = os.path.dirname(os.path.realpath(__file__))
BUILTIN_ICON_PATHS = (
    os.path.join(PARENT, "assets"),
)

UI32 = "<I"
I32 = "<i"
I64 = "<q"
F32 = "f"
F64 = "d"


def register_class(cls: type) -> None:
    import pv

    inst = cls()
    if issubclass(cls, pv.types.PropertyGroup):
        if cls.idname.count(".") != 0:
            raise ValueError(f"PropertyGroup idname must not contain periods: {cls.idname}")
        pv.context.scene.pgroups.append(inst)

    elif issubclass(cls, pv.types.UISection):
        icon_path = None
        if hasattr(cls, "icon") and cls.icon:
            for directory in BUILTIN_ICON_PATHS:
                for file in os.listdir(directory):
                    if cls.icon == file:
                        icon_path = os.path.join(directory, file)
            if os.path.isfile(cls.icon):
                icon_path = cls.icon

        if icon_path is not None and os.path.isfile(icon_path):
            inst.icon_img = cv2.imread(icon_path)
        pv.context.ui_sections.append(inst)

    elif issubclass(cls, pv.types.UIPanel):
        get(pv.context.ui_sections, cls.section_id).panels.append(inst)


def unregister_class(cls: type) -> None:
    import pv
    context = pv.context
    scene = pv.context.scene

    if issubclass(cls, pv.types.PropertyGroup):
        scene.pgroups.pop(get(scene.pgroups, cls.idname, True))
    elif issubclass(cls, pv.types.UISection):
        context.ui_sections.pop(get(context.ui_sections, cls.idname, True))
    elif issubclass(cls, pv.types.UIPanel):
        section = get(pv.context.ui_sections, cls.section_id, raise_error=False)
        if section is not None:
            # Need to account for possibility that section is already unregistered
            section.pop(get(section.pgroups, cls.idname, True))


def get(items, idname, idx=False, raise_error=True, not_found_rval=None) -> Any:
    for i, item in enumerate(items):
        if item.idname == idname:
            return i if idx else item

    if raise_error:
        raise ValueError(f"No object with idname {idname} in {items}")
    else:
        return not_found_rval

