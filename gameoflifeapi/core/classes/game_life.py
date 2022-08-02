
"""Module represent Main Game Functionality."""
import logging

from beartype import beartype

from gameoflifeapi.core.classes.game_cell import GameLifeCell
from gameoflifeapi.core.classes.game_enums import GameLifeCellState

log: logging.Logger = logging.getLogger(__name__)


class GameLife:
    """Represent Game Logic."""

    @beartype
    def __init__(self, number_of_rows: int = 10,
                 number_of_cells: int = 10) -> None:
        """Initialize GameLife object.

        Args:
            number_of_rows (int, optional): Number of rows. Defaults to 10.
            number_of_cells (int, optional): Number of columns. Defaults to 10.
        """
        log.debug('In __init__')
        self._number_of_rows: int = number_of_rows
        self._number_of_cols: int = number_of_cells
        self._game_field: list[list[GameLifeCell]] = self._init_game_field()
        self._previous_field: list[list[GameLifeCell]] = self._game_field
        self._game_life_generation: int = 0
        log.info('GameLife is initialized')
        log.debug('GameLife.__init__: rows: %d, col: %d, gen: %d',
                  self._number_of_rows, self._number_of_cols,
                  self._game_life_generation)

    @beartype
    def _init_game_field(self) -> list[list[GameLifeCell]]:
        """Initialize Game Field with Dead Cells.

        Returns:
            list[list[GameLifeCell]]: Initialized Game Field
        """
        cols: int = self._number_of_cols
        rows: int = self._number_of_rows
        log.debug('_init_game_field: Field with row: %d, col: %d be generated',
                  rows, cols)
        return [[GameLifeCell(row=r, col=c) for c in range(cols)]
                for r in range(rows)]

    @beartype
    def _change_cell_state(self, list_of_coordinates: list[tuple[int, int]],
                           cell_state: GameLifeCellState) -> None:
        """Change Cell State to passed.

        Args:
            list_of_coordinates (list[tuple[int, int]]): coordinates list 
                                [(x,y), (x,y),...]
            cell_state (GameLifeCellState): State of the Cell (ALIVE, DEAD)
        """
        rows = range(self.rows)
        cols = range(self.cols)
        for row_number in rows:
            for col_number in cols:
                if (row_number, col_number) in list_of_coordinates:
                    self._game_field[row_number][col_number].change_state(
                        cell_state)
                    log.debug('_change_cell_state. Cell changed with row: %d, col: %d, state: %s',
                              row_number, col_number, cell_state)

    @beartype
    def _count_amount_alive_neighbour(self, cell_row: int,
                                      cell_col: int) -> int:
        """Count Alive Neighbours around the Cell.

        Model of coordinates of Neighbours
            |-1 -1 | -1 0 | -1 +1|
            ----------------------
            | 0 -1 |  0 0 |  0 +1|
            ----------------------
            |+1 -1 | +1 0 | +1 +1|
        Args:
            cell_row (int): Row of the cell
            cell_col (int): Column of the cell

        Returns:
            int: Number of Alive Neighbours
        """
        log.debug('In _count_amount_alive_neighbour')
        rows = range(self.rows)
        cols = range(self.cols)
        coordinates_diff = (
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        )
        number_of_alive = 0
        log.debug('number of alive = %d', number_of_alive)
        for (x_row, x_col) in coordinates_diff:
            row_to_check = cell_row + x_row
            col_to_check = cell_col + x_col
            if row_to_check in rows and col_to_check in cols:
                cell: GameLifeCell = self.field[row_to_check][col_to_check]
                state: GameLifeCellState = cell.state
                if state is GameLifeCellState.ALIVE:
                    log.debug('Cell (%d, %d) is Alive',
                              row_to_check, col_to_check)
                    number_of_alive += 1
        log.debug('Out _count_amount_alive_neighbour')
        return number_of_alive

    @beartype
    def _apply_rules_and_change_state(self, current_cell: GameLifeCell,
                                      number_of_alive_neighbours: int) -> None:
        """Process cell state based on the rules of game.

        Rules:
        Alive	->	0-1 Alive Neighbour	->	Dead
        Alive	->	2-3 Alive Neighbour	->	Alive
        Alive	->	4-8 Alive Neighbour	->	Dead
        Dead	->	==3 Alive Neighbour	->	Alive

        Args:
            current_cell (GameLifeCell): Cell that should be processed
            number_of_alive_neighbours (int): Number of Alive neighbours
        """
        log.debug('In _apply_rules_and_change_state')
        if current_cell.state is GameLifeCellState.ALIVE:
            self._apply_rules_to_alive_cell(
                current_cell, number_of_alive_neighbours)
        elif current_cell.state is GameLifeCellState.DEAD:
            self._apply_rules_to_dead_cell(
                current_cell, number_of_alive_neighbours)
        log.debug('Out _apply_rules_and_change_state')

    @beartype
    def _apply_rules_to_alive_cell(self, current_cell: GameLifeCell,
                                   number_of_alive_neighbours: int) -> None:
        """Process rules related to the only Alive cell.

        Alive	->	0-1 Alive Neighbour	->	Dead
        Alive	->	2-3 Alive Neighbour	->	Alive
        Alive	->	4-8 Alive Neighbour	->	Dead

        Args:
            current_cell (GameLifeCell): Cell that should be processed
            number_of_alive_neighbours (int): Number of Alive neighbours
        """
        log.debug('In _apply_rules_to_alive_cell')
        if number_of_alive_neighbours < 2:  # 0 or 1
            current_cell.make_dead()
            log.debug('0 or 1 Alive: Cell (%d, %d) make_dead',
                      current_cell.row, current_cell.col)
        elif (number_of_alive_neighbours > 1
              and number_of_alive_neighbours < 4):  # 2 or 3
            current_cell.make_alive()
            log.debug('2 or 3 Alive: Cell (%d, %d) make_alive',
                      current_cell.row, current_cell.col)
        elif number_of_alive_neighbours > 3:  # 3 or more 4, 5, 6, 7, 8
            current_cell.make_dead()
            log.debug('3 or more 4, 5, 6, 7, 8 Alive: Cell (%d, %d) make_dead',
                      current_cell.row, current_cell.col)
        # For all other possible combination we need to skip all processing
        log.debug('Out _apply_rules_to_alive_cell')

    @beartype
    def _apply_rules_to_dead_cell(self, current_cell: GameLifeCell,
                                  number_of_alive_neighbours: int) -> None:
        """Process rules related to the only Dead cell.

        Dead	->	==3 Alive Neighbour	->	Alive

        Args:
            current_cell (GameLifeCell): Cell that should be processed
            number_of_alive_neighbours (int): Number of Alive neighbours
        """
        log.debug('In _apply_rules_to_dead_cell')
        if number_of_alive_neighbours == 3:
            current_cell.make_alive()
            log.debug('alive neighbours = 3: Cell (%d, %d) make_alive',
                      current_cell.row, current_cell.col)
        # For all other possible combination we need to skip all processing
        log.debug('Out _apply_rules_to_dead_cell')

    @property
    def field(self) -> list[list[GameLifeCell]]:
        """Property Field.

        Returns:
            list[list[GameLifeCell]]: Game Field
        """
        log.debug('field property access')
        cols: int = self._number_of_cols
        rows: int = self._number_of_rows
        return [[self._game_field[r][c] for c in range(cols)]
                for r in range(rows)]

    @property
    def rows(self) -> int:
        """Property Row.

        Returns:
            int: Number of ROW
        """
        log.debug('rows property access')
        return len(self._game_field)

    @property
    def cols(self) -> int:
        """Property Column.

        Returns:
            int: Number of COLUMNS
        """
        log.debug('cols property access')
        try:
            return len(self._game_field[0])
        except IndexError:
            return 0

    @property
    def game_life_generation(self) -> int:
        """Property Game Life Generation.

        Returns:
            int: Number of the Last Generaation
        """
        log.debug('figame_life_generation property access')
        return self._game_life_generation

    @property
    def previous_field(self) -> list[list[GameLifeCell]]:
        """Property Previous Field.

        Returns:
            list[list[GameLifeCell]]: Game Field of previous generation
        """
        log.debug('previous field property access')
        cols: int = self._number_of_cols
        rows: int = self._number_of_rows
        return [[self._previous_field[r][c] for c in range(cols)]
                for r in range(rows)]

    @beartype
    def set_alive_cells(self, state_field: list[tuple[int, int]]) -> None:
        """Make the cells by passed coordinate Alive.

        Args:
            state_field (list[tuple[int, int]]): coordinates list 
                                                    [(0,0), (1,3), ..., (x,y)]
        """
        log.debug('set_alive_cells')
        self._change_cell_state(state_field, GameLifeCellState.ALIVE)

    @beartype
    def set_dead_cells(self, state_field: list[tuple[int, int]]) -> None:
        """Make the cells by passed coordinate Dead.

        Args:
            state_field (list[tuple[int, int]]): coordinates list 
                                                    [(0,0), (1,3), ..., (x,y)]
        """
        log.debug('set_dead_cells')
        self._change_cell_state(state_field, GameLifeCellState.DEAD)

    @beartype
    def create_new_generation(self) -> None:
        """Process current Game Field to generate new Generation.

        Each Cell will be processed and status will be changed based on the
        Alive/Dead Neighbours.

        Generation count will be incremented.
        """
        log.debug('create_new_generation')
        for row in self.field:
            for cell in row:
                alive_neighbours: int = self._count_amount_alive_neighbour(
                    cell.row, cell.col)
                self._apply_rules_and_change_state(cell, alive_neighbours)
        self._game_life_generation += 1

    @beartype
    def is_the_final_generation(self) -> bool:
        """Check if the current generation is final.

        if previous game field is equal to the current game field it means
        that now new generation expected, nothing will change
        Returns:
            bool: _description_
        """
        return (self._game_life_generation > 0
                and self._previous_field == self._game_field)
