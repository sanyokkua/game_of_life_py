import logging
import random

from beartype import beartype
from gameoflifeapi.core.api.abstract.definitions import (AbstractPersistance,
                                                         AbstractController)
from gameoflifeapi.core.classes.game_cell import GameLifeCell
from gameoflifeapi.core.classes.game_enums import GameLifeCellState
from gameoflifeapi.core.classes.game_life import GameLife

log: logging.Logger = logging.getLogger(__name__)


class GameLifeController(AbstractController):
    """Main Controller of the game."""

    def __init__(self, persistance: AbstractPersistance) -> None:
        """Initialize Controller.

        Args:
            persistance (AbstractPersistance): Persistance used for
                                                saving/loadind game
        """
        log.info('__init__')
        self._current_game_instance: GameLife = None
        self._persistance: AbstractPersistance = persistance

    @property
    def game_field(self) -> list[list[GameLifeCell]]:
        """Return game field.

        Returns:
            list[list[GameLifeCell]]: Game field
        """
        log.info('game_field')
        return self._current_game_instance.field

    @property
    def field_rows(self) -> int:
        """Return number of rows.

        Returns:
            int: number of rows
        """
        log.info('__ifield_rowsit__')
        if self._current_game_instance:
            return self._current_game_instance.rows
        else:
            return 0

    @property
    def field_columns(self) -> int:
        """Return number of columns.

        Returns:
            int: number of columns
        """
        log.info('field_columns')
        if self._current_game_instance:
            return self._current_game_instance.cols
        else:
            return 0

    @beartype
    def start_new_game(self, rows: int, cols: int) -> None:
        """Start new game.

        Args:
            rows (int): number of rows
            cols (int): number of columns
        """
        log.info('start_new_game')
        self._current_game_instance = GameLife(rows, cols)
        log.debug('start_new_game: Created game, rows=%d, cols=%d',
                  self._current_game_instance.rows,
                  self._current_game_instance.cols)

    @beartype
    def load_saved_game(self, save_file_name: str) -> None:
        """Load saved game.

        Args:
            save_file_name (str): save game file name
        """
        log.info('load_saved_game')
        self._current_game_instance = self._persistance.load_game(
            save_file_name)
        log.debug('load_saved_game: Loaded game, rows=%d, cols=%d, gen=%d',
                  self._current_game_instance.rows,
                  self._current_game_instance.cols,
                  self._current_game_instance.generation)

    @beartype
    def save_game(self, save_file_name: str) -> None:
        """Save game.

        Args:
            save_file_name (str): save game file name
        """
        log.info('save_game')
        log.debug('Save File Name = %s', save_file_name)
        self._persistance.save_game(
            save_file_name, self._current_game_instance)
        log.debug('save_game: Saved game, rows=%d, cols=%d, gen=%d',
                  self._current_game_instance.rows,
                  self._current_game_instance.cols,
                  self._current_game_instance.generation)

    @beartype
    def edit_current_field_state(self, fields: list[tuple[int, int]],
                                 state: GameLifeCellState) -> None:
        """Change state of the cells in field.

        Args:
            fields (list[tuple[int, int]]): coordinates of cells
            state (GameLifeCellState): cell state
        """
        log.info('edit_current_field_state')
        if state is GameLifeCellState.ALIVE:
            log.debug('edit_current_field_state:set_alive_cells')
            self._current_game_instance.set_alive_cells(fields)
        else:
            log.debug('edit_current_field_state:set_dead_cells')
            self._current_game_instance.set_dead_cells(fields)

    def increment_generation(self) -> None:
        """Generate new generation."""
        log.info('increment_generation')
        self._current_game_instance.create_new_generation()

    @beartype
    def is_finished(self) -> bool:
        """Check if the game is finished.

        Checks if the current generation is the final

        Returns:
            bool: True if the final generation
        """
        log.info('is_finished')
        return self._current_game_instance.is_the_final_generation()

    @beartype
    def get_all_states(self) -> tuple[GameLifeCellState, ...]:
        """Return tuple of possible states.

        Returns:
            tuple[GameLifeCellState, ...]: tuple of the states
        """
        log.info('get_all_states')
        return (GameLifeCellState.ALIVE, GameLifeCellState.DEAD)

    def make_random_cell_states(self) -> None:
        """Set cells state by random values."""
        log.info('make_random_cell_states')
        max_number_of_cells: int = self.field_rows * self.field_columns
        min_number_of_cells: int = 5
        number_of_cells_to_make_alive: int = random.randrange(
            min_number_of_cells, max_number_of_cells)
        initial_state: set[tuple[int, int]] = set()
        while number_of_cells_to_make_alive > 0:
            random_row: int = random.randrange(0, self.field_rows)
            random_col: int = random.randrange(0, self.field_columns)
            initial_state.add((random_row, random_col))
            number_of_cells_to_make_alive -= 1
        log.debug('make_random_cell_states: cells number=%d',
                  len(initial_state))
        self.edit_current_field_state(
            list(initial_state), GameLifeCellState.ALIVE)
