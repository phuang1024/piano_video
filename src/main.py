#
#  Piano Video
#  Piano MIDI visualizer
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

import sys
import os
import shutil
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

import time
import signal
import argparse
import json
from gui import gui
from gui_utils import *


class SIGINT_Handler:
    threshold = 2

    def __init__(self, safe, verbose=False):
        printer = VerbosePrinter(verbose)

        self.safe = safe
        if safe:
            printer(f"Safe mode activated, threshold = {self.threshold} seconds")

    def __enter__(self):
        self.old_handler = signal.signal(signal.SIGINT, self.handler)
        self.last_int = 0

    def __exit__(self, type, value, traceback):
        signal.signal(signal.SIGINT, self.old_handler)

    def handler(self, sig, frame):
        if self.safe:
            t = time.time()
            if t - self.last_int < self.threshold:
                self.exit()
                return

            colors.red
            print("SIGINT received. Continuing because Safe Mode is activated.")
            print(f"Send SIGINT again in the next {self.threshold} seconds to exit.")
            colors.reset

            self.last_int = t

        else:
            self.exit()

    def exit(self):
        print(f"Received SIGINT, exiting normally.")
        set_run(False)


def init(verbose=False):
    printer = VerbosePrinter(verbose)
    printer("Initializing")

    for directory in ADDON_PATHS:
        printer(f"  Making add-on directory {directory}")
        os.makedirs(directory, exist_ok=True)

    printer(f"  Making config directory {CONFIG_PATH}")
    os.makedirs(CONFIG_PATH, exist_ok=True)

    if not os.path.isfile(ADDON_CONFIG_PATH):
        printer(f"  Initializing add-on config {ADDON_CONFIG_PATH}")
        data = []

        for directory in ADDON_PATHS:
            if os.path.isdir(directory):
                for file in sorted(os.listdir(directory)):
                    path = os.path.join(directory, file)
                    mod = import_file(path)
                    if hasattr(mod, "pv_info"):
                        data.append({
                            "path": path,
                            "info": mod.pv_info,
                            "activated": True,
                            "link": False,
                        })

        with open(ADDON_CONFIG_PATH, "w") as file:
            json.dump(data, file, indent=4)


def import_file(path):
    sys.path.insert(0, os.path.dirname(path))
    mod = __import__(os.path.splitext(os.path.basename(path))[0])
    sys.path.pop(0)
    return mod


def setup_addons(action: str, verbose: bool = False):
    printer = VerbosePrinter(verbose)
    printer(f"Setup add-ons: {action}")

    with open(ADDON_CONFIG_PATH, "r") as file:
        data = json.load(file)

    for addon in data:
        if addon["activated"]:
            path = addon["path"]
            if os.path.isfile(path):
                file = os.path.basename(path)
                printer(f"  Setting up {file}")
                mod = import_file(path)
                if hasattr(mod, action):
                    getattr(mod, action)()

    printer(f"  Exiting add-on setup")


def test_modules(verbose=False):
    printer = VerbosePrinter(verbose)
    printer("Testing dependent modules")
    for mod in DEPENDENCIES:
        printer(f"  Importing \"{mod}\"")
        __import__(mod)


def run(args):
    vb = args.verbose
    setup_addons("register", verbose=vb)
    if args.test:
        test_modules(verbose=vb)
    else:
        gui(verbose=vb)
    setup_addons("unregister", verbose=vb)


def trunc(s, length):
    if len(s) >= length:
        return s[:length-3] + "..."
    return s + " "*(length-len(s))


