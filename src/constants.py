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

DEFAULT_SETTINGS = {
    "files.midis": [],
    "files.video": "",

    "output.resolution": (1920, 1080),
    "output.fps": 30,
    "output.format": "video",
    "output.length": "autodetect",
    "output.ending_pause": 1,
    "output.path": "",

    "layout.middle_fac": 0.5,
    "layout.border_fac": 0,
    "layout.keys_height": 0.2,

    "piano.method": "video",
    "piano.video_path": "",
    "piano.video_crop": [],
    "piano.video_offset": 0,
    "piano.black_width_fac": 0.6,

    "blocks.time_offset": 0,
    "blocks.x_offset": 0,
    "blocks.color": (255, 255, 255),
    "blocks.speed": 0.15,
    "blocks.min_height": 30,
    "blocks.rounding": 6,
}

WHITE_KEYS = 52
BLACK_KEYS = 36
TOTAL_KEYS = WHITE_KEYS + BLACK_KEYS
