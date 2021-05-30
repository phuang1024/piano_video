#
#  Megalodon
#  UCI chess engine
#  Copyright the Megalodon developers
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

# Checks if there is trailing whitespace in source files.

import os

PARENT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
FILE_DIRS = [
    os.path.join(PARENT, "src"),
    os.path.join(PARENT, "tests"),
]


def main():
    exitcode = 0

    dirs = FILE_DIRS[:]
    while len(dirs) > 0:
        fdir = dirs.pop(0)
        for f in os.listdir(fdir):
            path = os.path.join(fdir, f)
            relpath = os.path.join(os.path.basename(fdir), f)
            if os.path.isfile(path):
                try:
                    with open(path, "r") as file:
                        data = file.read()
                        for i, l in enumerate(data.split("\n")):
                            if l.endswith(" "):
                                print(f"Trailing whitespace in file {relpath}, line {i+1}")
                                exitcode = 1
                        if not data.endswith("\n"):
                            print(f"No blank line at the end of file {relpath}")
                            exitcode = 1

                except UnicodeDecodeError:
                    pass

            elif os.path.isdir(path):
                dirs.append(path)

    return exitcode


exit(main())
