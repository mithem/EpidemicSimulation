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


def test_sort_by_class_name():
    class A:
        a = 0

    class B:
        b = 1

    class C:
        c = 2
    result = sort_by_class_name([B, A, C])
    assert result[0] == A
    assert result[1] == B
    assert result[2] == C


def test_fill_person_types_to():
    result = fill_person_types_to(["A", "B"], [75, 25], 4)
    print(result)
    assert len(result) == 4
    assert result[0] == "A"
    assert result[1] == "A"
    assert result[2] == "A"
    assert result[3] == "B"


def test_get_percent_of_world():
    assert get_percent_of_world(100, 10000) == 100
    assert get_percent_of_world("10%", 10000) == 1000
    assert get_percent_of_world("99%", 100) == 99
    assert get_percent_of_world("99%", 10) == 10
    assert get_percent_of_world("50%", 1) == 0
    assert get_percent_of_world("51%", 1) == 1
