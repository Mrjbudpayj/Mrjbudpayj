import math
import pytest
from canonicalization.jcs import jcs_canonicalize

@pytest.mark.parametrize("value,expected", [
    (333333333.33333329, b"333333333.3333333"),
    (1e30, b"1e+30"),
    (4.50, b"4.5"),
    (2e-3, b"0.002"),
    (1e-27, b"1e-27"),
    (-0.0, b"0"),
])
def test_rfc8785_number_vectors(value, expected):
    assert jcs_canonicalize(value) == expected


def test_unicode_key_ordering():
    # RFC 8785 orders object property names by UTF-16 code units.
    value = {"\ud834\udd1e": 1, "\ue000": 2}
    assert jcs_canonicalize(value) == b'{"\\ud834\\udd1e":1,"\\ue000":2}'


def test_nonfinite_rejected():
    for value in (math.nan, math.inf, -math.inf):
        with pytest.raises((ValueError, OverflowError)):
            jcs_canonicalize(value)
