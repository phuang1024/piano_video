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

    def read(self, frame_num, verbose=False) -> np.ndarray:
        if frame_num == self.last_frame_num:
            return self.last_img

        elif self.last_frame_num == -1 or frame_num > self.last_frame_num:
            while True:
                if verbose:
                    clearline()
                    log(f"Reading frame {self.last_frame_num}/{frame_num} of {self.path}")
                if frame_num == self.last_frame_num:
                    if verbose:
                        clearline()
                        log(f"Reading frame {frame_num} of {self.path}: Finished")
                        newline()
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

    height_fac = distance(*points[0], x5, y5) / distance(*points[0], *points[1])
    mask_height_fac = mask_size / distance(*points[0], *points[1])
    src_points = np.array([points[0], points[1], [x6, y6], [x5, y5]]).astype(np.float32)
    dst_points = np.array([[0, 0], [width, 0], [width, width*height_fac], [0, width*height_fac]]).astype(np.float32)

    settings["piano.computed_crop"] = [
        [*points, [x5, y5], [x6, y6]],
        src_points,
        dst_points,
        cv2.getPerspectiveTransform(src_points, dst_points),
        [width, width*height_fac, width*mask_height_fac]
    ]


def crop(settings, image):
    persp, size = settings["piano.computed_crop"][3:]
    result = cv2.warpPerspective(image, persp, tuple(map(int, size[:2])))
    return result


def generate_mask(settings):
    width, height, mask_height = settings["piano.computed_crop"][4]
    mask = []

    width, height, mask_height = map(int, (width, height, mask_height))
    for y in range(height):
        value = (height-y) / (height-mask_height)
        value = max(min(value, 1), 0) ** 2
        color = (value, value, value)
        mask.append([color for _ in range(width)])

    settings["piano.mask"] = np.array(mask, dtype=np.float32)


def preview_crop(settings):
    output = settings["files.output"]
    image = VideoReader(settings["files.video"]).read(settings["other.frame"], verbose=True)
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

    ans = input(f"Save cropped image to {output}? (y/n/Q) ").lower().strip()
    if ans == "y":
        cv2.imwrite(output, crop(settings, image))
    elif ans == "n":
        pass
    else:
        return

    ans = input(f"Save masked image to {output}? (y/n/Q) ").lower().strip()
    if ans == "y":
        cv2.imwrite(output, crop(settings, image)*settings["piano.mask"])
    elif ans == "n":
        pass
    else:
        return
