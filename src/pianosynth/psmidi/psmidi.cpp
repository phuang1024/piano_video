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

#include <fstream>
#include "psmidi.hpp"

namespace PS {
namespace Midi {

int read_int(std::ifstream& fp) {
    int value = 0;
    while (true) {
        char num;
        fp.read(&num, sizeof(char));
        value = (value<<7) + (num&127);
        if (!(num&128))
            break;
    }
    return value;
}

void write_int(std::ofstream& fp, int value) {
    while (true) {
        const char n = value & 127;
        value = value >> 7;
        const char bit = (value == 0) ? 0 : 1;
        const char byte = n + (bit<<7);
        fp.write(&byte, sizeof(char));
        if (!bit)
            break;
    }
}

}  // namespace Midi
}  // namespace PS
