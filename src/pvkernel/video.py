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

import numpy as np
import pv
from pv.types import DataGroup, OpGroup, Operator, PropertyGroup
from pv.utils import get, get_exists
from typing import Any, Sequence, Tuple, Type
from .export import export


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

        self._jobs = {
            "init": [],
            "intro": [],
            "piano": [],
            "blocks": [],
            "effects": [],
            "outro": [],
            "modifiers": [],
            "deinit": [],
        }
        self._render_img: np.ndarray = None
        self._frame: int = None

        self._dgroups = []   # DataGroups
        self._ogroups = []   # Operators
        self._pgroups = []   # PropertyGroups.

        self._add_callbacks()
        self._add_default_jobs()

    def __getattr__(self, name: str) -> Any:
        if pv.utils.get_exists(self._ogroups, name):
            return pv.utils.get(self._ogroups, name)
        if pv.utils.get_exists(self._dgroups, name):
            return pv.utils.get(self._dgroups, name)
        if pv.utils.get_exists(self._pgroups, name):
            return pv.utils.get(self._pgroups, name)

        raise AttributeError(f"pvkernel.Video has no attribute {name}")

    @property
    def render_img(self) -> np.ndarray:
        assert self._render_img is not None, "Input image not initialized (kernel fault)."
        return self._render_img

    @render_img.setter
    def render_img(self, value) -> None:
        self._render_img = value

    @property
    def frame(self) -> int:
        assert self._frame is not None, "Frame not initialized (kernel fault)."
        return self._frame

    def export(self, path: str) -> None:
        """
        Calls ``pvkernel.export.export``
        """
        export(self, path)

    def clear_jobs(self, slot: str) -> None:
        """
        Clear the jobs in a slot.
        """
        self._jobs[slot] = []

    def add_job(self, idname: str, slot: str) -> None:
        """
        Add a job to run.

        :param idname: Job idname.
        :param slot: Job slot idname.
        """
        jobs = pv.utils._get_jobs()
        job = get(jobs, idname)
        self._jobs[slot].extend(job.ops)

    def get_jobs(self, slot: str) -> Sequence[str]:
        """
        Get the jobs in a slot.
        """
        return self._jobs[slot]

    def _add_default_jobs(self):
        self.add_job("midi_job", "init")
        self.add_job("core_job", "init")
        self.add_job("blocks_job", "blocks")

    def _add_callbacks(self) -> None:
        """
        Adds callbacks. Internal use.
        """
        pv.utils.add_callback(self._add_dgroup, ("dgroup",))
        pv.utils.add_callback(self._add_ogroup, ("ogroup",))
        pv.utils.add_callback(self._add_pgroup, ("pgroup",))
        for cls in pv.utils._get_dgroups():
            self._add_dgroup(cls)
        for cls in pv.utils._get_ogroups():
            self._add_ogroup(cls)
        for cls in pv.utils._get_pgroups():
            self._add_pgroup(cls)

    def _add_dgroup(self, cls: Type[DataGroup]) -> None:
        """
        Callback function to add DataGroup to internal list.
        """
        self._dgroups.append(cls())

    def _add_ogroup(self, cls: Type[Operator]) -> None:
        """
        Callback function to add Operator to internal list.
        """
        group = cls.group
        if not get_exists(self._ogroups, group):
            self._ogroups.append(OpGroup(group, self))
        get(self._ogroups, cls.group).operators.append(cls(self))

    def _add_pgroup(self, cls: Type[PropertyGroup]) -> None:
        """
        Callback function to add PropertyGroup props to internal list.
        """
        self._pgroups.append(cls())
