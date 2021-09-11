//
//  Piano Video
//  A free piano visualizer.
//  Copyright Patrick Huang 2021
//
//  This program is free software: you can redistribute it and/or modify
//  it under the terms of the GNU General Public License as published by
//  the Free Software Foundation, either version 3 of the License, or
//  (at your option) any later version.
//
//  This program is distributed in the hope that it will be useful,
//  but WITHOUT ANY WARRANTY; without even the implied warranty of
//  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//  GNU General Public License for more details.
//
//  You should have received a copy of the GNU General Public License
//  along with this program.  If not, see <https://www.gnu.org/licenses/>.
//

#include <cmath>
#include <fstream>
#include <iostream>
#include "struct.hpp"
#include "wave.hpp"


/**
 * This function is called by the Python CLI tool.
 *
 * Invoke:
 *  ./pianosynth out.wav
 *
 * stdin:
 *  num_events
 *  event1 opt1 opt2
 *  event2 opt3 opt4
 *  ...
 *
 * Available events:
 *  Note on: note_on note velocity
 *  Note off: note_off note
 *  Damper set: damper value
 * Lowest note on piano has a value of 0
 */
int main(int argc, char** argv) {
    Wave::WaveWrite fp(argv[1]);

    for (int i = 0; i < (int)1e5; i++) {
        const int v = 100000000. * sin((double)i/33.0);
        fp.write_frame(v);
    }
}
