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
CUDA = nvcc

CXXFLAGS = -Wall -O3 -c -fPIC
CXXFILES = utils.o random.o draw/draw.o addons/glare/glare.o addons/smoke/smoke.o \
	addons/particles/particles.o

CUFLAGS = -dc -Xptxas -O3 -use_fast_math -c -Xcompiler -fPIC
CUFILES = utils_cu.o random_cu.o

.PHONY: all cpp cuda clean

# Useful targets

all: cpp cuda clean

cpp: $(CXXFILES)
	$(CXX) -shared -o libpvkernel.so $(CXXFILES)

cuda: $(CUFILES)
	$(CUDA) -shared -o libpvkernel.cu.so $(CUFILES)

clean:  # for some reason needs to do it twice
	find . -name "*.o" -delete
	find . -name "*.o" -delete


# Cuda files

utils_cu.o:
	$(CUDA) $(CUFLAGS) utils.cpp -o utils_cu.o

random_cu.o:
	$(CUDA) $(CUFLAGS) random.cpp -o random_cu.o
