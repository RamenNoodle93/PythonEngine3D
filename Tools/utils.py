from Tools.constants import *
import numpy as np

def bothPointsHidden(visible, edge):
        if not visible[edge[0]] and not visible[edge[1]]:
            return True
        return False

def clip_line(x1, y1, x2, y2, xmin = 0, ymin = 0, xmax = width, ymax = height):
    # Compute the region codes for the two endpoints of the line
    code1 = compute_region_code(x1, y1, xmin, ymin, xmax, ymax)
    code2 = compute_region_code(x2, y2, xmin, ymin, xmax, ymax)

    # Check if the line is completely inside the viewing region
    if code1 == 0 and code2 == 0:
        return [[x1, y1], [x2, y2]]

    # Check if the line is completely outside the viewing region
    if (code1 & code2) != 0:
        return None

    # Clip the line against each edge of the viewing region
    for edge, code in zip(['left', 'right', 'bottom', 'top'], [1, 2, 4, 8]):
        if code1 & code:
            x1, y1 = clip_point(x1, y1, x2, y2, edge, xmin, ymin, xmax, ymax)
            code1 = compute_region_code(x1, y1, xmin, ymin, xmax, ymax)
        elif code2 & code:
            x2, y2 = clip_point(x1, y1, x2, y2, edge, xmin, ymin, xmax, ymax)
            code2 = compute_region_code(x2, y2, xmin, ymin, xmax, ymax)

    return [[x1, y1], [x2, y2]]

def compute_region_code(x, y, xmin, ymin, xmax, ymax):
    code = 0
    if x < xmin:
        code |= 1
    elif x > xmax:
        code |= 2
    if y < ymin:
        code |= 4
    elif y > ymax:
        code |= 8
    return code

def clip_point(x1, y1, x2, y2, edge, xmin, ymin, xmax, ymax):
    if edge == 'left':
        x = xmin
        y = y1 + (y2 - y1) * (xmin - x1) / (x2 - x1)
    elif edge == 'right':
        x = xmax
        y = y1 + (y2 - y1) * (xmax - x1) / (x2 - x1)
    elif edge == 'bottom':
        x = x1 + (x2 - x1) * (ymin - y1) / (y2 - y1)
        y = ymin
    elif edge == 'top':
        x = x1 + (x2 - x1) * (ymax - y1) / (y2 - y1)
        y = ymax
    return x, y