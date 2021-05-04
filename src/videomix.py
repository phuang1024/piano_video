#
#  Piano Video
#  Piano MIDI visualizer
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
from utils import *


def compute_crop_points(settings):
    (x1, y1), (x2, y2), piano_height, fade_height = settings["piano.video_crop"]
    height = piano_height + fade_height
    slope = (y2-y1) / (x2-x1)
    x3, y3 = (x1-height*slope if slope != 0 else x1), y1+height
    x4, y4 = x3 + (x2-x1), y3 + (y2-y1)
    x5, y5 = (x1-piano_height*slope if slope != 0 else x1), y1+piano_height
    x6, y6 = x5 + (x2-x1), y5 + (y2-y1)

    for i in range(1, 7):
        settings[f"piano.video_crop_x{i}"] = locals()[f"x{i}"]
        settings[f"piano.video_crop_y{i}"] = locals()[f"y{i}"]


def crop_piano(settings, image):
    x1 = settings["piano.video_crop_x1"]
    y1 = settings["piano.video_crop_y1"]
    x2 = settings["piano.video_crop_x2"]
    y2 = settings["piano.video_crop_y2"]
    x3 = settings["piano.video_crop_x3"]
    y3 = settings["piano.video_crop_y3"]
    x4 = settings["piano.video_crop_x4"]
    y4 = settings["piano.video_crop_y4"]

    width = int(distance(x1, y1, x2, y2))
    height = int(distance(x1, y1, x3, y3))
    src_points = np.array(((x1, y1), (x2, y2), (x4, y4), (x3, y3)), dtype=np.float32)
    dst_points = np.array(((0, 0), (width, 0), (width, height), (0, height)), dtype=np.float32)

    persp = cv2.getPerspectiveTransform(src_points, dst_points)
    result = cv2.warpPerspective(image, persp, (width, height))
    return result
