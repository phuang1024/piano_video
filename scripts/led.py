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
Controls LEDs on the piano.
Lights up an LED when pressed, and turns it off when released.

Define your own implementations for ``led_on`` and ``led_off``.
``led_on`` is passed arguments ``(note_num, rgb_color)``
``led_off`` is passed arguments ``(note_num,)``
``note_num`` is 0 indexed starting from the lowest note on piano.
``rgb_color`` is a tuple (r, g, b) from 0 to 255, inclusive.

Edit the ``COLOR_GRADIENT`` to adjust the LED colors.
It is a sequence of ``(factor, hsv)`` values. Linear interpolation
is used between values.

Requirements:
* ``mido`` (pip install mido)
"""

import colorsys
import mido
from typing import Sequence, Tuple

# See above for instructions
COLOR_GRADIENT = (
    (0, (0, 0.6, 1)),
    (1, (1, 0.6, 1)),
)


def led_on(note_num: int, rgb_color: Tuple[int, int, int]):
    """
    Define your own implementation. See above for instructions.
    """
    print(f"LED On: {note_num}, {rgb_color}")

def led_off(note_num: int):
    """
    Define your own implementation. See above for instructions.
    """
    print(f"LED Off: {note_num}")


def mix_cols(c1: Tuple[float, float, float], c2: Tuple[float, float, float], fac: float) -> Tuple[float, float, float]:
    return tuple([c1[i]*(1-fac) + c2[i]*fac for i in range(3)])

def interpolate(grad: Sequence[Tuple[int, Tuple[float, float, float]]], fac: float) -> Tuple[float, float, float]:
    """
    Return HSV value. Each index is from 0 to 1.
    """
    if len(grad) == 0:
        raise ValueError("At least one gradient key must be specified.")

    elif len(grad) == 1:
        return grad[0][1]

    else:
        if fac <= grad[0][0]:
            return grad[0][1]
        if fac >= grad[-1][0]:
            return grad[-1][1]

        idx = 0
        for i in range(len(grad)):
            if grad[i][0] > fac:
                idx = i - 1
                break

        size = grad[idx+1][0] - grad[idx][0]
        col_fac = (fac-grad[idx][0]) / size

        return mix_cols(grad[idx][1], grad[idx+1][1], col_fac)


def main():
    inputs = mido.get_input_names()
    print("Found these MIDI inputs:")
    for i, inp in enumerate(inputs):
        print(f"* {i}: {inp}")
    choice = int(input("Enter input number: "))

    port = mido.open_input(inputs[choice])

    try:
        while True:
            msg = port.receive()

            if msg.type == "note_on":
                note = msg.note - 21
                color = interpolate(COLOR_GRADIENT, note / 88)
                color = [int(255*x) for x in colorsys.hsv_to_rgb(*color)]
                led_on(note, color)

            elif msg.type == "note_off":
                note = msg.note - 21
                led_off(note)

    except KeyboardInterrupt:
        port.close()


if __name__ == "__main__":
    main()
