"""Definition of Enums used by Game."""
import enum


class GameLifeCellState(enum.Enum):
    """Define two possible states of the CELL."""

    ALIVE = 0
    DEAD = 1

    def __repr__(self) -> str:
        """Override representation of the enum.

        Returns:
            str: Enum Item Name
        """
        return f'{self.name}'
