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

#ifdef __GNUC__
    #define  MODS
#else
    #define  MODS  __host__ __device__
#endif

#include <cstdlib>
#include <cmath>
#include <ctime>
#include "random.hpp"


namespace Random {
    MODS void seed() {
        srand(std::time(nullptr));
    }


    MODS int randint(const int min, const int max) {
        /* Return int NOT including max */
        return min + (rand() % (max-min));
    }

    MODS double uniform(const double min, const double max) {
        const double num = ((double)rand())/1e9 + (double)rand();
        return min + (fmod(num, max-min));
    }
}
