from pytest import mark, raises

from lstr import Lock


def test_eq__false() -> None:
    assert Lock(index=0, length=1) != Lock(index=1, length=1)


def test_eq__not_implemented() -> None:
    with raises(NotImplementedError) as ex:
        Lock(index=0, length=1) != "foo"
    assert str(ex.value) == "Cannot compare Lock with str."


def test_eq__true() -> None:
    assert Lock(index=0, length=1) == Lock(index=0, length=1)


def test_repr() -> None:
    assert repr(Lock(index=0, length=1)) == "Lock: index=0, length=1"


@mark.parametrize(
    "lock, index, length, expect",
    [
        (Lock(index=3, length=2), 0, 3, False),
        (Lock(index=3, length=2), 1, 3, True),
        (Lock(index=3, length=2), 2, 3, True),
        (Lock(index=3, length=2), 3, 3, True),
        (Lock(index=3, length=2), 4, 3, True),
        (Lock(index=3, length=2), 5, 3, False),
        (Lock(index=3, length=2), 6, 3, False),
        (Lock(index=3, length=2), 7, 3, False),
    ],
)
def test_intersects(lock: Lock, index: int, length: int, expect: bool) -> None:
    assert lock.intersects(index=index, length=length) == expect, index


@mark.parametrize(
    "lock, index, expect",
    [
        (Lock(index=3, length=2), 0, True),
        (Lock(index=3, length=2), 1, True),
        (Lock(index=3, length=2), 2, True),
        (Lock(index=3, length=2), 3, False),
        (Lock(index=3, length=2), 4, False),
        (Lock(index=3, length=2), 5, False),
        (Lock(index=3, length=2), 6, False),
    ],
)
def test_is_earlier(lock: Lock, index: int, expect: bool) -> None:
    assert lock.is_earlier(index) == expect


@mark.parametrize(
    "lock, index, expect",
    [
        (Lock(index=3, length=2), 0, False),
        (Lock(index=3, length=2), 1, False),
        (Lock(index=3, length=2), 2, False),
        (Lock(index=3, length=2), 3, False),
        (Lock(index=3, length=2), 4, False),
        (Lock(index=3, length=2), 5, True),
        (Lock(index=3, length=2), 6, True),
        (Lock(index=3, length=2), 7, True),
    ],
)
def test_is_later(lock: Lock, index: int, expect: bool) -> None:
    assert lock.is_later(index) == expect, index
