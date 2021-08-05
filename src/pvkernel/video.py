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
    "Video",
)

import pv
from pv.types import DataGroup, PropertyGroup
from typing import Any, Tuple, Type, Union


class Video:
    """
    This class holds all the settings of a video.
    It is also used like a "context" for all rendering functions.
    """
    resolution: Tuple[int, int]
    fps: float

    def __init__(self, resolution: Tuple[int, int] = (1920, 1080), fps: float = 30.) -> None:
        """
        Initializes the Video.

        :param resolution: (X, Y) pixel resolution.
        :param fps: Frames per second. Can be float, but will be rounded down in export.
        :return: None
        """
        self.resolution = resolution
        self.fps = fps

        self._pgroups = []   # PropertyGroups.
        self._dgroups = []   # DataGroups

        self._add_callbacks()

    def __getattr__(self, name: str) -> Any:
        if pv.utils.get_exists(self._pgroups, name):
            return pv.utils.get(self._pgroups, name)
        if pv.utils.get_exists(self._dgroups, name):
            return pv.utils.get(self._dgroups, name)

        raise AttributeError(f"pvkernel.Video has no attribute {name}")

    def _add_callbacks(self) -> None:
        """
        Adds callbacks. Internal use.
        """
        pv.utils.add_callback(self._add_pgroup, ("pgroup",))
        pv.utils.add_callback(self._add_dgroup, ("dgroup",))
        for cls in pv.utils._get_pgroups():
            self._add_pgroup(cls)
        for cls in pv.utils._get_dgroups():
            self._add_dgroup(cls)

    def _add_pgroup(self, cls: Type[PropertyGroup]) -> None:
        """
        Callback function to add PropertyGroup props to internal list.
        """
        self._pgroups.append(cls())

    def _add_dgroup(self, cls: Type[DataGroup]) -> None:
        """
        Callback function to add DataGroup to internal list.
        """
        self._dgroups.append(cls())
