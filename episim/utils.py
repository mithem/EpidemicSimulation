import fcntl
import math
import struct
import termios
from typing import Union

import numpy as np


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
    cumsum = np.cumsum(np.insert(x, 0, 0))
    return list((cumsum[N:] - cumsum[:-N]) / float(N))


def terminal_size():
    th, tw, hp, wp = struct.unpack('HHHH',
                                   fcntl.ioctl(0, termios.TIOCGWINSZ,
                                               struct.pack('HHHH', 0, 0, 0, 0)))
    return tw, th


def get_custom_properties(config, person):
    ic = person.infection_chance
    if ic == None:
        ic = config.infection_chance

    id = person.infection_distance
    if id == None:
        id = config.infection_distance

    rm = person.random_movement
    if rm == None:
        rm = config.random_movement

    return ic, id, rm


def get_person_types_amount(a: Union[str, list]):
    try:
        a = a.split(":")
    except AttributeError:
        pass
    for i in a:
        a[a.index(i)] = int(i)
    if np.sum(a) != 100:
        raise ValueError("person_types_amount needs to sum up to 100 (%)")
    return a


def sort_by_class_name(l):
    di = {}  # kinda weird but i'm too tired to think of something better
    for i in l:
        di[i.__name__] = i
    cls_names = list(di.keys()).copy()
    cls_names.sort()
    return [di[i] for i in cls_names]


def fill_person_types_to(person_types: list, value: list, total_length: int):
    result = []
    for pt in person_types:
        decimal_portion = (value[person_types.index(pt)] / 100.0)
        fill_value = int(round(
            decimal_portion * total_length, 0))
        for counter in range(fill_value):
            result.append(pt)
    return result


def get_percent_of_world(value: Union[int, str], capacity):
    try:
        return int(value)
    except ValueError:
        if type(value) == str:
            if value[-1] == "%":
                return int(round(int(value[:-1]) * 0.01 * capacity, 0))
            else:
                raise ValueError("Unable to parse int")
