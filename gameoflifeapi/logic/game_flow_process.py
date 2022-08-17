"""Defines Game Flow Process API."""
import logging
import math
import random
from typing import Callable

from gameoflifeapi.logic.data.cell import Cell
from gameoflifeapi.logic.data.field import Field
from gameoflifeapi.logic.data.state import CellState
from gameoflifeapi.logic.exceptions import GenerationValueException
from gameoflifeapi.logic.rules import apply_rules_and_change_state

log: logging.Logger = logging.getLogger(__name__)


class GameFlowProcess:
    """Game Flow Process implementation."""

    def __init__(self, rows: int = 10,
                 columns: int = 10,
                 generation: int = 0,
                 game_field: Field = None,
                 on_generation_created: Callable[[], None] = None) -> None:
        """Initialize GameController.

        Args:
            rows (int, optional): Number of rows. Defaults to 10.
            columns (int, optional): Number of columns. Defaults to 10.
            generation (int, optional): Number of current generation.
                                                            Defaults to 10.
        """
        if generation < 0:
            raise GenerationValueException("Generation can't be lower 0")

        self._game_field: Field = game_field

        if not game_field:
            self._game_field = Field(rows, columns)

        self._generation: int = generation
        if on_generation_created:
            self._on_generation_created = on_generation_created
        else:
            def default_handler() -> None:
                log.debug('Default on_generation_created')

            self._on_generation_created = default_handler

    @property
    def game_field(self) -> Field:
        """Return Game Field Property.

        Returns:
            GameField: current GameField
        """
        return self._game_field

    @property
    def generation(self) -> int:
        """Return geneneration number.

        Returns:
            int: Number of the current generation
        """
        return self._generation

    def switch_cell_state(self, row: int, column: int) -> None:
        """Change Cell state to opposite.

        Args:
            row (int): ROW coordinate
            column (int): COLUMN coordinate
        """
        all_cells: dict[tuple[int, int], Cell] = self._game_field.all_cells
        current_cell: Cell = all_cells[(row, column)]
        current_state: CellState = current_cell.state
        if current_state is CellState.ALIVE:
            current_cell.state = CellState.DEAD
        else:
            current_cell.state = CellState.ALIVE

    def create_next_generation(self) -> None:
        """Create next generation of the field."""
        for ((_row, _col), cell) in self._game_field.all_cells.items():
            apply_rules_and_change_state(cell)
        self._generation += 1
        self._count_neighbours_for_field()

    def randomize_next_generation(self) -> None:
        """Change state of cells in random way."""
        for ((row, col), _cell) in self._game_field.all_cells.items():
            if bool(random.getrandbits(1)):
                self.switch_cell_state(row, col)
        self._count_neighbours_for_field()

    def _count_neighbours_for_field(self) -> None:
        """Count number of the alive neighbour cells for each cell."""
        for ((_row, _col), cell) in self._game_field.all_cells.items():
            self._count_neighbours_for_cell(cell)
        self._on_generation_created()

    def _count_neighbours_for_cell(self, cell: Cell) -> None:
        """Count the number of alive cells around passed cell.

        Args:
            cell (FieldCell): _description_
        """
        coordinates_diff: set = {
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        }
        row: int = cell.row
        col: int = cell.column
        count: int = 0
        for row_diff, col_diff in coordinates_diff:
            to_visit_row: int = row + row_diff
            to_visit_col: int = col + col_diff
            is_not_valid_row: bool = to_visit_row < 0 or to_visit_col > self.game_field.rows
            is_not_valid_col: bool = to_visit_col < 0 or to_visit_col > self.game_field.columns
            if is_not_valid_row or is_not_valid_col:
                continue
            try:
                cells: dict[tuple[int, int], Cell] = self._game_field.all_cells
                neighbour_cell: Cell = cells[(to_visit_row, to_visit_col)]
                if neighbour_cell.state is CellState.ALIVE:
                    count += 1
            except KeyError as err:
                log.debug('Coordinate is not valid, %s', err)
        cell.neighbours = count
