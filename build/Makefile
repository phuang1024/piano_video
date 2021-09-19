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

VERSION = 0.4.0

.PHONY: all clean api kernel

all: api kernel

clean:
	mv dist/*.whl .
	rm -rf pvkernel
	rm -rf pv
	rm -rf build dist *.egg-info

api:
	rm -rf pv
	cp -r ../src/pv .
	python package.py "pv" "Piano Video API" "$(VERSION)"

kernel:
	rm -rf pvkernel
	cp -r ../src/pvkernel .
	cp -r ../src/pvaddons pvkernel/pvaddons
	python package.py "pvkernel" "Piano Video kernel" "$(VERSION)"
