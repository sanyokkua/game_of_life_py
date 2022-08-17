"""Definitions of the Game Exceptions."""
import logging

log: logging.Logger = logging.getLogger(__name__)


class CoordinateValueException(Exception):
    """Defines exception raised on incorrect coordinates."""

    def __init__(self, message: str) -> None:
        """Initialize exception.

        Args:
            message (str): Error message
        """
        Exception.__init__(self, message)
        log.debug('CoordinateValueException.__init__')


class NeighboursNumberException(AttributeError):
    """Defines exception raised on incorrect neighbour number."""

    def __init__(self, message: str) -> None:
        """Initialize exception.

        Args:
            message (str): Error message
        """
        AttributeError.__init__(self, message)
        log.debug('NeighboursNumberException.__init__')


class GameFieldSizeException(Exception):
    """Defines exception raised on incorrect sizes."""

    def __init__(self, message: str) -> None:
        """Initialize exception.

        Args:
            message (str): Error message
        """
        Exception.__init__(self, message)
        log.debug('GameFieldSizeException.__init__')


class GenerationValueException(Exception):
    """Defines exception raised on incorrect generation value."""

    def __init__(self, message: str) -> None:
        """Initialize exception.

        Args:
            message (str): Error message
        """
        Exception.__init__(self, message)
        log.debug('GenerationValueException.__init__')


class GameFieldValueException(Exception):
    """Defines exception raised on incorrect GameField value."""

    def __init__(self, message: str) -> None:
        """Initialize exception.

        Args:
            message (str): Error message
        """
        Exception.__init__(self, message)
        log.debug('GameFieldValueException.__init__')
