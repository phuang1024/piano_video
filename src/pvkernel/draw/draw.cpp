//
//  Piano Video
//  A free piano visualizer.
//  Copyright Patrick Huang 2021
//
//  This program is free software: you can redistribute it and/or modify
//  it under the terms of the GNU General Public License as published by
//  the Free Software Foundation, either version 3 of the License, or
//  (at your option) any later version.
//
//  This program is distributed in the hope that it will be useful,
//  but WITHOUT ANY WARRANTY; without even the implied warranty of
//  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//  GNU General Public License for more details.
//
//  You should have received a copy of the GNU General Public License
//  along with this program.  If not, see <https://www.gnu.org/licenses/>.
//

#include <algorithm>
#include "../utils.hpp"

using std::min;
using std::max;


extern "C" void draw_line(UCH* img, const int width, const int height, CD x1, CD y1, CD x2, CD y2,
        CD thick, CD r, CD g, CD b, CD a) {
    /*
    TODO buggy
    Draws a line.

    :param img: Image.
    :param width: Image width.
    :param height: Image height.
    :param x1, x2, y1, y2: Line points.
    :param thick: Line thickness.
    :param r, g, b, a: R, G, B, A values.
    */
    const int xmin = max((int)(min(x1, x2)-thick-1), 0);
    const int xmax = min((int)(max(x1, x2)+thick+1), (int)width-1);
    const int ymin = max((int)(min(y1, y2)-thick-1), 0);
    const int ymax = min((int)(max(y1, y2)+thick+1), (int)height-1);

    CD dx = fabs(x1-x2), dy = fabs(y1-y2);
    CD m = (dy == 0) ? 1e9 : dx/dy;
    CD y_int = y1 - m*x1;
    CD A = -m, B = 1, C = -y_int;

    CD afac = a / 255;
    const UCH c1[3] = {(UCH)r, (UCH)g, (UCH)b};

    for (int x = xmin; x <= xmax; x++) {
        for (int y = ymin; y <= ymax; y++) {
            CD dist = fabs(A*x + B*y + C) / pythag(A, B);
            CD fac = dbounds(thick-dist+1);

            UCH c2[3], color[3];
            img_getc(img, width, x, y, c2);
            img_mix(color, c2, c1, fac*afac);
            img_setc(img, width, x, y, color[0], color[1], color[2]);
        }
    }
}

extern "C" void draw_circle(UCH* img, const int width, const int height, CD cx, CD cy,
        CD rad, CD border, CD r, CD g, CD b, CD a) {
    /*
    Draws a circle.

    :param img: Image.
    :param width: Image width.
    :param height: Image height.
    :param cx: Center X.
    :param cy: Center Y.
    :param rad: Radius.
    :param border: Border thickness. Set to 0 for filled.
    :param r, g, b, a: R, G, B, A values.
    */
    const int xmin = max((int)(cx-rad-1), 0);
    const int xmax = min((int)(cx+rad+1), (int)width-1);
    const int ymin = max((int)(cy-rad-1), 0);
    const int ymax = min((int)(cy+rad+1), (int)height-1);

    CD afac = a / 255;
    CD out_thres = rad;
    CD in_thres = (border == 0 ? 0 : (rad-border));
    const UCH c1[3] = {(UCH)r, (UCH)g, (UCH)b};

    for (int x = xmin; x <= xmax; x++) {
        for (int y = ymin; y <= ymax; y++) {
            CD dist = pythag(x-cx, y-cy);
            CD out_fac = dbounds(out_thres-dist+1);
            CD in_fac = dbounds(dist-in_thres+1);

            UCH c2[3], color[3];
            img_getc(img, width, x, y, c2);
            img_mix(color, c2, c1, out_fac*in_fac*afac);
            img_setc(img, width, x, y, color[0], color[1], color[2]);
        }
    }
}

extern "C" void draw_rect(UCH* img, const int width, const int height, CD dx, CD dy, CD dw, CD dh,
        CD border, CD border_rad, CD tl_rad, CD tr_rad, CD bl_rad, CD br_rad, CD r, CD g, CD b, CD a) {
    /*
    Draws a rectangle.

    :param img: Image.
    :param width: Image width.
    :param height: Image height.
    :param dx: Top left X.
    :param dy: Top left Y.
    :param dw: Width.
    :param dh: Height.
    :param border: Border thickness. Set to 0 for filled.
    :param border_rad: Radius of corner rounding.
    :param tl_rad: Top left corner radius.
    :param tr_rad: Top right corner radius.
    :param bl_rad: Bottom left corner radius.
    :param br_rad: Bottom right corner radius.
    */
    CD radii[4] = {
        (tl_rad < 0) ? border_rad : tl_rad,
        (tr_rad < 0) ? border_rad : tr_rad,
        (br_rad < 0) ? border_rad : br_rad,
        (bl_rad < 0) ? border_rad : bl_rad,
    };
    double thresholds[4];
    for (int i = 0; i < 4; i++)
        thresholds[i] = ((border == 0) ? 0 : (radii[i]-border));

    CD afac = a / 255;
    const UCH c1[3] = {(UCH)r, (UCH)g, (UCH)b};

    const int xmin = max((int)(dx-1), 0);
    const int xmax = min((int)(dx+dw+1), (int)width);
    const int ymin = max((int)(dy-1), 0);
    const int ymax = min((int)(dy+dh+1), (int)height);
    for (int x = xmin; x <= xmax; x++) {
        for (int y = ymin; y <= ymax; y++) {
            bool is_corner = false;
            UCH corner_no;
            double corner_pos[2];
            if (x < dx+radii[0] && y < dy+radii[0]) {
                is_corner = true;
                corner_no = 0;
                corner_pos[0] = dx+radii[0];
                corner_pos[1] = dy+radii[0];
            } else if (x > dx+dw-radii[1] && y < dy+radii[1]) {
                is_corner = true;
                corner_no = 1;
                corner_pos[0] = dx+dw-radii[1];
                corner_pos[1] = dy+radii[1];
            } else if (x > dx+dw-radii[2] && y > dy+dh-radii[2]) {
                is_corner = true;
                corner_no = 2;
                corner_pos[0] = dx+dw-radii[2];
                corner_pos[1] = dy+dh-radii[2];
            } else if (x < dx+radii[3] && y > dy+dh-radii[3]) {
                is_corner = true;
                corner_no = 3;
                corner_pos[0] = dx+radii[3];
                corner_pos[1] = dy+dh-radii[3];
            }

            double final_fac;
            if (is_corner) {
                CD dist = pythag(x-corner_pos[0], y-corner_pos[1]);
                CD out_fac = dbounds(radii[corner_no]-dist+1);
                CD in_fac = dbounds(dist-thresholds[corner_no]+1);
                final_fac = out_fac*in_fac*afac;
            } else {
                CD out_fac = dbounds(x-dx+1) * dbounds(dx+dw-x+1) * dbounds(y-dy+1) * dbounds(dy+dh-y+1);
                CD in_fac = (border == 0) ? 1 :
                    dbounds(dx+border-x+1) + dbounds(x-(dx+dw-border)+1) + dbounds(dy+border-y+1) + dbounds(y-(dy+dh-border)+1);
                final_fac = out_fac*in_fac*afac;
            }

            UCH c2[3], color[3];
            img_getc(img, width, x, y, c2);
            img_mix(color, c2, c1, final_fac);
            img_setc(img, width, x, y, color[0], color[1], color[2]);
        }
    }
}
