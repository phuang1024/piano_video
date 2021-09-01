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
Keyboard rendering.
"""

import math
import numpy as np
import cv2
import pv
from pv.props import FloatProp, ListProp, StrProp
from pvkernel import Video


class KEYBOARD_PT_Props(pv.PropertyGroup):
    idname = "keyboard"

    left_offset = FloatProp(
        name="Left Offset",
        description="Piano left side pixel offset.",
        default=0,
    )

    right_offset = FloatProp(
        name="Right Offset",
        description="Piano right side pixel offset",
        default=0,
    )

    black_width_fac = FloatProp(
        name="Black Width Factor",
        description="Black key width factor respective to white key.",
        default=0.5,
    )

    video_path = StrProp(
        name="Path",
        description="Video file path",
    )

    video_start = FloatProp(
        name="Video Start",
        description="Time you start playing in the video in seconds",
    )

    crop = ListProp(
        name="Crop",
        description="Corner locations in clockwise starting from top left.",
        default=[[0, 0], [1920, 0], [1920, 1080], [0, 1080]],
    )

    mask = FloatProp(
        name="Mask",
        description="Amount of space under the keyboard to show (pixels).",
        default=200,
    )


class KEYBOARD_OT_Render(pv.Operator):
    group = "keyboard"
    idname = "render"
    label = "Render"
    description = "Render keyboard on render image."

    def execute(self, video: Video) -> None:
        width, height = video.resolution

        data = video.data.keyboard
        props = video.props.keyboard

        size = data.size

        img = read_frame(video, video.frame)
        img = cv2.warpPerspective(img, data.crop, (size[0], size[1]))

        video.render_img[height//2:, ...] = img[:540, ...]


class KEYBOARD_DT_Data(pv.DataGroup):
    idname = "keyboard"


class KEYBOARD_JT_Init(pv.Job):
    idname = "keyboard_init"

    def execute(self, video: Video) -> None:
        width, height = video.resolution

        data = video.data.keyboard
        props = video.props.keyboard

        points = props.crop
        mask = props.mask

        # Using np.float64 returns inf when dividing by 0, which is what we want
        with np.errstate(divide="ignore"):
            slope1 = np.float64(points[0][1]-points[3][1]) / (points[0][0]-points[3][0])
            x5, y5 = points[3][0]+(mask/slope1), points[3][1]+mask

            slope2 = np.float64(points[1][1]-points[2][1]) / (points[1][0]-points[2][0])
            x6, y6 = points[2][0]+(mask/slope2), points[2][1]+mask

        height_fac = math.hypot(*points[0], x5, y5) / math.hypot(*points[0], *points[1])
        mask_height_fac = mask / math.hypot(*points[0], *points[1])
        src_points = np.array([points[0], points[1], [x6, y6], [x5, y5]]).astype(np.float32)
        dst_points = np.array([[0, 0], [width, 0], [width, width*height_fac], [0, width*height_fac]]).astype(np.float32)

        data.video = cv2.VideoCapture(props.video_path)
        data.fps = video.data.keyboard.video.get(cv2.CAP_PROP_FPS)
        data.crop = cv2.getPerspectiveTransform(src_points, dst_points)
        data.size = list(map(int, [width, width*height_fac, width*(height_fac-mask_height_fac)]))


class KEYBOARD_JT_Render(pv.Job):
    idname = "keyboard_render"
    ops = ("keyboard.render",)


class KEYBOARD_JT_Deinit(pv.Job):
    idname = "keyboard_deinit"

    def execute(self, video: Video) -> None:
        video.data.keyboard.video.release()


def read_frame(video: Video, frame: int) -> np.ndarray:
    """
    Read a frame from ``video.data.keyboard.video``.

    :param video: The video class instance.
    :param frame: Frame to read. 0 = when the first block starts playing.
    """
    data = video.data.keyboard
    props = video.props.keyboard

    real_frame = int(props.video_start*data.fps + frame/video.fps*data.fps)
    data.video.set(1, real_frame)

    ret, img = data.video.read()
    assert ret, "VideoCapture read failed."

    return img


classes = (
    KEYBOARD_PT_Props,
    KEYBOARD_OT_Render,
    KEYBOARD_DT_Data,
    KEYBOARD_JT_Init,
    KEYBOARD_JT_Render,
    KEYBOARD_JT_Deinit,
)

def register():
    for cls in classes:
        pv.utils.register_class(cls)
