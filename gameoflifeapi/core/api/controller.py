import logging

from beartype import beartype
from gameoflifeapi.core.api.persistance import GameLifePicklePersistance
from gameoflifeapi.core.classes.game_cell import GameLifeCell
from gameoflifeapi.core.classes.game_life import GameLife

log: logging.Logger = logging.getLogger(__name__)


class GameLifeController:

    def __init__(self) -> None:
        self._current_game_instance: GameLife = None

    @property
    def game_field(self) -> list[list[GameLifeCell]]:
        return self._current_game_instance.field

    @beartype
    def start_new_game(self, rows: int, cols: int) -> None:
        log.info('start_new_game')

    @beartype
    def load_saved_game(self, save_file_name: str) -> None:
        log.info('load_saved_game')

    @beartype
    def save_game(self, save_file_name: str) -> None:
        log.info('save_game')

    @beartype
    def edit_current_field_state(self) -> None:
        log.info('edit_current_field_state')

    @beartype
    def increment_generation(self) -> None:
        log.info('increment_generation')

    @beartype
    def is_finished(self) -> bool:
        log.info('is_finished')
        return False
