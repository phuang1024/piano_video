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

#define  PI  3.14159265

#include <cmath>
#include <algorithm>

using std::min;
using std::max;

typedef  unsigned char       UCH;
typedef  long long           LL;
typedef  unsigned long long  ULL;
typedef  const double        CD;


#ifndef __GNUC__
__host__ __device__
#endif
double radians(CD deg);

#ifndef __GNUC__
__host__ __device__
#endif
double degrees(CD rad);

#ifndef __GNUC__
__host__ __device__
#endif
double pythag(CD dx, CD dy);


#ifndef __GNUC__
__host__ __device__
#endif
int ibounds(const int v, const int vmin = 0, const int vmax = 1);

#ifndef __GNUC__
__host__ __device__
#endif
double dbounds(CD v, CD vmin = 0, CD vmax = 1);

#ifndef __GNUC__
__host__ __device__
#endif
double map_range(CD v, CD old_min, CD old_max, CD new_min, CD new_max);


#ifndef __GNUC__
__host__ __device__
#endif
bool is_white(const UCH key);

#ifndef __GNUC__
__host__ __device__
#endif
double key_pos(CD start, CD end, const UCH key);


#ifndef __GNUC__
__host__ __device__
#endif
void img_set(UCH* img, const int width, const int x, const int y, const UCH channel, const UCH value);

#ifndef __GNUC__
__host__ __device__
#endif
void img_setc(UCH* img, const int width, const int x, const int y, const UCH r, const UCH g, const UCH b);

#ifndef __GNUC__
__host__ __device__
#endif
void img_get(UCH* img, const int width, const int x, const int y, const UCH channel, UCH* value);

#ifndef __GNUC__
__host__ __device__
#endif
void img_getc(UCH* img, const int width, const int x, const int y, UCH* color);

#ifndef __GNUC__
__host__ __device__
#endif
void img_mix(UCH* dest, const UCH* c1, const UCH* c2, CD fac);
