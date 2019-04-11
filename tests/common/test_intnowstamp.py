import time 

import pytest

from source.common import inttimestamp


def test_inttimestamp():
    assert inttimestamp.intnowstamp() == pytest.approx(int(time.time()), 2)