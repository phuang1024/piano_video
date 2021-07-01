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
from http.server import HTTPServer, BaseHTTPRequestHandler


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        pass


def main():
    parser = argparse.ArgumentParser("Server of Piano Video add-on system.")
    parser.add_argument("--ip", help="IP address to bind to", default="0.0.0.0")
    parser.add_argument("--port", help="Port to bind to", type=int, default=5555)
    args = parser.parse_args()

    print(f"Serving on IP {args.ip} and PORT {args.port}")
    server = HTTPServer((args.ip, args.port), Handler)
    server.serve_forever()


main()
