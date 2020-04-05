import fcntl
import math
import struct
import termios

import numpy


def coordinate_distance(a: tuple, b: tuple):
    dx = abs(a[0] - b[0])
    dy = abs(a[1] - b[1])
    return math.sqrt((dx**2) + (dy**2))  # Pythagorean theorem


def get_neighbor_coords(c: tuple, d: int, boundary_length: int):
    """return list of neighbors coordinates from `c`, max distance `d` away. `boundary_length`specifies how big the coordinate system is. Implies it starts at (0, 0)."""
    result = []
    for x in range(int(round(0-d, 0)), int(math.ceil(d + 1))):
        a_x = c[0] + x  # absolute x coord
        for y in range(int(round(0 - d, 0)), int(math.ceil(d + 1))):
            a_y = c[1] + y  # absolute y coord
            if a_x >= 0 and a_x <= boundary_length:  # within x boundaries
                if a_y >= 0 and a_y <= boundary_length:  # within y boundaries
                    if x != 0 or y != 0:  # not the same coordinate
                        result.append((a_x, a_y))
    return result


def moving_average(x, N):
    cumsum = numpy.cumsum(numpy.insert(x, 0, 0))
    return list((cumsum[N:] - cumsum[:-N]) / float(N))


def terminal_size():
    th, tw, hp, wp = struct.unpack('HHHH',
                                   fcntl.ioctl(0, termios.TIOCGWINSZ,
                                               struct.pack('HHHH', 0, 0, 0, 0)))
    return tw, th
