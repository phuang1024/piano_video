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

#include "utils.hpp"


#ifndef __GNUC__
__host__ __device__
#endif
double radians(CD deg) {
    /* Convert degrees to radians. */
    return deg / 180 * PI;
}

#ifndef __GNUC__
__host__ __device__
#endif
double degrees(CD rad) {
    /* Radians to degrees. */
    return rad / PI * 180;
}

#ifndef __GNUC__
__host__ __device__
#endif
double pythag(CD dx, CD dy) {
    /* Pythagorean distance. */
    return std::pow((dx*dx) + (dy*dy), 0.5);
}

#ifndef __GNUC__
__host__ __device__
#endif
int ibounds(const int v, const int vmin, const int vmax) {
    /* Integer bounds. */
    return min(max(v, vmin), vmax);
}

#ifndef __GNUC__
__host__ __device__
#endif
double dbounds(CD v, CD vmin, CD vmax) {
    /* Double bounds. */
    return min(max(v, vmin), vmax);
}

#ifndef __GNUC__
__host__ __device__
#endif
double map_range(CD v, CD old_min, CD old_max, CD new_min, CD new_max) {
    /* Map value from one range to another */
    CD fac = (v-old_min) / (old_max-old_min);
    CD mapped = fac * (new_max-new_min) + new_min;
    return mapped;
}


#ifndef __GNUC__
__host__ __device__
#endif
bool is_white(const UCH key) {
    /* Is the key white on piano */
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

#ifndef __GNUC__
__host__ __device__
#endif
double key_pos(CD start, CD end, const UCH key) {
    /* Returns the MIDDLE of the key, not the left. */
    CD white_width = (end-start) / 52.0;

    double x = start;
    for (UCH i = 0; i < 88; i++) {
        if (is_white(i)) {
            if (i == key) return x - white_width/2.0;
            x += white_width;
        } else {
            if (i == key) return x - 1.5*white_width;
        }
    }

    return x;
}


#ifndef __GNUC__
__host__ __device__
#endif
void img_set(UCH* img, const UINT width, const UINT x, const UINT y, const UCH channel, const UCH value) {
    /*
    Sets pixel and channel of image to a value.

    :param img: Image.
    :param width: Image width.
    :param x: X coordinate.
    :param y: Y coordinate.
    :param channel: Channel number, corresponding to B, G, R.
    :param value: Number from 0 to 255.
    */
    img[3*(y*width + x) + channel] = value;
}

#ifndef __GNUC__
__host__ __device__
#endif
void img_setc(UCH* img, const UINT width, const UINT x, const UINT y, const UCH r, const UCH g, const UCH b) {
    /*
    Sets pixel to color. Equivalent to three calls of img_set()

    :param img: Image.
    :param width: Image width.
    :param x: X coordinate.
    :param y: Y coordinate.
    :param r, g, b: R, G, B values.
    */
    img_set(img, width, x, y, 0, r);
    img_set(img, width, x, y, 1, g);
    img_set(img, width, x, y, 2, b);
}

#ifndef __GNUC__
__host__ __device__
#endif
void img_get(UCH* img, const UINT width, const UINT x, const UINT y, const UCH channel, UCH* value) {
    /*
    Gets value at pixel and channel and modifies "value" param.

    :param img: Image.
    :param width: Image width.
    :param x: X coordinate.
    :param y: Y coordinate.
    :param channel: Channel number, corresponding to B, G, R.
    :param value: Value pointer. Will be modified to be the obtained value.
    */
    value[0] = img[3*(y*width + x) + channel];
}

#ifndef __GNUC__
__host__ __device__
#endif
void img_getc(UCH* img, const UINT width, const UINT x, const UINT y, UCH* color) {
    /*
    Gets value at pixel and modifies "value" param. Equivalent to 3 calls of img_get()

    :param img: Image.
    :param width: Image width.
    :param x: X coordinate.
    :param y: Y coordinate.
    :param value: Value pointer. Will be modified to be the obtained value.
    */
    img_get(img, width, x, y, 0, color+0);
    img_get(img, width, x, y, 1, color+1);
    img_get(img, width, x, y, 2, color+2);
}

#ifndef __GNUC__
__host__ __device__
#endif
void img_mix(UCH* dest, const UCH* c1, const UCH* c2, CD fac) {
    /*
    Mixes two colors with a factor.

    :param dest: Destination array. Will be modified.
    :param c1: Color 1.
    :param c2: Color 2.
    :param fac: Factor. 0 = full c1, 1 = full c2
    */
    for (int i = 0; i < 3; i++)
        dest[i] = ibounds(c1[i]*(1-fac) + c2[i]*fac, 0, 255);
}
