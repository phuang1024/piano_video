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
#include <string>


namespace Wave {

/**
 * Write wave file. File format and specifications are constant:
 * 32 bit
 * 1 channel
 * 44100 fps
 */
class WaveWrite {
public:
    /**
     * Calls close() if not closed.
     */
    ~WaveWrite();

    /**
     * Initialize with output file path.
     */
    WaveWrite(const std::string path);

    /**
     * Must be called after done writing.
     */
    void close();

    /**
     * Write one frame (signed 32 bit int)
     */
    void write_frame(const int v);

private:
    std::ofstream _fp;
    bool _open;
    int _frames_written;

    void _write_header();
};

}  // namespace Wave
