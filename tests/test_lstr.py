from typing import List

from pytest import mark

from lstr import Lock, lstr


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
def test_can_replace(value: lstr, index: int, length: int, expect: bool) -> None:
    assert value.can_replace(index=index, length=length) == expect


def test_lock() -> None:
    ls = lstr("abcdef")
    assert ls.can_replace(index=0, length=1)
    ls.lock(index=0, length=1)
    assert not ls.can_replace(index=0, length=1)


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
def test_replace(
    index: int,
    length: int,
    value: str,
    expect: str,
    expect_locks: List[Lock],
) -> None:
    ls = lstr("abcdef", locks=[Lock(1, 2), Lock(4, 2)])
    ls.replace(index=index, length=length, value=value)
    assert str(ls) == expect
    assert ls.locks == expect_locks


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
