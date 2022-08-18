"""Definition of the main controller of the game."""
import logging
from typing import Callable

from gameoflifeapi.api.abstract_definitions import (AbstractController,
                                                    AbstractPersistance)
from gameoflifeapi.logic.data.dtos import (LoadGameDataDto, NewGameDataDto,
                                           SaveGameDataDto)
from gameoflifeapi.logic.data.field import Field
from gameoflifeapi.logic.game_flow_process import GameFlowProcess

log: logging.Logger = logging.getLogger(__name__)


class GameLifeController(AbstractController):
    """Main Controller of the game."""

    def __init__(self, persistance: AbstractPersistance,
                 on_generation_created: Callable[[], None]) -> None:
        """Initialize Controller.

        Args:
            persistance (AbstractPersistance): Persistance used for
                                                saving/loadind game
        """
        AbstractController.__init__(self, persistance)
        self._on_generation_created = on_generation_created
        log.debug('__init__')

    def start_new_game(self, new_game_data: NewGameDataDto) -> None:
        """Start new game.

        Args:
            new_game_data (NewGameDataDto): New Game Data
        """
        log.debug('start_new_game')
        self._game_flow = GameFlowProcess(
            rows=new_game_data.number_of_rows,
            columns=new_game_data.number_of_columns,
            on_generation_created=self._on_generation_created
        )
        if new_game_data.is_random_first_generation:
            self._game_flow.randomize_next_generation()
        log.debug('start_new_game: Created game, rows=%d, cols=%d, rand=%s',
                  self.rows,
                  self.columns,
                  new_game_data.is_random_first_generation)

    def load_game(self, save_file_name: str) -> None:
        """Load saved game.

        Args:
            save_file_name (str): save game file name
        """
        log.debug('load_saved_game')
        game_data: LoadGameDataDto = self._persistance.load_game(
            save_file_name)
        game_field: Field = game_data.game_field
        generation: int = game_data.generation

        self._game_flow = GameFlowProcess(
            game_field=game_field,
            generation=generation,
            rows=game_field.rows,
            columns=game_field.columns,
            on_generation_created=self._on_generation_created
        )
        self._on_generation_created()
        log.debug('load_saved_game: Loaded game, rows=%d, cols=%d, gen=%d',
                  self.rows,
                  self.columns,
                  self._game_flow.generation)

    def save_game(self, save_file_name: str) -> None:
        """Save game.

        Args:
            save_file_name (str): save game file name
        """
        log.debug('save_game')
        log.debug('Save File Name = %s', save_file_name)
        save_game_data: SaveGameDataDto = SaveGameDataDto(
            game_field=self._game_flow.game_field,
            generation=self._game_flow.generation
        )
        self._persistance.save_game(save_file_name, save_game_data)
        log.debug('save_game: Saved game, rows=%d, cols=%d, gen=%d',
                  self.rows,
                  self.columns,
                  self._game_flow.generation)

    def trigger_cell(self, row_number: int, column_numbed: int) -> None:
        """Change state of the cells in field.

        Args:
            fields (list[tuple[int, int]]): coordinates of cells
            state (GameLifeCellState): cell state
        """
        log.debug('trigger_cell')
        self._game_flow.switch_cell_state(row_number, column_numbed)

    def increment_generation(self) -> None:
        """Generate new generation."""
        log.debug('increment_generation')
        self._game_flow.create_next_generation()

    def randomize_cells_state(self) -> None:
        """Set cells state by random values."""
        log.debug('make_random_cell_states')
        self._game_flow.randomize_next_generation()
