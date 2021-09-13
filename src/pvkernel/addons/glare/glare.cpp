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

#include <algorithm>
#include <cmath>
#include <iostream>
#include "../../utils.hpp"
#include "../../random.hpp"


/**
 * Render the glare on an image.
 * @param img Image.
 * @param width height: Image dimensions.
 * @param intensity Glare intensity factor.
 * @param radius Glare radius.
 * @param notes Array of notes to add glare to (0 is lowest note).
 * @param num_notes Number of notes.
 * @param x_start X pixel start of piano.
 * @param x_end X pixel end of piano.
 */
extern "C" void glare(UCH* img, const int width, const int height, CD intensity, CD radius,
        const UCH* notes, const UCH num_notes, CD x_start, CD x_end) {
    const double mid = height / 2.0;
    const UCH white[3] = {255, 255, 255};
    const int border = 25;

    for (UCH i = 0; i < num_notes; i++) {
        const UCH note = notes[i];
        const double x_pos = key_pos(x_start, x_end, note);
        const double curr_intensity = intensity - Random::uniform(0, 0.1);
        const double rad = radius * Random::uniform(1, 0.9);   // Current radius

        for (int x = x_pos-rad-border; x < x_pos+rad+border; x++) {
            for (int y = mid-rad-border; y < mid+rad+border; y++) {
                // const double dx = abs(x-x_pos), dy = abs(y-mid);
                const double dist = pythag(x-x_pos, y-mid);
                const double dist_fac = dist / rad;

                if (dist_fac < 0.5) {
                    const double fac = std::pow(map_range(dist_fac, 0, 0.5, 0.9, 0.3), 2);
                    img_mixadd(img, width, x, y, fac, white);
                } else if (dist_fac < 1) {
                    const double h = map_range(dist_fac, 0.5, 1, 0, 0.8);
                    const double s = 0.5;
                    const double v = dbounds(map_range(dist_fac, 0.5, 1, 0.16, 0)) * curr_intensity;
                    UCH color[3];
                    hsv2rgb(color, h, s, 1);
                    img_mixadd(img, width, x, y, v, color);
                }
            }
        }
    }
}
