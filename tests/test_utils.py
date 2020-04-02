from episimlib.utils import coordinate_distance, get_neighbor_coords


def test_coordinate_distance():
    d = coordinate_distance((0, 0), (1, 1))
    assert d > 1.4 and d < 1.5


def test_get_neighbor_coords():
    c = (0, 0)
    result = get_neighbor_coords(c, 3, 100)
    print(result)
    expected = [(0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
    for c in expected:
        assert c in result
