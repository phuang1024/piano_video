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
from constants import *
from utils import *


class VideoReader:
    def __init__(self, path):
        self.path = path
        self.reset()

    def raise_rval(self, rval):
        if not rval:
            raise ValueError(f"Error decoding frame {self.last_frame_num} of video {self.path}")

    def reset(self):
        self.video = cv2.VideoCapture(self.path)
        self.last_frame_num = -1
        self.last_img = None

    def next(self) -> np.ndarray:
        rval, frame = self.video.read()
        self.last_frame_num += 1
        self.raise_rval(rval)
        self.last_img = frame
        return frame

    def read(self, frame_num) -> np.ndarray:
        if frame_num == self.last_frame_num:
            return self.last_img

        elif self.last_frame_num == -1 or frame_num > self.last_frame_num:
            while True:
                if frame_num == self.last_frame_num:
                    return self.last_img
                rval, frame = self.video.read()
                self.last_frame_num += 1
                self.raise_rval(rval)
                self.last_img = frame

        elif frame_num < self.last_frame_num:
            self.reset()
            return self.read(frame_num)


def compute_crop(settings):
    width, height = settings["output.resolution"]
    points, mask_size = settings["piano.video_crop"]

    # Using np.float64 returns inf when dividing by 0, which is what we want
    with np.errstate(divide="ignore"):
        slope1 = np.float64(points[0][1]-points[3][1]) / (points[0][0]-points[3][0])
        x5, y5 = points[3][0]+(mask_size/slope1), points[3][1]+mask_size

        slope2 = np.float64(points[1][1]-points[2][1]) / (points[1][0]-points[2][0])
        x6, y6 = points[2][0]+(mask_size/slope2), points[2][1]+mask_size

    height_fac = distance(*points[0], *points[3]) / distance(*points[0], *points[1])
    src_points = [points[0], points[1], [x6, y6], [x5, y5]]
    dst_points = [[0, height/2], [width, height/2], [width, height/2+width*height_fac], [0, height/2+width*height_fac]]

    settings["piano.computed_crop"] = [
        [*points, [x5, y5], [x6, y6]],
        src_points,
        dst_points,
        cv2.getPerspectiveTransform(np.array(src_points).astype(np.float32),
            np.array(dst_points).astype(np.float32)),
    ]


def preview_crop(settings):
    output = settings["files.output"]
    image = VideoReader(settings["files.video"]).read(settings["other.frame"])
    computed = settings["piano.computed_crop"]

    image_crop_box = array_to_surf(image)
    pygame.draw.line(image_crop_box, RED, computed[0][0], computed[0][1], 2)
    pygame.draw.line(image_crop_box, RED, computed[0][0], computed[0][3], 2)
    pygame.draw.line(image_crop_box, RED, computed[0][2], computed[0][1], 2)
    pygame.draw.line(image_crop_box, RED, computed[0][2], computed[0][3], 2)
    pygame.draw.line(image_crop_box, GREEN, computed[0][2], computed[0][5], 2)
    pygame.draw.line(image_crop_box, GREEN, computed[0][3], computed[0][4], 2)
    pygame.draw.line(image_crop_box, GREEN, computed[0][4], computed[0][5], 2)

    for i in range(4):
        pygame.draw.circle(image_crop_box, RED, computed[0][i], 10, width=2)
    for i in range(4, 6):
        pygame.draw.circle(image_crop_box, GREEN, computed[0][i], 10, width=2)

    ans = input(f"Save crop preview to {output}? (y/n/Q) ").lower().strip()
    if ans == "y":
        pygame.image.save(image_crop_box, output)
    elif ans == "n":
        pass
    else:
        return