def manage_addons(cmds):
    parser = argparse.ArgumentParser(description="Manage your Piano Video add-ons")
    parser.add_argument("cmd", nargs="?", choices=["help", "list", "info", "act", "dact", "rm", "inst", "link"])
    parser.add_argument("opts", nargs="*")
    args = parser.parse_args(cmds)

    num = int(args.opts[0])-1 if len(args.opts) > 0 else None
    with open(ADDON_CONFIG_PATH, "r") as file:
        data = json.load(file)
    addon = None if num is None else data[num]

    if args.cmd not in (None, "help", "list", "inst", "link") and (num is None or not 0 <= num < len(data)) or addon is None:
        print("Invalid add-on number.")
        return

    if args.cmd == "help" or args.cmd is None:
        parser.print_help(sys.stderr)

    elif args.cmd == "list":
        row  = "+-----+-----------------------+------------------------------+-----------+"
        head = "| Num |       File Name       |       Parent Directory       | Activated |"
        print(row)
        print(head)

        num = 1
        for addon in data:
            sys.stdout.write(row)
            sys.stdout.write("\n| ")
            sys.stdout.write(trunc(str(num), 3))
            sys.stdout.write(" | ")
            sys.stdout.write(trunc(os.path.basename(addon["path"]), 21))
            sys.stdout.write(" | ")
            sys.stdout.write(trunc(os.path.basename(os.path.dirname(addon["path"])), 28))
            sys.stdout.write(" | ")
            sys.stdout.write(trunc("True" if addon["activated"] else "False", 9))
            sys.stdout.write(" |\n")
            num += 1
        print(row)

    elif args.cmd == "info":
        print("File path: ", addon["path"])
        print("Activated: ", addon["activated"])
        print("Included metadata:")
        print(json.dumps(addon["info"], indent=4))

    elif args.cmd == "dact":
        data[num]["activated"] = False

    elif args.cmd == "act":
        data[num]["activated"] = True

    elif args.cmd == "rm":
        path = data[num]["path"]
        if not data[num]["link"]:
            if input(f"Remove path {path} permanently? [y/N] ").lower().strip() != "y":
                return
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)
        else:
            print("Removed add-on internal data (the file is not deleted).")
        data.pop(num)

    elif args.cmd == "inst":
        path = os.path.realpath(input("Enter file or directory path: "))
        mod = import_file(path)

        if hasattr(mod, "pv_info"):
            if os.path.isfile(path):
                shutil.copy(path, ADDON_INSTALL_PATH)
            elif os.path.isdir(path):
                shutil.copytree(path, ADDON_INSTALL_PATH)
            final_path = os.path.join(ADDON_INSTALL_PATH, os.path.basename(path))

            data.append({
                "path": final_path,
                "info": mod.pv_info,
                "activated": True,
                "link": False,
            })

        else:
            print("Not installing because \"pv_info\" is missing.")

    elif args.cmd == "link":
        path = os.path.realpath(input("Enter file or directory path: "))
        mod = import_file(path)
        if hasattr(mod, "pv_info"):
            data.append({
                "path": path,
                "info": mod.pv_info,
                "activated": True,
                "link": True,
            })
        else:
            print("Not installing because \"pv_info\" is missing.")

    with open(ADDON_CONFIG_PATH, "w") as file:
        json.dump(data, file, indent=4)


def main():
    parser = argparse.ArgumentParser(description="Piano performance visualizer.")
    parser.add_argument("-S", "--safe", action="store_true", help="Safe mode (protects accidental SIGINT or KeyboardInterrupt)")
    parser.add_argument("-V", "--version", action="store_true", help="Show the version of the program.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Display more information to stdout.")
    parser.add_argument("-T", "--test", action="store_true", help="Test API and modules. No GUI window will open.")
    parser.add_argument("cmd", nargs="?", choices=["addons"])
    parser.add_argument("opts", nargs="*")
    args = parser.parse_args()

    init(args.verbose)

    if args.version:
        print(f"Piano Video v{VERSION}  Copyright (C) 2021  Patrick Huang")
        print("Licensed under GNU General Public License v3")
        print("This program comes with ABSOLUTELY NO WARRANTY.")
        print("This is free software, and you are welcome to redistribute it under certain conditions.")
        print("Running in Python " + ".".join(map(str, sys.version_info[:3])))
        return

    if args.cmd is not None:
        if args.cmd == "addons":
            manage_addons(args.opts)
        return

    with SIGINT_Handler(args.safe, args.verbose):
        run(args)


main()
