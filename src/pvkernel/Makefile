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

C_FLAGS = -Wall -O3 -c -fPIC
CU_FLAGS = -Xptxas -O3 -use_fast_math -c -Xcompiler -fPIC
C_FILES = utils.o draw/draw.o addons/imgfilter/cppblur.o addons/glare/glare.o
CU_FILES = addons/imgfilter/cublur.o

.PHONY: clean cpp

# Useful targets

cpp: $(C_FILES)
	$(CXX) -shared -o libpvkernel.so $(C_FILES)

cuda: $(CU_FILES)
	$(CUDA) -shared -o libpvkernel.cu.so $(CU_FILES)

clean:
	find . -name *.o -delete


# C files

utils.o:
	$(CXX) $(C_FLAGS) utils.cpp

draw/draw.o:
	cd ./draw; \
	$(CXX) $(C_FLAGS) draw.cpp

addons/imgfilter/cppblur.o:
	cd ./addons/imgfilter; \
	$(CXX) $(C_FLAGS) cppblur.cpp

addons/glare/glare.o:
	cd ./addons/glare; \
	$(CXX) $(C_FLAGS) glare.cpp


# Cuda files

addons/imgfilter/cublur.o:
	cd ./addons/imgfilter; \
	$(CUDA) $(CU_FLAGS) cublur.cu
