import sys

from wvutils.constants import IS_64_BIT


def test_is_64_bit():
    if sys.maxsize > 2**32:
        assert IS_64_BIT
    else:
        assert not IS_64_BIT
