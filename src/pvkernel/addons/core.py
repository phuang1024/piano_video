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
Core properties and operators.

Will register:

* Data group ``core``
* Property group ``core``
* Operator group ``core``
* Job group ``core``
"""

import pv
from pv.props import FloatProp
from pvkernel import Video


class BUILTIN_PT_Core(pv.PropertyGroup):
    idname = "core"

    pause_start = FloatProp(
        name="Start Pause",
        description="Number of seconds before first note",
        default=3,
    )

    pause_end = FloatProp(
        name="End Pause",
        description="Number of seconds after last note",
        default=3,
    )


class BUILTIN_DT_Core(pv.DataGroup):
    idname = "core"


class BUILTIN_OT_RunningTime(pv.Operator):
    group = "core"
    idname = "running_time"
    label = "Running Time"
    description = "Total frames the piano plays with start and end pauses. Saves to core_data.running_time"

    def execute(self, video: Video) -> None:
        pause = video.fps * (video.props.core.pause_start+video.props.core.pause_end)
        first_note = min(video.data.midi.notes, key=lambda n: n.start).start
        last_note = max(video.data.midi.notes, key=lambda n: n.end).end

        total = pause + (last_note-first_note)
        video.data.core.running_time = int(total)


class BUILTIN_OT_KeyPos(pv.Operator):
    group = "core"
    idname = "key_pos"
    label = "Key Positions"
    description = "Calculate key X positions and widths and store in a list at core_data.key_pos"

    @staticmethod
    def is_white(key: int):
        """
        Whether the key is a white key, starting from the lowest note with a value of 0.
        """
        return (key-3) % 12 not in (1, 3, 6, 8, 10)

    def execute(self, video: Video) -> None:
        left = video.props.keyboard.left_offset
        right = video.props.keyboard.right_offset + video.resolution[0]
        width = right - left

        video.data.core.key_pos = [None] * 88

        white_width = width / 52
        black_width = white_width * video.props.keyboard.black_width_fac
        black_offset = white_width - black_width/2
        x = left
        for key in range(88):
            if self.is_white(key):
                video.data.core.key_pos[key] = (x, white_width)
                x += white_width
            else:
                video.data.core.key_pos[key] = (x-black_offset, black_width)

        assert None not in video.data.core.key_pos, "Error calculating key position."


class BUILTIN_JT_Core(pv.Job):
    idname = "core"
    ops = ("core.running_time", "core.key_pos")


classes = (
    BUILTIN_PT_Core,
    BUILTIN_DT_Core,
    BUILTIN_OT_RunningTime,
    BUILTIN_OT_KeyPos,
    BUILTIN_JT_Core,
)

def register():
    for cls in classes:
        pv.utils.register_class(cls)
