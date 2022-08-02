
"""Definition of the abstract classes."""
from abc import ABC, abstractmethod

from gameoflifeapi.core.classes.game_cell import GameLifeCell
from gameoflifeapi.core.classes.game_enums import GameLifeCellState
from gameoflifeapi.core.classes.game_life import GameLife


class AbstractController(ABC):
    """Abstract Persistance."""

    @property
    @abstractmethod
    def game_field(self) -> list[list[GameLifeCell]]:
        pass

    @property
    @abstractmethod
    def field_rows(self) -> int:
        pass

    @property
    @abstractmethod
    def field_columns(self) -> int:
        pass

    @abstractmethod
    def start_new_game(self, rows: int, cols: int) -> None:
        pass

    @abstractmethod
    def load_saved_game(self, save_file_name: str) -> None:
        pass

    @abstractmethod
    def save_game(self, save_file_name: str) -> None:
        pass

    @abstractmethod
    def edit_current_field_state(self, fields: list[tuple[int, int]],
                                 state: GameLifeCellState) -> None:
        pass

    @abstractmethod
    def increment_generation(self) -> None:
        pass

    @abstractmethod
    def is_finished(self) -> bool:
        pass

    @abstractmethod
    def get_all_states(self) -> tuple[GameLifeCellState, ...]:
        pass

    @abstractmethod
    def make_random_cell_states(self) -> None:
        pass


class AbstractPersistance(ABC):

    @abstractmethod
    def save_game(self, file_name: str, game_instance: GameLife) -> None:
        pass

    @abstractmethod
    def load_game(self, file_name: str) -> GameLife:
        pass
