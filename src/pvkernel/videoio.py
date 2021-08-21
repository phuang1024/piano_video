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

import sys
import os
import numpy as np
import cv2
from subprocess import PIPE, STDOUT, Popen, DEVNULL
from typing import TYPE_CHECKING, Tuple
from .utils import FFMPEG

Video = None
if TYPE_CHECKING:
    from .video import Video


class VideoWriter:
    """Writes a video."""
    path: str

    def __init__(self, path: str, resolution: Tuple[int, int], fps: int, video: Video) -> None:
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


class VideoWriterFFmpeg:
    """Writes a video and compiles using FFmpeg."""
    path: str

    def __init__(self, path: str, resolution: Tuple[int, int], fps: int, video: Video) -> None:
        self.path = path
        self.resolution = resolution
        self.fps = int(fps)
        self.cache = os.path.join(video.cache, "ffmpeg_export")

        self._entered = False
        self._frame = 0

    def __enter__(self):
        os.makedirs(self.cache, exist_ok=True)
        self._entered = True
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._entered = False
        if exc_type == KeyboardInterrupt:
            return

        args = [FFMPEG, "-y", "-i", os.path.join(self.cache, "%d.jpg"), "-c:v", "libx265", "-an", "-r", str(self.fps),
            "-crf", "25", self.path]
        print("Compiling video...")
        p = Popen(args, stdin=DEVNULL, stdout=PIPE, stderr=STDOUT)
        p.wait()

        if p.returncode != 0:
            if input("FFmpeg failed. Show output? [Y/n] ").lower().strip() == "n":
                return
            while True:
                data = p.stdin.read(1024)
                sys.stderr.write(data)
                if len(data) < 1024:
                    break

    def _check_entered(self):
        assert self._entered, "VideoWriterFFmpeg can only be used in a \"with\" statement."

    def write(self, img: np.ndarray) -> None:
        """Write a frame. Return the total number of frames written."""
        self._check_entered()
        path = os.path.join(self.cache, f"{self._frame}.jpg")
        cv2.imwrite(path, img)
        self._frame += 1
