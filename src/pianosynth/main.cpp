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


int main() {
    Wave::WaveWrite fp("a.wav");

    for (int i = 0; i < (int)1e7; i++) {
        const int v = 100000000 * sin((double)i/33.0);
        fp.write_frame(v);
    }
}
