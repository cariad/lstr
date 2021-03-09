from typing import Any, List

from lstr.lock import Lock


class lstr:
    """
    A partially lockable string.

    Arguments:
        value: String value.
        locks: Ranges to lock. Further locks can be added via `lock()`.
    """

    def __init__(self, value: str, locks: List[Lock] = []) -> None:
        self.value = value
        self.locks = locks

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, lstr):
            return self.value == other.value and self.locks == other.locks
        if isinstance(other, str):
            return self.value == other
        other_type = type(other).__name__
        raise NotImplementedError(f"Cannot compare lstr with {other_type}.")

    def __len__(self) -> int:
        return len(self.value)

    def __str__(self) -> str:
        return self.value

    def can_write(self, index: int, length: int) -> bool:
        """
        Calculates whether or not the given range of this string can be
        overwritten.

        Arguments:
            index:  Start index.
            length: Length.

        Returns:
            `True` if the range can be overwritten, otherwise `False`.
        """
        if index < 0 or length < 0 or index + length > len(self.value):
            return False
        for lock in self.locks:
            if lock.intersects(index=index, length=length):
                return False
        return True

    def lock(self, index: int, length: int) -> None:
        """
        Locks a range of the string.

        Arguments:
            index:  Start index.
            length: Length.
        """
        self.locks.append(Lock(index=index, length=length))

    def write(self, value: str, index: int, length: int) -> bool:
        """
        Attempts to overwrite a given range with a new value.

        Arguments:
            value:  String.
            index:  Start index.
            length: Length.

        Returns:
            `True` if the overwrite was permitted, otherwise `False`.
        """
        if not self.can_write(index=index, length=length):
            return False
        self.value = self.value[0:index] + value + self.value[index + length :]
        if distance := len(value) - length:
            self.shift_locks(index=index, distance=distance)
        return True

    def shift_locks(self, index: int, distance: int) -> None:
        """
        Shifts all the locks affected by a change at a given index by a given
        distance.

        Arguments:
            index:    Affected index.
            distance: Distance. Negative distances shift to the left.
        """
        for lock in [lock for lock in self.locks if lock.index >= index]:
            lock.index += distance
