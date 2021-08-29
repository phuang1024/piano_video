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

typedef  unsigned char       UCH;
typedef  long long           LL;
typedef  unsigned long long  ULL;
typedef  const double        CD;


/**
 * Convert a degree measure to radians.
 */
MODS double radians(CD deg);

/**
 * Convert a radian measure to degrees.
 */
MODS double degrees(CD rad);

/**
 * Hypotenuse of two legs.
 */
MODS double pythag(CD dx, CD dy);

/**
 * Return the bounded integer.
 */
MODS int ibounds(const int v, const int vmin = 0, const int vmax = 1);

/**
 * Return the bounded double.
 */
MODS double dbounds(CD v, CD vmin = 0, CD vmax = 1);

/**
 * Map a value from the old range to a new range.
 */
MODS double map_range(CD v, CD old_min, CD old_max, CD new_min, CD new_max);

/**
 * Whether a piano key is white. 0 = lowest.
 */
MODS bool is_white(const UCH key);

/**
 * Piano key X position.
 * @param start X location start.
 * @param end X location end.
 * @param key key number. 0 = lowest.
 */
MODS double key_pos(CD start, CD end, const UCH key);

/**
 * Check whether the point is inside the image dimensions.
 */
MODS bool img_bounds(const int width, const int height, const int x, const int y);

/**
 * Set pixel and channel to value.
 */
MODS void img_set(UCH* img, const int width, const int x, const int y, const UCH channel, const UCH value);

/**
 * Set pixel to r, g, b args.
 */
MODS void img_setc(UCH* img, const int width, const int x, const int y, const UCH r, const UCH g, const UCH b);

/**
 * Set pixel to color arg.
 */
MODS void img_setc(UCH* img, const int width, const int x, const int y, const UCH* color);

/**
 * Add color to image pixel.
 */
MODS void img_addc(UCH* img, const int width, const int x, const int y, const UCH r, const UCH g, const UCH b);

/**
 * Add color to image pixel.
 */
MODS void img_addc(UCH* img, const int width, const int x, const int y, const UCH* color);

/**
 * Get the value at pixel and channel.
 * @param value the destination pointer. will overwrite to the obtained value.
 */
MODS void img_get(UCH* img, const int width, const int x, const int y, const UCH channel, UCH* value);

/**
 * Get a color of a pixel of an image.
 * @param color destination color array.
 */
MODS void img_getc(UCH* img, const int width, const int x, const int y, UCH* color);

/**
 * Mix two colors with a linear interpolation.
 * @param dest destination color.
 */
MODS void img_mix(UCH* dest, const UCH* c1, const UCH* c2, CD fac);
