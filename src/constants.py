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

import os
import multiprocessing

# Using lists to keep consistent with json data
DEFAULT_SETTINGS = {
    "files.midis": [],
    "files.video": "",
    "files.output": "",

    "output.resolution": [1920, 1080],
    "output.fps": 30,
    "output.ending_pause": 3,
    "output.format": "VIDEO",

    "blocks.time_offset": 0,
    "blocks.time_mult": 1,
    "blocks.x_offset": 0,
    "blocks.black_width_fac": 0.6,
    "blocks.speed": 0.15,
    "blocks.stabilize_fast": True,
    "blocks.stabilize_max_time": 6,
    "blocks.stabilize_new_time": 3.5,

    "blocks.style": "SOLID",
    "blocks.rounding": 6,
    "blocks.fade_top": True,
    "blocks.color_type": "SOLID",
    "blocks.color": [200, 200, 210],
    "blocks.image": "",
    "blocks.image_gradient": [],
    "blocks.image_speed": 0.15,
    "blocks.glow": True,
    "blocks.glow_color": [100, 110, 160],
    "blocks.border": 1,
    "blocks.border_color": [220, 225, 240],

    "piano.video_offset": 0,
    "piano.video_crop": [],
    "piano.height_fac": 1,
    "piano.top": "LIGHT_BAR",
    "piano.octave_lines": True,

    "effects.glare": True,
    "effects.glare_size": [200, 200],

    "effects.dots": True,
    "effects.dots.style": "FLOATING",
    "effects.dots.glow": True,
    "effects.dots.dps": 90,
    "effects.dots.lifetime": 3,

    "effects.stars": False,
    "effects.stars.probability": 0.35,
    "effects.stars.lifetime": 3,
    "effects.stars.size": 8,

    "text.font": "",
    "text.show_intro": False,
    "text.intro": [],
    "text.show_ending": False,
    "text.ending": [],

    "other.random_seed": 1,
    "other.use_mc": True,
    "other.cores": multiprocessing.cpu_count(),
}

PARENT = os.path.dirname(os.path.realpath(__file__))
DEFAULT_RANDOM = 0

WHITE_KEYS = 52
BLACK_KEYS = 36

RED = (255, 0, 0)
GREEN = (0, 255, 0)
