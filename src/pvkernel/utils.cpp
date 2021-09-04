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
#include <algorithm>
#include "utils.hpp"

using std::min;
using std::max;


MODS double radians(CD deg) {
    return deg / 180 * PI;
}

MODS double degrees(CD rad) {
    return rad / PI * 180;
}

MODS double pythag(CD dx, CD dy) {
    #if CPP
        return std::pow((dx*dx) + (dy*dy), 0.5);
    #else
        return pow((dx*dx) + (dy*dy), 0.5);
    #endif
}

MODS int ibounds(const int v, const int vmin, const int vmax) {
    return min(max(v, vmin), vmax);
}

MODS double dbounds(CD v, CD vmin, CD vmax) {
    return min(max(v, vmin), vmax);
}

MODS double map_range(CD v, CD old_min, CD old_max, CD new_min, CD new_max) {
    CD fac = (v-old_min) / (old_max-old_min);
    CD mapped = fac * (new_max-new_min) + new_min;
    return mapped;
}

MODS void mat_2x2inv(float dest[4], const float src[4]) {
    CD det = src[0]*src[3] - src[1]*src[2];
    dest[0] = src[3] / det;
    dest[1] = -src[1] / det;
    dest[2] = -src[2] / det;
    dest[3] = src[0] / det;
}


MODS bool is_white(const UCH key) {
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

MODS double key_pos(CD start, CD end, const UCH key) {
    // For some reason we need to subtract one white width from the pos
    CD white_width = (end-start) / 52.0;

    double x = start;
    for (UCH i = 0; i < 88; i++) {
        if (is_white(i)) {
            if (i == key) return x - white_width/2.0;
            x += white_width;
        } else {
            if (i == key) return x - white_width;
        }
    }

    return x;
}


MODS bool img_bounds(const int width, const int height, const int x, const int y) {
    return ((0<=x && x<width) && (0<=y && y<height));
}

MODS void img_set(UCH* img, const int width, const int x, const int y, const UCH channel, const UCH value) {
    img[3*(y*width + x) + channel] = value;
}

MODS void img_setc(UCH* img, const int width, const int x, const int y, const UCH r, const UCH g, const UCH b) {
    img_set(img, width, x, y, 0, r);
    img_set(img, width, x, y, 1, g);
    img_set(img, width, x, y, 2, b);
}

MODS void img_setc(UCH* img, const int width, const int x, const int y, const UCH* color) {
    img_setc(img, width, x, y, color[0], color[1], color[2]);
}

MODS void img_addc(UCH* img, const int width, const int x, const int y, const UCH r, const UCH g, const UCH b) {
    UCH current[3];
    img_getc(img, width, x, y, current);

    img_set(img, width, x, y, 0, max(r, current[0]));
    img_set(img, width, x, y, 1, max(g, current[1]));
    img_set(img, width, x, y, 2, max(b, current[2]));
}

MODS void img_addc(UCH* img, const int width, const int x, const int y, const UCH* color) {
    img_addc(img, width, x, y, color[0], color[1], color[2]);
}

MODS void img_get(UCH* img, const int width, const int x, const int y, const UCH channel, UCH* value) {
    value[0] = img[3*(y*width + x) + channel];
}

MODS void img_getc(UCH* img, const int width, const int x, const int y, UCH* color) {
    img_get(img, width, x, y, 0, color+0);
    img_get(img, width, x, y, 1, color+1);
    img_get(img, width, x, y, 2, color+2);
}

MODS void img_mix(UCH* dest, const UCH* c1, const UCH* c2, CD fac) {
    for (int i = 0; i < 3; i++)
        dest[i] = ibounds(c1[i]*(1-fac) + c2[i]*fac, 0, 255);
}
