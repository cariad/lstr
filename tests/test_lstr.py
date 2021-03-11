from logging import Logger
from typing import List, Union

from pytest import mark, raises

from lstr import Amount, Lock, lstr


@mark.parametrize(
    "value, index, length, expect",
    [
        (lstr("abc"), -1, 1, False),
        (lstr("abc"), 0, -1, False),
        (lstr("abc"), 0, 0, True),
        (lstr("abc"), 0, 1, True),
        (lstr("abc"), 1, 1, True),
        (lstr("abc"), 2, 1, True),
        (lstr("abc"), 3, 1, False),
        (lstr("abc", locks=[Lock(1, 1)]), 0, 1, True),
        (lstr("abc", locks=[Lock(1, 1)]), 1, 1, False),
        (lstr("abc", locks=[Lock(1, 1)]), 2, 1, True),
        (lstr("abcdef", locks=[Lock(2, 2)]), 0, 2, True),
        (lstr("abcdef", locks=[Lock(2, 2)]), 1, 2, False),
        (lstr("abcdef", locks=[Lock(2, 2)]), 2, 2, False),
        (lstr("abcdef", locks=[Lock(2, 2)]), 3, 2, False),
        (lstr("abcdef", locks=[Lock(2, 2)]), 4, 2, True),
    ],
)
def test_can_write(value: lstr, index: int, length: int, expect: bool) -> None:
    assert value.can_write(index=index, length=length) == expect


@mark.parametrize(
    "x, y, expect",
    [
        (lstr("abc"), lstr("abc"), True),
        (lstr("abc"), lstr("abcd"), False),
        (lstr("abc"), lstr("abc", locks=[Lock(index=0, length=1)]), False),
        (lstr("abc"), "abc", True),
        (lstr("abc"), "abcd", False),
    ],
)
def test_eq(x: lstr, y: Union[lstr, str], expect: bool) -> None:
    assert (x == y) is expect


def test_eq__not_implemented() -> None:
    with raises(NotImplementedError) as ex:
        lstr("abc") == 0
    assert str(ex.value) == "Cannot compare lstr with int."


@mark.parametrize(
    "value, expect",
    [
        (lstr(""), 0),
        (lstr("a"), 1),
        (lstr("ab"), 2),
        (lstr("abc"), 3),
    ],
)
def test_len(value: lstr, expect: int) -> None:
    assert len(value) == expect


def test_lock() -> None:
    ls = lstr("abcdef")
    assert ls.can_write(index=0, length=1)
    ls.lock(index=0, length=1)
    assert not ls.can_write(index=0, length=1)


@mark.parametrize(
    "index, length, value, expect, expect_locks",
    [
        # STR:   a b c d e f
        # INDEX: 0 1 2 3 4 5
        # LOCK:    X X   X X
        (-1, 1, "?", "abcdef", [Lock(1, 2), Lock(4, 2)]),
        (0, -1, "?", "abcdef", [Lock(1, 2), Lock(4, 2)]),
        # Index: 0
        (0, 0, "?", "?abcdef", [Lock(2, 2), Lock(5, 2)]),
        (0, 1, "?", "?bcdef", [Lock(1, 2), Lock(4, 2)]),
        (0, 1, "??", "??bcdef", [Lock(2, 2), Lock(5, 2)]),
        # Index: 1
        (1, 0, "?", "a?bcdef", [Lock(2, 2), Lock(5, 2)]),
        (1, 1, "?", "abcdef", [Lock(1, 2), Lock(4, 2)]),
        (1, 1, "??", "abcdef", [Lock(1, 2), Lock(4, 2)]),
        # Index: 2
        (2, 0, "?", "abcdef", [Lock(1, 2), Lock(4, 2)]),
        (2, 1, "?", "abcdef", [Lock(1, 2), Lock(4, 2)]),
        (2, 1, "??", "abcdef", [Lock(1, 2), Lock(4, 2)]),
        # Index: 3
        (3, 0, "?", "abc?def", [Lock(1, 2), Lock(5, 2)]),
        (3, 1, "?", "abc?ef", [Lock(1, 2), Lock(4, 2)]),
        (3, 1, "??", "abc??ef", [Lock(1, 2), Lock(5, 2)]),
        # Index: 4
        (4, 0, "?", "abcd?ef", [Lock(1, 2), Lock(5, 2)]),
        (4, 1, "?", "abcdef", [Lock(1, 2), Lock(4, 2)]),
        (4, 1, "??", "abcdef", [Lock(1, 2), Lock(4, 2)]),
        # Index: 5
        (5, 0, "?", "abcdef", [Lock(1, 2), Lock(4, 2)]),
        (5, 1, "?", "abcdef", [Lock(1, 2), Lock(4, 2)]),
        (5, 1, "??", "abcdef", [Lock(1, 2), Lock(4, 2)]),
        # Index: 6
        (6, 0, "?", "abcdef?", [Lock(1, 2), Lock(4, 2)]),
        (6, 1, "?", "abcdef", [Lock(1, 2), Lock(4, 2)]),
        (6, 1, "??", "abcdef", [Lock(1, 2), Lock(4, 2)]),
    ],
)
def test_write(
    index: int,
    length: int,
    value: str,
    expect: str,
    expect_locks: List[Lock],
) -> None:
    ls = lstr("abcdef", locks=[Lock(1, 2), Lock(4, 2)])
    ls.write(index=index, length=length, value=value)
    assert str(ls) == expect
    assert ls.locks == expect_locks


