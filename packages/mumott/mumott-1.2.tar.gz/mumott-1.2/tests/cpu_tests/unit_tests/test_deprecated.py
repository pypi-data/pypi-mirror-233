import pytest
from mumott.core.deprecation_warning import deprecated


@deprecated('')
class Foo:
    def __init__(self, number):
        self.number = number

    @deprecated('')
    def bar(self):
        return self.number


@deprecated('abcd')
def foobar(number):
    return number


def test_class():
    with pytest.warns(DeprecationWarning, match='Class Foo'):
        f = Foo(5)
    assert f.number == 5


def test_method():
    f = Foo(5)
    with pytest.warns(DeprecationWarning, match='Function/Method bar'):
        assert f.bar() == 5


def test_function():
    with pytest.warns(DeprecationWarning, match='Function/Method foobar'):
        n = foobar(5)
    assert n == 5


def test_extra_string():
    with pytest.warns(DeprecationWarning, match='abcd'):
        n = foobar(5)
    assert n == 5
