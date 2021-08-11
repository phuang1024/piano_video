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

/*
Cuda implementations for util functions.
*/

#include "utils_cu.cuh"


__host__ __device__ double radians(CD deg) {
    /*
    Convert degrees to radians.
    */
    return deg / 180 * PI;
}

__host__ __device__ double degrees(CD rad) {
    /*
    Radians to degrees.
    */
    return rad / PI * 180;
}

__host__ __device__ double pythag(CD dx, CD dy) {
    /*
    Pythagorean distance.

    :param dx: X delta.
    :param dy: Y delta.
    */
    return std::pow((dx*dx) + (dy*dy), 0.5);
}

__host__ __device__ int ibounds(const int v, const int vmin, const int vmax) {
    /*
    Integer bounds.

    :param v: Value.
    :param vmin: Minimum value.
    :param vmax: Maximum value.
    */
    return min(max(v, vmin), vmax);
}

__host__ __device__ double dbounds(CD v, CD vmin, CD vmax) {
    /*
    Double bounds.

    :param v: Value.
    :param vmin: Minimum value.
    :param vmax: Maximum value.
    */
    return min(max(v, vmin), vmax);
}

__host__ __device__ double map_range(CD v, CD old_min, CD old_max, CD new_min, CD new_max) {
    CD fac = (v-old_min) / (old_max-old_min);
    CD mapped = fac * (new_max-new_min) + new_min;
    return mapped;
}


__host__ __device__ bool is_white(const UCH key) {
    const UCH num = (key-3) % 12;
    switch (num) {
        case 1: return false;
        case 3: return false;
        case 6: return false;
        case 8: return false;
        case 10: return false;
        default: return true;
    }
}

__host__ __device__ double key_pos(CD start, CD end, const UCH key) {
    // FIXME BUGGY
    CD white_width = (end-start) / 52.0;

    double x = 0;
    for (UCH i = 0; i < key; i++) {
        if (is_white(i))
            x += white_width;
    }
    if (is_white(key))
        x += white_width/2.0;

    return x;
}