def test_repr() -> None:
    value = lstr(
        "Hello, world!",
        locks=[
            Lock(index=0, length=5),
            Lock(index=12, length=1),
        ],
    )
    assert repr(value) == (
        ""
        + "  0  1  2  3  4  5  6  7  8  9 10 11 12\n"
        + "  H  e  l  l  o  ,     w  o  r  l  d  !\n"
        + "  ^  ^  ^  ^  ^                       ^"
    )


@mark.parametrize(
    "index, distance, expect",
    [
        (0, 0, [Lock(1, 2), Lock(4, 2)]),
        (0, 1, [Lock(2, 2), Lock(5, 2)]),
        (0, -1, [Lock(0, 2), Lock(3, 2)]),
        (3, 0, [Lock(1, 2), Lock(4, 2)]),
        (3, 1, [Lock(1, 2), Lock(5, 2)]),
        (3, -1, [Lock(1, 2), Lock(3, 2)]),
        (6, 0, [Lock(1, 2), Lock(4, 2)]),
        (6, 1, [Lock(1, 2), Lock(4, 2)]),
        (6, -1, [Lock(1, 2), Lock(4, 2)]),
    ],
)
def test_shift_locks(index: int, distance: int, expect: List[Lock]) -> None:
    ls = lstr("abcdef", locks=[Lock(1, 2), Lock(4, 2)])
    ls.shift_locks(index=index, distance=distance)
    assert ls.locks == expect


@mark.parametrize(
    "value, expect_amount, expect",
    [
        (
            lstr("first a then b please"),
            Amount.NOOP,
            lstr("first a then b please"),
        ),
        (
            lstr("first `a` then `b` please", [Lock(index=6, length=12)]),
            Amount.NONE,
            lstr("first `a` then `b` please", [Lock(index=6, length=12)]),
        ),
        (
            lstr("first `a` then `b` please", [Lock(index=6, length=3)]),
            Amount.SOME,
            lstr("first `a` then b please", [Lock(index=6, length=3)]),
        ),
        (
            lstr("first `a` then `b` please", [Lock(index=15, length=3)]),
            Amount.SOME,
            lstr("first a then `b` please", [Lock(index=13, length=3)]),
        ),
        (
            lstr("first `a` then `b` please", [Lock(0, 5), Lock(10, 4), Lock(19, 6)]),
            Amount.ALL,
            lstr("first a then b please", [Lock(0, 5), Lock(8, 4), Lock(15, 6)]),
        ),
    ],
)
def test_sub(value: lstr, expect_amount: Amount, expect: lstr, logger: Logger) -> None:
    assert value.sub(r"`([^`]+)`", r"\g<1>") == expect_amount
    assert value == expect
