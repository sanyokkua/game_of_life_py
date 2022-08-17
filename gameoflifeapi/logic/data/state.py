"""Definition of the Game Field Cell State."""
import enum
import logging

log: logging.Logger = logging.getLogger(__name__)


class CellState(enum.Enum):
    """Represent State of the field."""

    DEAD: int = 0
    ALIVE: int = 1

    def __repr__(self) -> str:
        """Return name of the enum.

        Returns:
            str: Name
        """
        log.debug('CellState.__repr__: %s', self.name)
        return self.name
