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

"""
Compiles C++ and Cuda in the kernel to Shared Object files.
Need to use a Python script because I'm not good with C++ Makefiles.
"""

import os
import time
import shutil
import threading
import argparse
from subprocess import Popen, DEVNULL
from typing import Sequence

CPP: str = shutil.which("g++")
CUDA: str = shutil.which("nvcc")

CPP_FILES: Sequence[str] = (
)
CUDA_FILES: Sequence[str] = (
)


class ProcManager:
    """
    Manages processes.
    """

    def __init__(self, max_procs: int) -> None:
        self.max = max_procs
        self.procs = []
        self.queue = []
        self.running = True

        threading.Thread(target=self.starter).start()

    def starter(self):
        """
        Starts processes from ``self.queue``. Run in a different thread.
        Stops once ``self.running`` is False.
        Will wait for all processes after exiting loop.
        """
        while True:
            time.sleep(0.1)

            while True:
                removed = False
                for i, p in enumerate(self.procs):
                    if p.poll() is not None:
                        self.procs.pop(i)
                        removed = True
                        break
                if not removed:
                    break

            if len(self.queue) > 0:
                args = self.queue.pop(0)
                proc = Popen(args, stdin=DEVNULL, stdout=DEVNULL, stderr=DEVNULL)
                self.procs.append(proc)

            if not self.running:
                break

        for proc in self.procs:
            proc.wait()

    def add_job(self, args: Sequence[str]) -> None:
        self.queue.append(args)


def main():
    parser = argparse.ArgumentParser(description="Compile kernel C++ and Cuda.")
    parser.add_argument("-j", type=int, default=1, help="Max number of compiling processes.")
    parser.add_argument("--cpp", action="store_true", help="Compile C++ files.")
    parser.add_argument("--cuda", action="store_true", help="Compile Cuda files.")
    args = parser.parse_args()

    manager = ProcManager(args.j)
    if args.cpp:
        for file in CPP_FILES:
            prefix = os.path.dirname(file)
            name = ".".join(os.path.basename(file).split(".")[:-1])
            ext = os.path.basename(file).split(".")[-1]
            manager.add_job((CPP, "-O3", "-Wall", "-c", "-fPIC", file))
            manager.add_job((CPP, "-shared", os.path.join(prefix, name+".o"), "-o", os.path.join(prefix, "lib"+name+".so")))


main()
