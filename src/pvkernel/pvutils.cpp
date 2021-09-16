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

/**
 * Implementation for general purpose utils.
 */

#include <cmath>
#include <algorithm>
#include "pvutils.hpp"

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


MODS void hsv2rgb(UCH dest[3], CD src[3]) {
    const double h = src[0], s = src[1], v = src[2];

    const double c = s * v;
    const double x = c * (1 - fabs(fmod(h*6, 2) - 1));
    const double m = v - c;

    // r prime, g prime, b prime
    double rp, gp, bp;
    if (h < 1.0/6) {
        rp = c; gp = x; bp = 0;
    } else if (h < 2.0/6) {
        rp = x; gp = c; bp = 0;
    } else if (h < 3.0/6) {
        rp = 0; gp = c; bp = x;
    } else if (h < 4.0/6) {
        rp = 0; gp = x; bp = c;
    } else if (h < 5.0/6) {
        rp = x; gp = 0; bp = c;
    } else {
        rp = c; gp = 0; bp = x;
    }

    const double r = (rp + m) * 255;
    const double g = (gp + m) * 255;
    const double b = (bp + m) * 255;
    dest[0] = r;
    dest[1] = g;
    dest[2] = b;
}

MODS void hsv2rgb(UCH dest[3], CD h, CD s, CD v) {
    const double src[3] = {h, s, v};
    hsv2rgb(dest, src);
}
