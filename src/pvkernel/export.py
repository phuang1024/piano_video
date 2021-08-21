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
import cv2
from tqdm import trange
from typing import TYPE_CHECKING
from pv import Job
from pv.utils import call_op
from .videoio import VideoWriter

Video = None
if TYPE_CHECKING:
    from .video import Video


def exe_job(video: Video, job: Job):
    job.execute(video)
    for op in job.ops:
        call_op(video, op)


def export(context: Video, path: str) -> None:
    """Exports the video from a video."""
    for job in context.get_jobs("init"):
        exe_job(context, job)

    res = context.resolution
    with VideoWriter(path, res, int(context.fps)) as video:
        intro = context.props.core.pause_start * context.fps
        for frame in trange(context.data.core.running_time, desc="Rendering video"):
            context._frame = int(frame - intro)
            context._render_img = np.zeros((res[1], res[0], 3), dtype=np.uint8)

            for job in context.get_jobs("frame_init"):
                exe_job(context, job)
            for job in context.get_jobs("frame"):
                exe_job(context, job)
            for job in context.get_jobs("frame_deinit"):
                exe_job(context, job)
            for job in context.get_jobs("modifiers"):
                exe_job(context, job)

            img = cv2.cvtColor(context.render_img, cv2.COLOR_BGR2RGB)
            video.write(img)

    for job in context.get_jobs("deinit"):
        exe_job(context, job)
