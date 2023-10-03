from pytest import approx
from streetlevel import geo


def test_wgs84_to_tile_coord():
    expected = (69172, 42368)
    actual = geo.wgs84_to_tile_coord(53.539043721545404, 9.98702908360777, 17)
    assert expected == actual


def tile_coord_to_wgs84():
    expected = (53.54030739150021, 9.986572265625)
    actual = geo.tile_coord_to_wgs84(69172, 42368, 17)
    assert expected[0] == approx(actual[0], 0.00001)
    assert expected[1] == approx(actual[1], 0.00001)
