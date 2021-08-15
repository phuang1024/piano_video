#
#  Piano Video
#  A free piano visualizer.
#  Copyright Patrick Huang 2021
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

CXX = g++
CXXFLAGS = -Wall -O3 -c -fPIC
CXXFILES = psmidi.o


.PHONY: all compile clean

all: compile clean

compile: $(CXXFILES)
	$(CXX) -shared $(CXXFILES) -o libpsmidi.so
	cp *.hpp ../include
	cp libpsmidi.so ../lib

clean:
	rm *.o
