import pytest

from rand_useragent import randua


def test_invalid_args():
    with pytest.raises(AssertionError):
        randua(browsers=600)
        randua(os=20)
        randua(min_percent="2.5")
        randua(fallback=True)


def test_fallback():
    assert (
        randua(browsers=["non existing"])
        == "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0"
    )
    assert (
        randua(os=["non existing"])
        == "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0"
    )
    assert (
        randua(min_percent=100.2)
        == "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0"
    )
    assert (
        randua(browsers=["non existing"], fallback="user defined fallback")
        == "user defined fallback"
    )
