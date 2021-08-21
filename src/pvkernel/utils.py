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

import os
import shutil
from typing import Any, Dict

PARENT = os.path.dirname(os.path.realpath(__file__))
ADDON_PATHS = (
    os.path.join(PARENT, "addons"),
)

CUDA = ("PV_USE_CUDA" in os.environ)
FFMPEG = shutil.which("ffmpeg")
HAS_FFMPEG = (FFMPEG is not None)


class Namespace:
    """
    You can do ``namespace.a = 1`` or ``namespace.a`` to set and
    access any value.
    """
    _items: Dict[str, Any]

    def __init__(self) -> None:
        object.__setattr__(self, "_items", {})

    def __getattr__(self, name: str) -> Any:
        if name in self._items:
            return self._items[name]
        else:
            raise AttributeError(f"Namespace has no attribute {name}")

    def __setattr__(self, name: str, value: Any) -> None:
        self._items[name] = value


def rgba(color):
    return (*color, 255) if len(color) == 3 else color
