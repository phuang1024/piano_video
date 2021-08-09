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

* Data group ``core_data``
* Property group ``core_props``
* Operator group ``core_ops``
* Job group ``core_job``
"""

import pv
from pv.props import FloatProp
from pvkernel import Video


class BUILTIN_PT_Core(pv.types.PropertyGroup):
    idname = "core_props"

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


class BUILTIN_DT_Core(pv.types.DataGroup):
    idname = "core_data"


class BUILTIN_OT_RunningTime(pv.types.Operator):
    group = "core_ops"
    idname = "running_time"
    label = "Running Time"
    description = "Total frames the piano plays with start and end pauses. Saves to core_data.running_time"

    def execute(self, video: Video) -> None:
        pause = video.fps * (video.core_props.pause_start+video.core_props.pause_end)
        first_note = min(video.midi_data.notes, key=lambda n: n.start).start
        last_note = max(video.midi_data.notes, key=lambda n: n.end).end

        total = pause + (last_note-first_note)
        video.core_data.running_time = int(total)


class BUILTIN_OT_KeyPos(pv.types.Operator):
    group = "core_ops"
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
        left = video.piano_props.left_offset
        right = video.piano_props.right_offset + video.resolution[0]
        width = right - left

        video.core_data.key_pos = [None] * 88

        white_width = width / 52
        black_width = white_width * video.piano_props.black_width_fac
        black_offset = white_width - black_width/2
        x = 0
        for key in range(88):
            if self.is_white(key):
                video.core_data.key_pos[key] = (x, white_width)
                x += white_width
            else:
                video.core_data.key_pos[key] = (x+black_offset, black_width)

        assert None not in video.core_data.key_pos, "Error calculating key position."
        print(video.core_data.key_pos)


class BUILTIN_JT_Core(pv.types.Job):
    idname = "core_job"
    ops = ("core_ops.running_time", "core_ops.key_pos")


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
