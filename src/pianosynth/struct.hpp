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

typedef  unsigned char       UCH;
typedef  unsigned short      USHORT;
typedef  unsigned int        UINT;
typedef  long long           LL;
typedef  unsigned long long  ULL;


namespace Struct {

const int _one = 1;
const bool _endian_little = *(char*)(&_one);

/**
 * Write data to file.
 * @param reverse whether to write bytes starting from last.
 */
void write_raw(std::ofstream& fp, const void* data, const int size, const bool reverse);

/**
 * Write data to file.
 * @param little_endian whether to WRITE as little endian.
 */
void write_data(std::ofstream& fp, const void* data, const int size, const bool little_endian);

/**
 * Write number to file.
 * Use the template to specify type.
 * @param little_endian whether to WRITE as little endian.
 */
template<class T>
void write_num(std::ofstream& fp, const T v, const bool little_endian) {
    write_data(fp, &v, sizeof(v), little_endian);
}

}  // namespace Struct
