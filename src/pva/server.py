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

import os
import argparse
import base64
import json
from hashlib import sha256, sha384, sha512
from http.server import HTTPServer, BaseHTTPRequestHandler

PARENT = os.path.dirname(os.path.realpath(__file__))


class Data:
    @staticmethod
    def read(path: str, mode: str = "r"):
        with open(os.path.join(PARENT, path), mode) as file:
            return file.read()

    @staticmethod
    def write(path: str, data, mode: str = "w"):
        with open(os.path.join(PARENT, path), mode) as file:
            file.write(data)

    @staticmethod
    def isfile(path: str):
        return os.path.isfile(os.path.join(PARENT, path))

    @staticmethod
    def isdir(path: str):
        return os.path.isdir(os.path.join(PARENT, path))

    @staticmethod
    def makedirs(path: str):
        os.makedirs(os.path.join(PARENT, path))

    @staticmethod
    def load(path: str):
        return json.loads(Data.read(path))

    @staticmethod
    def dump(path: str, obj):
        Data.write(path, json.dumps(obj))


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        pass


def secure_hash(data: bytes) -> bytes:
    """
    A function that calls SHA2 algorithms many times.
    This makes it harder to brute force reverse hashes,
    as each hash will take longer.

    Currently, one CPU core can manage 1000 hashes per second.
    """
    for _ in range(1000):
        data = sha384(data).digest()
    for _ in range(1000):
        data = sha256(data).digest()
    for _ in range(1000):
        data = sha512(data).digest()
    return data


def main():
    parser = argparse.ArgumentParser(description="Server of Piano Video add-on system.")
    parser.add_argument("--ip", help="IP address to bind to", default="0.0.0.0")
    parser.add_argument("--port", help="Port to bind to", type=int, default=5555)
    args = parser.parse_args()

    print(f"Serving on IP {args.ip} and PORT {args.port}")
    server = HTTPServer((args.ip, args.port), Handler)
    server.serve_forever()


main()
