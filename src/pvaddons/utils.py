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
Utils for use by builtin addons.
"""

from pvkernel import Video
from typing import Tuple


def first_note(video: Video) -> float:
    """
    :return: The frame the first note starts.
    """
    return min(video.data.midi.notes, key=lambda n: n.start).start


def block_pos(video: Video, note, first_note: float) -> Tuple[float, float]:
    """
    Get the start and end block position.

    :param video: Video. Current frame will be used.
    :param note: Note class. Defined in ``midi.py``
    :param first_note: The frame the first note starts.
    :return: (top, bottom) pixel locations.
        0 is the bottom (where the blocks hit the piano).
        Going up from 0 makes the y value smaller.
    """
    frame = video.frame
    height = video.resolution[1]
    threshold = height / 2
    speed = video.props.blocks.speed * height / video.fps   # pixels per frame

    start = note.start - first_note - frame
    end = note.end - first_note - frame
    if video.props.midi.reverse:
        top = threshold + start*speed
        bottom = threshold + end*speed
    else:
        top = threshold - end*speed
        bottom = threshold - start*speed

    return (top, bottom)
