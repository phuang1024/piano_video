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
MIDI parsing and handling.

Will register:

* Data group ``midi``
* Property group ``midi``
* Operator group ``midi``
* Job ``midi``
"""

import os
import mido
import pv
from pv.props import StrProp
from pvkernel import Video
from utils import block_pos, first_note
from typing import Any, Dict


class Message:
    """
    Represents one MIDI message.

    Attributes:

    * ``type``: Type.
    * ``time``: Time (in frames) this message happens.
    * ``attrs``: Dict of any other attributes.
    """
    type: str
    time: float
    attrs: Dict[str, Any]

    def __init__(self, type: str, time: float, **attrs: Dict[str, Any]) -> None:
        self.type = type
        self.time = time
        self.attrs = attrs

    def __getattr__(self, name: str) -> Any:
        return self.attrs[name]


class Note:
    """
    Represents one note.

    Attributes:

    * ``start``: Frame start.
    * ``end``: Frame end.
    * ``note``: Note number (0 is lowest on piano).
    * ``velocity``: Velocity.
    """
    start: float
    end: float
    note: int
    velocity: int

    def __init__(self, start: float, end: float, note: int, velocity: int) -> None:
        self.start = start
        self.end = end
        self.note = note
        self.velocity = velocity


class MIDI_PT_Midi(pv.types.PropertyGroup):
    idname = "midi"

    paths = StrProp(
        name="Paths",
        description="MIDI file paths. Separate with os.path.pathsep",
    )


class MIDI_DT_Midi(pv.types.DataGroup):
    idname = "midi"


class MIDI_OT_Parse(pv.types.Operator):
    group = "midi"
    idname = "parse"
    label = "Parse MIDI"
    description = "Parse selected midi files and store in data group."

    def execute(self, video: Video) -> None:
        paths = video.props.midi.paths.split(os.path.pathsep)
        messages = []
        for path in paths:
            with mido.MidiFile(os.path.realpath(path)) as midi:
                time = 0
                for msg in midi:
                    time += msg.time * video.fps
                    attrs = {a: getattr(msg, a) for a in dir(msg) if (not a.startswith("_")) and (a not in ("time", "type"))}
                    messages.append(Message(msg.type, time, **attrs))
        messages.sort(key=lambda m: m.time)

        notes = []
        on = [0] * 88   # When the note was on
        for msg in messages:
            if msg.type in ("note_on", "note_off"):
                note = msg.note - 21
                note_on = (msg.type == "note_on" and msg.velocity > 0)
                if 0 <= note < 88:
                    if note_on:
                        on[note] = msg.time
                    else:
                        notes.append(Note(on[note], msg.time, note, msg.velocity))
        notes.sort(key=lambda n: n.start)

        video.data.midi.messages = messages
        video.data.midi.notes = notes


class MIDI_OT_NotesPlaying(pv.types.Operator):
    group = "midi"
    idname = "notes_playing"
    label = "Notes Playing"
    description = "Calculate notes currently playing and store in ``midi.notes_playing``"

    def execute(self, video: Video) -> None:
        threshold = video.resolution[1] / 2
        first = first_note(video)

        video.data.midi.notes_playing = []
        for note in video.data.midi.notes:
            top, bottom = block_pos(video, note, first)
            if top <= threshold <= bottom:
                video.data.midi.notes_playing.append(note.note)


class MIDI_JT_Init(pv.types.Job):
    idname = "midi"
    ops = ("midi.parse",)


class MIDI_JT_FrameInit(pv.types.Job):
    idname = "midi_frame_init"
    ops = ("midi.notes_playing",)


classes = (
    MIDI_PT_Midi,
    MIDI_DT_Midi,
    MIDI_OT_Parse,
    MIDI_OT_NotesPlaying,
    MIDI_JT_Init,
    MIDI_JT_FrameInit,
)

def register():
    for cls in classes:
        pv.utils.register_class(cls)
