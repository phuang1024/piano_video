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

#include <iostream>
#include "smoke.hpp"
#include "../../utils.hpp"


void smoke_sim_diff(SmokePtcl* ptcls, const int size, CD strength) {
    for (int i = 0; i < size-1; i++) {
        for (int j = i+1; j < size; j++) {
            SmokePtcl* p1 = &ptcls[i];
            SmokePtcl* p2 = &ptcls[j];
            CD dx = p1->x - p2->x, dy = p1->y - p2->y;
            CD dist = pythag(dx, dy);

            if (dist <= DIFF_DIST) {
                CD curr_strength = strength * (1-(dist/DIFF_DIST));

                // ddx = delta (delta x) = change in velocity
                CD total_vel = dx + dy;
                CD ddx = curr_strength * (dx/total_vel), ddy = curr_strength * (dy/total_vel);

                p1->vx += ddx;
                p1->vy += ddy;
                p2->vx -= ddx;
                p2->vy -= ddy;
            }
        }
    }
}
