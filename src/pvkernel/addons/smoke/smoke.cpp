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
#include "../../random.hpp"
#include "../../utils.hpp"


struct Particle {
    // Contains x, y, velocity x, velocity y
    // x, y are pixel locations.
    // vx, vy are pixel per frame values.
    float x, y, vx, vy;
};


void simulate(const int fps_int, const int num_new, CD x_start, CD x_end, CD y_start, CD x_vel_min, CD x_vel_max,
        CD y_vel_min, CD y_vel_max, const char* ip, const char* op) {
    /*
    Simulate one frame of smoke activity.

    :param fps: Video fps.
    :param num_new: Number of new particles to generate.
    :param x_start, x_end: X coordinate boundaries.
    :param y_start: Y coordinate.
    :param x_vel_min, x_vel_max, y_vel_min, y_vel_max: Pixels per second bounds.
    :param ip: Input file path (leave blank if no input).
    :param op: Output file path.
    */

    // Type and/or format conversion
    CD fps = (double)fps_int;
    CD vx_min = x_vel_min/fps, vx_max = x_vel_max/fps;
    CD vy_min = y_vel_min/fps, vy_max = y_vel_max/fps;

    std::vector<Particle> ptcls;
    ptcls.reserve((int)1e6);

    // Read from input file
    if (strlen(ip) > 0) {
        std::ifstream fin(ip);
        int count;
        fin.read((char*)(&count), SIZE_INT);

        for (int i = 0; i < count; i++) {
            Particle ptcl;
            fin.read((char*)(&ptcl.x), SIZE_FLT);
            fin.read((char*)(&ptcl.y), SIZE_FLT);
            fin.read((char*)(&ptcl.vx), SIZE_FLT);
            fin.read((char*)(&ptcl.vy), SIZE_FLT);
            ptcls.push_back(ptcl);
        }
    }

    // Add new particles
    for (int i = 0; i < num_new; i++) {
        Particle ptcl;
        ptcl.x = Random::uniform(x_start, x_end);
        ptcl.y = y_start;
        ptcl.vx = Random::uniform(vx_min, vx_max);
        ptcl.vx = Random::uniform(vy_min, vy_max);
    }

    const int size = ptcls.size();

    // Simulate motion
    for (int i = 0; i < size; i++) {
        Particle& ptcl = ptcls[i];
        ptcl.x += ptcl.vx;
        ptcl.y += ptcl.vy;
    }

    // Write to output
    std::ofstream fout(op);
    fout.write((char*)(&size), SIZE_INT);
    for (int i = 0; i < size; i++) {
        const Particle& ptcl = ptcls[i];
        fout.write((char*)(&ptcl.x), SIZE_FLT);
        fout.write((char*)(&ptcl.y), SIZE_FLT);
        fout.write((char*)(&ptcl.vx), SIZE_FLT);
        fout.write((char*)(&ptcl.vy), SIZE_FLT);
    }
}
