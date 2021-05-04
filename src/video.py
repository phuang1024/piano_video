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

import cv2


class VideoReader:
    def __init__(self, path):
        self.path = path
        self.reset()

    def raise_rval(self, rval):
        if not rval:
            raise ValueError(f"Error decoding frame {self.last_frame} of video {self.path}")

    def reset(self):
        self.video = cv2.VideoCapture(self.path)
        self.last_frame = -1
        self.last_img = None

    def next(self):
        rval, frame = self.video.read()
        self.last_frame += 1
        self.raise_rval(rval)
        self.last_img = frame
        return frame

    def read(self, frame_num):
        if frame_num == self.last_frame:
            return self.last_img

        elif self.last_frame == -1 or frame_num > self.last_frame:
            while True:
                if frame_num == self.last_frame:
                    return self.last_img
                rval, frame = self.video.read()
                self.last_frame += 1
                self.raise_rval(rval)
                self.last_img = frame

        elif frame_num < self.last_frame:
            self.reset()
            return self.read(frame_num)
