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
typedef  unsigned int        UINT;
typedef  long long           LL;
typedef  unsigned long long  ULL;
typedef  const double        CD;


double radians(CD deg);
double pythag(CD dx, CD dy);

int ibounds(const int v, const int vmin = 0, const int vmax = 1);
double dbounds(CD v, CD vmin = 0, CD vmax = 1);

bool is_white(const UCH key);
double key_pos(CD start, CD end, const UCH key);

void img_set(UCH* img, const UINT width, const UINT x, const UINT y, const UCH channel, const UCH value);
void img_setc(UCH* img, const UINT width, const UINT x, const UINT y, const UCH r, const UCH g, const UCH b);
void img_get(UCH* img, const UINT width, const UINT x, const UINT y, const UCH channel, UCH* value);
void img_getc(UCH* img, const UINT width, const UINT x, const UINT y, UCH* color);
void img_mix(UCH* dest, const UCH* c1, const UCH* c2, CD fac);
