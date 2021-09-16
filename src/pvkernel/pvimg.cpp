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
 * Implementation for image processing utils.
 */

#include <cmath>
#include <algorithm>
#include "pvutils.hpp"

using std::min;
using std::max;


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

MODS void img_mixadd(UCH* img, const int width, const int x, const int y, CD fac, const UCH r,
        const UCH g, const UCH b) {
    UCH original[3], modified[3];
    const UCH input[3] = {r, g, b};
    img_getc(img, width, x, y, original);
    img_mix(modified, original, input, fac);
    img_setc(img, width, x, y, modified[0], modified[1], modified[2]);
}

MODS void img_mixadd(UCH* img, const int width, const int x, const int y, CD fac, const UCH input[3]) {
    img_mixadd(img, width, x, y, fac, input[0], input[1], input[2]);
}
