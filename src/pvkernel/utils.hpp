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

#pragma once

#ifdef __CUDACC__
    #define  MODS  __host__ __device__
    #define  CPP  false

    // Typical GPU has 1500 cores so going above won't help
    #define  CU_BLOCK_SIZE  256
    #define  CU_BLOCK_CNT   6
#else
    #define  MODS
    #define  CPP  true
#endif

#define  PI  3.14159265

#include <cmath>
#include <algorithm>

using std::min;
using std::max;

typedef  unsigned char       UCH;
typedef  long long           LL;
typedef  unsigned long long  ULL;
typedef  const double        CD;


MODS double radians(CD deg);
MODS double degrees(CD rad);
MODS double pythag(CD dx, CD dy);

MODS int ibounds(const int v, const int vmin = 0, const int vmax = 1);
MODS double dbounds(CD v, CD vmin = 0, CD vmax = 1);
MODS double map_range(CD v, CD old_min, CD old_max, CD new_min, CD new_max);

MODS bool is_white(const UCH key);
MODS double key_pos(CD start, CD end, const UCH key);

MODS bool img_bounds(const int width, const int height, const int x, const int y);
MODS void img_set(UCH* img, const int width, const int x, const int y, const UCH channel, const UCH value);
MODS void img_setc(UCH* img, const int width, const int x, const int y, const UCH r, const UCH g, const UCH b);
MODS void img_setc(UCH* img, const int width, const int x, const int y, const UCH* color);
MODS void img_get(UCH* img, const int width, const int x, const int y, const UCH channel, UCH* value);
MODS void img_getc(UCH* img, const int width, const int x, const int y, UCH* color);
MODS void img_mix(UCH* dest, const UCH* c1, const UCH* c2, CD fac);
