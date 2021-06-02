//
//  Piano Video
//  Piano MIDI visualizer
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
#include <fstream>
#include <string>

using std::cout;
using std::cin;
using std::endl;
using std::string;

typedef  unsigned char  UCH;
typedef  unsigned int   UINT;


/*
Pass arguments through stdin
$ ./smoke.out
cache_dir
pathsep
width height fps
*/


int main(const int argc, const char** argv) {
    string cache_dir, pathsep;
    UINT width, height, fps;
    getline(cin, cache_dir);
    getline(cin, pathsep);
    cin >> width >> height >> fps;
}
