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

import os
import random
import string
import numpy as np
import pv
from pv.types import Cache, DataGroup, Job, OpGroup, Operator, PropertyGroup
from pv.utils import get
from typing import Sequence, Tuple, Type
from .export import export
from .utils import HAS_FFMPEG, Namespace


class Video:
    """
    This class holds all the settings of a video.
    It is also used like a "context" for all rendering functions.

    Attributes users can use:

    * ``export(path)``: Render and save video to path.
    * ``clear_jobs(slot)``: Clear all the jobs of a slot.
    * ``add_job(idname, slot)``: Add a job to a slot.
    * ``get_jobs(slot)``: Return the jobs of a slot.

    Attributes add-ons can use:

    * ``frame``: Current frame that is rendering.
    * ``render_img``: Modify this attribute to update the render image.
    * ``cache``: Cache directory. You should extend off of this if you need cache.
    """
    resolution: Tuple[int, int]
    fps: float
    ffmpeg: bool

    props: Namespace
    ops: Namespace
    data: Namespace

    _frame: int
    _render_img: np.ndarray

    def __init__(self, resolution: Tuple[int, int] = (1920, 1080), fps: float = 30.0, ffmpeg: bool = ...) -> None:
        """
        Initializes the Video.

        :param resolution: (X, Y) pixel resolution.
        :param fps: Frames per second. Can be float, but will be rounded down in export.
        :param ffmpeg: Use FFmpeg to compile video. Default True if ffmpeg is present.
        :return: None
        """
        self.resolution = resolution
        self.fps = fps
        self.ffmpeg = HAS_FFMPEG if ffmpeg == ... else ffmpeg

        rand = "".join(random.choices(string.ascii_letters+string.digits, k=32))
        self.cache = os.path.join(os.getcwd(), ".pvcache", rand)
        os.makedirs(self.cache)

        self._jobs = {
            "init": [],
            "intro": [],
            "frame_init": [],
            "frame": [],
            "frame_deinit": [],
            "outro": [],
            "modifiers": [],
            "deinit": [],
        }

        self._render_img = None
        self._frame = None

        self._add_callbacks()
        self._add_default_jobs()

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
        self._jobs[slot].append(job())

    def get_jobs(self, slot: str) -> Sequence[Job]:
        """
        Get the jobs in a slot.
        """
        return self._jobs[slot]

    def _add_default_jobs(self):
        self.add_job("midi", "init")
        self.add_job("core", "init")
        self.add_job("midi_frame_init", "frame_init")
        self.add_job("blocks", "frame")
        self.add_job("smoke", "frame")
        self.add_job("ptcls", "frame")
        self.add_job("glare", "frame")

    def _add_callbacks(self) -> None:
        """
        Adds callbacks. Internal use.
        """
        self.caches = Namespace()
        self.props = Namespace()
        self.ops = Namespace()
        self.data = Namespace()

        pv.utils.add_callback(self._add_dgroup, ("dgroup",))
        pv.utils.add_callback(self._add_ogroup, ("ogroup",))
        pv.utils.add_callback(self._add_pgroup, ("pgroup",))
        pv.utils.add_callback(self._add_cache, ("cache",))

        for cls in pv.utils._get_dgroups():
            self._add_dgroup(cls)
        for cls in pv.utils._get_ogroups():
            self._add_ogroup(cls)
        for cls in pv.utils._get_pgroups():
            self._add_pgroup(cls)
        for cls in pv.utils._get_caches():
            self._add_cache(cls)

    def _add_dgroup(self, cls: Type[DataGroup]) -> None:
        """
        Callback function to add DataGroup to internal list.
        """
        setattr(self.data, cls.idname, cls())

    def _add_ogroup(self, cls: Type[Operator]) -> None:
        """
        Callback function to add Operator to internal list.
        """
        group = cls.group
        if not hasattr(self.ops, group):
            setattr(self.ops, group, OpGroup(group, self))
        setattr(getattr(self.ops, group), cls.idname, cls(self))

    def _add_pgroup(self, cls: Type[PropertyGroup]) -> None:
        """
        Callback function to add PropertyGroup props to internal list.
        """
        setattr(self.props, cls.idname, cls())

    def _add_cache(self, cls: Type[Cache]) -> None:
        setattr(self.caches, cls.idname, cls(self))
