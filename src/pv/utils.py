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

PARENT = os.path.dirname(os.path.realpath(__file__))
BUILTIN_ICON_PATHS = (
    os.path.join(PARENT, "assets"),
)

UI32 = "<I"
I32 = "<i"
I64 = "<q"
F32 = "f"
F64 = "d"


def register_class(cls):
    import pv

    inst = cls()
    if issubclass(cls, pv.types.PropertyGroup):
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
        pv.context.ui_panels.append(inst)


def unregister_class(cls):
    import pv
    context = pv.context
    scene = pv.context.scene

    if issubclass(cls, pv.types.PropertyGroup):
        for i in range(len(scene.pgroups)):
            if scene.pgroups[i].idname == cls.idname:
                scene.pgroups.pop(i)
                break
        else:
            raise ValueError(f"No registered PropertyGroup: {cls.idname}")

    elif issubclass(cls, pv.types.UISection):
        for i in range(len(context.ui_sections)):
            if context.ui_sections[i].idname == cls.idname:
                context.ui_sections.pop(i)
                break
        else:
            raise ValueError(f"No registered UISection: {cls.idname}")

    elif issubclass(cls, pv.types.UIPanel):
        for i in range(len(context.ui_panels)):
            if context.ui_panels[i].idname == cls.idname:
                context.ui_panels.pop(i)
                break
        else:
            raise ValueError(f"No registered UIPanel: {cls.idname}")
