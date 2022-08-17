"""Definition of the Game Field Cell Object.

Raises:
    CoordinateValueException: On incorrect coordinates passed
    AttributeError: On incorrect values assigned
    NeighboursNumberException: On incorrect values assigned
Returns:
    _type_: Field Cell Implementation
"""

from gameoflifeapi.logic.data.state import CellState
from gameoflifeapi.logic.exceptions import (CoordinateValueException,
                                            NeighboursNumberException)


class Cell:
    """Represent Field Cell implementation.

    Raises:
        CoordinateValueException: On incorrect coordinates passed
        AttributeError: On incorrect values assigned
        NeighboursNumberException: On incorrect values assigned
    """

    def __init__(self, row: int, column: int,
                 state: CellState = CellState.DEAD) -> None:
        """Initialize Cell Object.

        Args:
            row (int): ROW coordinate
            column (int): COLUMN coordinate
            state (FieldState, optional): Cell State.
                            Defaults to FieldState.DEAD.
        """
        self._validate_coordinate(row)
        self._validate_coordinate(column)
        self._row: int = row
        self._column: int = column
        self._state: CellState = state
        self._neighbours: int = 0

    def _validate_coordinate(self, value: int) -> None:
        """Validate value.

        Helper method for validation coordinates.

        Args:
            value (int): coordinate value

        Raises:
            CoordinateValueException: On incorrect value
        """
        if value < 0:
            raise CoordinateValueException(
                f'Passed coordinate is not correct, {value}')

    @property
    def row(self) -> int:
        """ROW property.

        Returns:
            int: row value of the cell
        """
        return self._row

    @property
    def column(self) -> int:
        """COLUMN property.

        Returns:
            int: column value of the cell
        """
        return self._column

    @property
    def state(self) -> CellState:
        """STATE property.

        Returns:
            int: state value of the cell
        """
        return self._state

    @state.setter
    def state(self, value: CellState) -> None:
        """Setter for property STATE.

        Args:
            value (FieldState): Value of the state

        Raises:
            AttributeError: If state is not supported or
                            value is not correct
        """
        if value not in [CellState.DEAD, CellState.ALIVE]:
            raise AttributeError(f'Passed value is not allowed, {value}')
        self._state = value

    @property
    def neighbours(self) -> int:
        """NEIGHBOUR property.

        Returns:
            int: Number of neighbours
        """
        return self._neighbours

    @neighbours.setter
    def neighbours(self, value: int) -> None:
        """Setter for NEIGHBOUR property.

        Args:
            value (int): number of ALIVE neighbours

        Raises:
            NeighboursNumberException: On incorrect number of neighbours
        """
        if value is None or not 0 <= value <= 8:
            raise NeighboursNumberException('Number is not in 0..8')
        self._neighbours = value
