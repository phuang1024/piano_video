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
#include "../../utils.hpp"


extern "C" void glare(UCH* img, const UINT width, const UINT height, CD intensity, CD radius,
        const UCH* notes, const UCH num_notes, CD x_start, CD x_end) {
    /*
    Add the glare.

    :param img: Image.
    :param width, height: Image dimensions.
    :param intensity: Glare intensity factor.
    :param radius: Glare radius.
    :param notes: Array of notes to add glare to (0 is lowest note).
    :param num_notes: Number of notes.
    :param x_start: X pixel start of piano.
    :param x_end: X pixel end of piano.
    */

    CD mid = height / 2.0;
    const UCH white[3] = {255, 255, 255};
    const UINT border = 25;

    for (UCH i = 0; i < num_notes; i++) {
        const UCH note = notes[i];
        CD x_pos = key_pos(x_start, x_end, note);

        for (UINT x = x_pos-radius-border; x < x_pos+radius+border; x++) {
            for (UINT y = mid-radius-border; y < mid+radius+border; y++) {
                CD dx = abs(x-x_pos), dy = abs(y-mid);
                CD dist = pythag(x-x_pos, y-mid);
                CD dist_fac = dist / radius;

                // Streaks every 45 degrees
                CD angle = degrees(atan(dy/dx));
                CD angle_dist = min(min(abs(angle), abs(angle-45)), abs(angle-90));
                CD angle_fac = dbounds(map_range(angle_dist, 0, 5, 0.96, 1));

                CD fac = dbounds(angle_fac * dist_fac);   // 0 = full white, 1 = no white
                CD real_fac = 1 - ((1-fac)*intensity);    // Account for intensity
                UCH original[3], modified[3];
                img_getc(img, width, x, y, original);
                img_mix(modified, white, original, real_fac);
                img_setc(img, width, x, y, modified[0], modified[1], modified[2]);
            }
        }
    }
}
