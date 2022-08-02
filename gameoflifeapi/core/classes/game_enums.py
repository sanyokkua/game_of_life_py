"""Definition of Enums used by Game."""
import enum


class GameLifeCellState(enum.Enum):
    """Define two possible states of the CELL."""

    ALIVE = 0
    DEAD = 1
