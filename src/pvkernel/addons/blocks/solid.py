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

from pvkernel import Video
from pvkernel import draw


def draw_block_solid(video: Video, rect):
    props = video.props.blocks_solid
    rounding = props.rounding

    if props.glow:
        new_rect = (rect[0]-2, rect[1]-2, rect[2]+4, rect[3]+4)
        draw.rect(video.render_img, props.glow_color, new_rect, border_radius=rounding)
    draw.rect(video.render_img, props.color, rect, border_radius=rounding)
    if props.border > 0:
        draw.rect(video.render_img, props.border_color, rect, border=props.border, border_radius=rounding)
