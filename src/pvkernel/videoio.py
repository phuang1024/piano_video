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

"""
Provides convenient video read and write classes.
"""

from typing import Tuple
import numpy as np
import cv2


class VideoWriter:
    """
    Writes a video.
    """
    path: str

    def __init__(self, path: str, resolution: Tuple[int, int], fps: int) -> None:
        self.path = path
        self.resolution = resolution
        self.fps = fps

        self._entered = False
        self._pos = 0

    def __enter__(self):
        self._video = cv2.VideoWriter(self.path, cv2.VideoWriter_fourcc(*"mp4v"),
            self.fps, self.resolution)
        self._entered = True
        return self

    def __exit__(self, *args):
        self._video.release()
        self._entered = False

    def _check_entered(self):
        assert self._entered, "VideoWriter can only be used in a \"with\" statement."

    def tell(self) -> int:
        """
        Return number of frames written.
        """
        self._check_entered()
        return self._pos

    def write(self, img: np.ndarray) -> int:
        """
        Write a frame. Return the total number of frames written.
        """
        self._check_entered()
        self._pos += 1
        self._video.write(img)
        return self._pos
