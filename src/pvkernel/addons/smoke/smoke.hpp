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

#define  SIZE_INT  sizeof(int)
#define  SIZE_FLT  sizeof(float)

#define  AIR_RESIST  0.95
#define  MAX_AGE     6
#define  DIFF_DIST   4
#define  DIFF_STR    1


struct SmokePtcl {
    SmokePtcl() {
        good = true;
    }

    bool good;  // Whether to read from cache

    float age;  // Seconds

    // x, y are pixel locations.
    // vx, vy are pixel per frame values.
    float x, y, vx, vy;
};
