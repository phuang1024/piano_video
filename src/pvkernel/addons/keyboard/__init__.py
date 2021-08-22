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


class KEYBOARD_OT_Render(pv.Operator):
    group = "keyboard"
    idname = "render"
    label = "Render"
    description = "Render keyboard on render image."

    def execute(self, video: Video) -> None:
        pass


class KEYBOARD_DT_Data(pv.DataGroup):
    idname = "keyboard"


class KEYBOARD_JT_Init(pv.Job):
    idname = "keyboard_init"

    def execute(self, video: Video) -> None:
        path = video.props.keyboard.video_path
        video.data.keyboard.video = cv2.VideoCapture(path)
        video.data.keyboard.fps = video.data.keyboard.video.fps


class KEYBOARD_JT_Render(pv.Job):
    idname = "keyboard_render"
    ops = ("keyboard.render",)


class KEYBOARD_JT_Deinit(pv.Job):
    idname = "keyboard_init"

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
