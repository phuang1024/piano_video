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

#include <fstream>

namespace PS {
namespace Midi {

/** Read variable length quantity integer. */
int read_int(std::ifstream& fp);

/** Write variable length quantity integer. */
void write_int(std::ofstream& fp, int value);

/**
 * Class for reading a MIDI file.
 */
class MidiRead {
public:
    MThd header;
};

/**
 * MIDI header chunk.
 */
class MThd {
public:
    ~MThd();
    MThd(std::ifstream* fp);

    char format;
};

}  // namespace Midi
}  // namespace PS
