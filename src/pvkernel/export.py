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

import numpy as np
from typing import TYPE_CHECKING
from pv.utils import call_op
from .videoio import VideoWriter

Video = None
if TYPE_CHECKING:
    from .video import Video


def export(context: Video, path: str) -> None:
    """
    Exports the video from a video.
    """
    res = context.resolution
    with VideoWriter(path, res, int(context.fps)) as video:
        for i in range(30):
            context._render_img = np.zeros((res[1], res[0], 4), dtype=np.uint8)
            for op in context._jobs["blocks"]:
                call_op(context, op)
            video.write(context.render_img[..., :3])
