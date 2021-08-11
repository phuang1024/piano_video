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

int ibounds(const int v, const int vmin, const int vmax) {
    /*
    Integer bounds.

    :param v: Value.
    :param vmin: Minimum value.
    :param vmax: Maximum value.
    */
    return min(max(v, vmin), vmax);
}

double dbounds(CD v, CD vmin, CD vmax) {
    /*
    Double bounds.

    :param v: Value.
    :param vmin: Minimum value.
    :param vmax: Maximum value.
    */
    return min(max(v, vmin), vmax);
}


bool is_white(const UCH key) {
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

double key_pos(CD start, CD end, const UCH key) {
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

void img_mix(UCH* dest, const UCH* c1, const UCH* c2, CD fac) {
    /*
    Mixes two colors with a factor.

    :param dest: Destination array. Will be modified.
    :param c1: Color 1.
    :param c2: Color 2.
    :param fac: Factor. 0 = full c1, 1 = full c2
    */
    for (int i = 0; i < 3; i++)
        dest[i] = c1[i]*(1-fac) + c2[i]*fac;
}
