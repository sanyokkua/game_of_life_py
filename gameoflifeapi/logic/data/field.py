"""Defines Game Field class."""
from gameoflifeapi.logic.data.cell import Cell
from gameoflifeapi.logic.exceptions import GameFieldSizeException


class Field:
    """Defines Game Field class."""

    def __init__(self, rows: int = 10, columns: int = 10) -> None:
        """Initialize Game Field Object.

        Args:
            rows (int, optional): Number of rows. Defaults to 10.
            columns (int, optional): Number of columns. Defaults to 10.
        Raises:
            GameFieldSizeException: On incorrect size passed
        """
        self._validate_game_field_size(rows)
        self._validate_game_field_size(columns)
        self._rows: int = rows
        self._columns: int = columns
        self._init_cells()

    def _validate_game_field_size(self, value: int) -> None:
        """Validate passed size.

        Args:
            value (int): Passed value

        Raises:
            GameFieldSizeException: On incorrect size passed
        """
        if value is None or value < 10:
            raise GameFieldSizeException('Minimal field size should be 10x10')

    def _init_cells(self) -> None:
        self._cells: dict[tuple[int, int], Cell] = {}
        rows: range = range(self._rows)
        cols: range = range(self._columns)
        for row in rows:
            for col in cols:
                cell = Cell(row, col)
                coordinates = (row, col)
                self._cells[coordinates] = cell

    @property
    def rows(self) -> int:
        """ROWS property.

        Returns:
            int: Number of rows.
        """
        return self._rows

    @property
    def columns(self) -> int:
        """COLUMNS property.

        Returns:
            int: Number columns.
        """
        return self._columns

    @property
    def all_cells(self) -> dict[tuple[int, int], Cell]:
        """CELLS property.

        Returns:
            dict[tuple[int, int], FieldCell]: Dictionary with
                    all cells and coordinates { (x,y) -> Cell }
        """
        return self._cells
