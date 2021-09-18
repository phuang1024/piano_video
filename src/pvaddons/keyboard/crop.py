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

import math
import numpy as np
import cv2
import pv
from pvkernel import Video
from pvkernel.utils import bounds


class KEYBOARD_JT_Init(pv.Job):
    idname = "keyboard_init"

    def execute(self, video: Video) -> None:
        self.compute_crop(video)

    def compute_crop(self, video: Video):
        """
        Find perspective warp and store in data.
        """
        width, height = video.resolution

        data = video.data.keyboard
        props = video.props.keyboard

        points = props.crop
        mask = props.mask

        data.video = cv2.VideoCapture(props.video_path)
        data.fps = video.data.keyboard.video.get(cv2.CAP_PROP_FPS)

        #
        #  REMEMBER: The lists are zero indexed and this diagram
        #  is 1 indexed.
        #
        #  This drawing places the lines perpendicular to each other,
        #  but keep in mind this may not be the case.
        #
        #  User inputs [p1, p2, p3, p4] through props.keyboard.crop
        #
        #  p1-----------------------p2
        #  |        keyboard         |
        #  p4-----------------------p3
        #  |      below keyboard     |
        #  p5-----------------------p6
        #

        # Using np.float64 returns inf when dividing by 0, which is what we want
        with np.errstate(divide="ignore"):
            # Find p5 by using slope of p1 and p4
            slope1 = np.float64(points[0][1]-points[3][1]) / (points[0][0]-points[3][0])
            x5, y5 = points[3][0]+(mask/slope1), points[3][1]+mask

            # Find p6 by using slope of p2 and p3
            slope2 = np.float64(points[1][1]-points[2][1]) / (points[1][0]-points[2][0])
            x6, y6 = points[2][0]+(mask/slope2), points[2][1]+mask

        # height_fac = vertical / horizontal
        # mask_height_fac = mask_size / vertical
        height_fac = math.hypot(*points[0], x5, y5) / math.hypot(*points[0], *points[1])
        mask_height_fac = mask / math.hypot(*points[0], *points[3])
        kbd_height = int(width * height_fac)

        # Compute start and end points for perspective warp
        src_points = np.array([points[0], points[1], [x6, y6], [x5, y5]]).astype(np.float32)
        dst_points = np.array([[0, 0], [width, 0], [width, kbd_height], [0, kbd_height]]).astype(np.float32)

        # Compute mask_img. It will be multiplied with the cropped keyboard
        # to dim the bottom.
        mask_img = np.empty((kbd_height, width, 3), dtype=np.float32)
        for i in range(kbd_height):
            value = np.interp(i, (kbd_height * (1-mask_height_fac), kbd_height), (1, 0))
            value = bounds(value)
            mask_img[i, ...] = value

        data.points = [*points, [x5, y5], [x6, y6]]
        data.crop = cv2.getPerspectiveTransform(src_points, dst_points)
        data.mask_img = mask_img
        data.size = (width, kbd_height)
