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

from pvkernel import Video
from utils import block_pos, first_note


def iter_blocks(video: Video):
    """
    Iterate through all blocks to draw for the current frame.
    Return a generator. Each entry is ``(x, y, width, height)``
    """
    height = video.resolution[1]
    threshold = height / 2
    first = first_note(video)

    for note in video.data.midi.notes:
        top, bottom = block_pos(video, note, first)
        if not (bottom < 0 or top > threshold):
            x, width = video.data.core.key_pos[note.note]
            bottom = min(bottom, threshold+10)

            yield (x, top, width, bottom-top)
