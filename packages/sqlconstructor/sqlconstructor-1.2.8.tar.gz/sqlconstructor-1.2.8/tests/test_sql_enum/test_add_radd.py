import pytest
from sqlconstructor import SqlEnum


@pytest.mark.SqlEnum
def test_add():
    assert SqlEnum('a', 'b') + 'c' == "(\n  a,\n  b\n)c"


@pytest.mark.SqlEnum
def test_add_inline():
    assert SqlEnum('a', 'b').inline() + 'c' == "a, bc"


@pytest.mark.SqlEnum
def test_radd():
    assert 'c' + SqlEnum('a', 'b') == "c(\n  a,\n  b\n)"


@pytest.mark.SqlEnum
def test_radd_inline():
    assert 'c' + SqlEnum('a', 'b').inline() == "ca, b"
