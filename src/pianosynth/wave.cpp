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
#include "struct.hpp"
#include "wave.hpp"


namespace Wave {

WaveWrite::~WaveWrite() {
    if (_open)
        close();
}

WaveWrite::WaveWrite(const std::string path) {
    _fp = std::ofstream(path);
    _open = true;
    _frames_written = 0;
}

void WaveWrite::close() {
    if (_open) {
        _write_header();
        _open = false;
        _fp.close();
    }
}

void WaveWrite::write_frame(const int v) {
    Struct::write_num<int>(_fp, v, true);
    _frames_written++;
}

void WaveWrite::_write_header() {
    const int data_len = _frames_written * 4;

    _fp.seekp(0);
    _fp.write("RIFF", 4);
    Struct::write_num<UINT>(_fp, 36+data_len, true);    // Data length including header
    _fp.write("WAVE", 4);
    _fp.write("fmt ", 4);
    Struct::write_num<UINT>(_fp, 16, true);       // Something
    Struct::write_num<USHORT>(_fp, 1, true);      // Audio format PCM
    Struct::write_num<USHORT>(_fp, 1, true);      // One channel
    Struct::write_num<UINT>(_fp, 44100, true);    // FPS
    Struct::write_num<UINT>(_fp, 44100*4, true);  // FPS * nchannels * sampwidth
    Struct::write_num<USHORT>(_fp, 4, true);      // nchannels * sampwidth
    Struct::write_num<USHORT>(_fp, 32, true);     // sampwidth * 4
    _fp.write("data", 4);
    Struct::write_num<UINT>(_fp, data_len, true); // length of actual audio
}

}  // namespace Wave
