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

import mido


def parse_midis(settings):
    notes = []

    for file in settings["files.midis"]:
        midi = mido.MidiFile(file)
        tpb = midi.ticks_per_beat

        starts = [None for _ in range(88)]
        tempo = 500000
        curr_frame = 0
        for msg in midi.tracks[0]:
            curr_frame += msg.time / tpb * tempo / 1000000 * settings["output.fps"]
            if msg.is_meta and msg.type == "set_tempo":
                tempo = msg.tempo
            elif msg.type in ("note_on", "note_off"):
                note, velocity = msg.note-21, msg.velocity
                if velocity == 0 or msg.type == "note_off":
                    notes.append((note, starts[note], curr_frame))
                else:
                    starts[note] = curr_frame

    return notes
