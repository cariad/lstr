from enum import Enum


class Amount(Enum):
    """
    Vaguely but truthfully describes an amount.
    """

    NONE = 0
    SOME = 1
    ALL = 2
