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

#define  PI  3.14159265

#include <cmath>

typedef  unsigned char       UCH;
typedef  unsigned int        UINT;
typedef  long long           LL;
typedef  unsigned long long  ULL;
typedef  const double        CD;


double radians(CD deg) {
    /*
    Convert degrees to radians.
    */
    return deg/180*2*PI;
}

double pythag(CD dx, CD dy) {
    /*
    Pythagorean distance.

    :param dx: X delta.
    :param dy: Y delta.
    */
    return std::pow((dx*dx) + (dy*dy), 0.5);
}

int ibounds(const int v, const int vmin = 0, const int vmax = 1) {
    /*
    Integer bounds.

    :param v: Value.
    :param vmin: Minimum value.
    :param vmax: Maximum value.
    */
    return min(max(v, vmin), vmax);
}

double dbounds(CD v, CD vmin = 0, CD vmax = 1) {
    /*
    Double bounds.

    :param v: Value.
    :param vmin: Minimum value.
    :param vmax: Maximum value.
    */
    return min(max(v, vmin), vmax);
}
