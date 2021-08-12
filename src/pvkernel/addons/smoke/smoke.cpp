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

#define  SIZE_INT  sizeof(int)
#define  SIZE_FLT  sizeof(float)

#include <cstring>
#include <fstream>
#include <vector>
#include "../../utils.hpp"


struct Particle {
    // Contains x, y, velocity x, velocity y
    // x, y are pixel locations.
    // vx, vy are pixel per second values.
    float x, y, vx, vy;
};


void simulate(const int fps_int, const int num_new, const char* ip, const char* op) {
    /*
    Simulate one frame of smoke activity.

    :param fps: Video fps.
    :param num_new: Number of new particles to generate.
    :param ip: Input file path (leave blank if no input).
    :param op: Output file path.
    */

    CD fps = (double)fps_int;   // Using double because division later.

    int num_ptcls = 0;   // Avoid push_back() bc does a boundary check.
    std::vector<Particle> ptcls;
    ptcls.reserve((int)1e6);

    if (strlen(ip) > 0) {
        std::ifstream fp(ip);
        int count;
        fp.read((char*)(&count), SIZE_INT);

        for (int i = 0; i < count; i++) {
            Particle ptcl;
            fp.read((char*)(&ptcl.x), SIZE_FLT);
            fp.read((char*)(&ptcl.y), SIZE_FLT);
            fp.read((char*)(&ptcl.vx), SIZE_FLT);
            fp.read((char*)(&ptcl.vy), SIZE_FLT);
            ptcls[num_ptcls++] = ptcl;
        }
    }
}
