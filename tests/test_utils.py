from episim.utils import *


def test_coordinate_distance():
    d = coordinate_distance((0, 0), (1, 1))
    assert d > 1.4 and d < 1.5


def test_get_neighbor_coords():
    c = (0, 0)
    result = get_neighbor_coords(c, 3, 100)
    print(result)
    expected = [(0, 1), (0, 2), (0, 3),
                (1, 0), (1, 1), (1, 2), (1, 3),
                (2, 0), (2, 1), (2, 2), (2, 3),
                (3, 0), (3, 1), (3, 2), (3, 3)]
    for c in expected:
        assert c in result
    assert len(result) == len(expected)


def test_get_neighbor_coords_2():
    c = (3, 3)
    result = get_neighbor_coords(c, 3, 100)
    print(result)
    expected = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6),
                (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6),
                (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6),
                (3, 0), (3, 1), (3, 2), (3, 4), (3, 5), (3, 6),
                (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6),
                (5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6),
                (6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6)
                ]
    for i in expected:
        assert i in result
    assert len(result) == len(expected)
