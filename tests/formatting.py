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

import sys
import os
import pathlib

RED = "\x1b[31m"
GREEN = "\x1b[32m"

# List of (dir, recursive, (glob1, glob2, glob3))
PATHS = (
#     (".",         False, ("*.md", "*.gitignore", "*.txt")),
#     ("./build",   False, ("*.py",)),
#     ("./docs",    False, ("*.rst",)),
#     ("./scripts", True,  ("*.py",)),
#     ("./src",     True,  ("*.py", "*.c", "*.cpp")),
#     ("./tests",   True,  ("*.py",)),
)


def test_file(path):
    msg = "OK"
    exitcode = 0

    with open(path, "r") as file:
        data = file.read()

    if not data.endswith("\n"):
        msg = "no blank line at the end"
        exitcode = 1

    for i, line in enumerate(data.split("\n")):
        if line.endswith(" "):
            msg = f"line {i+1}: trailing whitespace"
            exitcode = 1

    sys.stdout.write(GREEN if exitcode == 0 else RED)
    print(path, msg)

    return exitcode


def test_dir(directory, rec, globs):
    exitcode = 0

    for file in os.listdir(directory):
        path = os.path.join(directory, file)
        abspath = os.path.realpath(path)

        if rec and os.path.isdir(abspath):
            exitcode = max(exitcode, test_dir(path, rec, globs))

    path = pathlib.Path(directory)
    for glob in globs:
        for relpath in path.glob(glob):
            abspath = os.path.realpath(relpath)
            if os.path.isfile(abspath):
                exitcode = max(exitcode, test_file(relpath))

    return exitcode


def main():
    exitcode = 0
    for path in PATHS:
        exitcode = max(exitcode, test_dir(*path))
    return exitcode


exit(main())
