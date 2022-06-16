import pytest


def test_sanity():
    with pytest.raises(Exception):
        raise Exception("POW!")
