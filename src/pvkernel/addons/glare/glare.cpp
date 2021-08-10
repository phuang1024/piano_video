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

#include <../../consts.hpp>


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

   for (UCH i = 0; i < num_notes; i++) {
       const UCH note = notes[i];
       CD x_pos = key_pos(x_start, x_end, note);

       for (UINT x = x_pos-radius; x < x_pos+radius; x++) {
           for (UINT y = mid-radius; y < mid+radius; y++) {
               CD dist = pythag(x-x_pos, y-mid);
               CD fac = intensity * (1-(dist/radius));

               UCH original[3], modified[3];
               img_getc(img, width, x, y, original);
               img_mix(modified, original, white, fac);
               img_setc(img, width, x, y, modified[0], modified[1], modified[2]);
           }
       }
   }
}
