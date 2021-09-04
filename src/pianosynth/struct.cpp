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

#include <iostream>
#include <fstream>
#include "struct.hpp"


namespace Struct {

void write_raw(std::ofstream& fp, const void* _data, const int size, const bool reverse) {
    const char* data = (char*)_data;

    if (reverse) {
        for (int i = size-1; i >= 0; i--)
            fp.write(data+i, 1);
    } else {
        fp.write(data, size);
    }
}

void write_num(std::ofstream& fp, const void* _data, const int size, const bool little_endian) {
    const char* data = (char*)_data;

    write_raw(fp, data, size, little_endian != _endian_little);
}

}  // namespace Struct
