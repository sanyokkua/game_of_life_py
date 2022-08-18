"""Definition of the abstract classes."""
from abc import ABC, abstractmethod

from gameoflifeapi.logic.data.dtos import (GameStateDto, LoadGameDataDto,
                                           NewGameDataDto, SaveGameDataDto)
from gameoflifeapi.logic.game_flow_process import GameFlowProcess


class AbstractPersistance(ABC):
    """AbstractPersistance Abstract class for file persistance."""

    @abstractmethod
    def save_game(self, file_name: str,
                  save_game_data: SaveGameDataDto) -> None:
        """save_game Save game to persistence object.

        Args:
            file_name (str): File Name
            game_state (GameState): GameState
        """
        pass

    @abstractmethod
    def load_game(self, file_name: str) -> LoadGameDataDto:
        """load_game Load game from persistance object.

        Args:
            file_name (str): File Name

        Returns:
            GameState: Game State
        """
        pass


class AbstractController(ABC):
    """Abstract Controller."""

    def __init__(self, persistance: AbstractPersistance) -> None:
        """__init__ Initialize Controller.

        Args:
            persistance (AbstractPersistance): persistance
        """
        super().__init__()
        self._persistance: AbstractPersistance = persistance
        self._game_flow: GameFlowProcess = None

    @property
    def rows(self) -> int:
        """Return Number of rows.

        Returns:
            int: value
        """
        if self._game_flow is not None:
            return self._game_flow.game_field.rows
        return 0

    @property
    def columns(self) -> int:
        """Return Number of columns.

        Returns:
            int: value
        """
        if self._game_flow is not None:
            return self._game_flow.game_field.columns
        return 0

    @property
    def game_state(self) -> GameStateDto:
        """Return Game Genearation Value Property.

        Returns:
            GameState: GameState
        """
        state: GameStateDto = GameStateDto(
            game_field=self._game_flow.game_field,
            generation=self._game_flow.generation)
        return state

    @abstractmethod
    def start_new_game(self, new_game_data: NewGameDataDto) -> None:
        pass

    @abstractmethod
    def load_game(self, file_name: str) -> None:
        pass

    @abstractmethod
    def save_game(self, file_name: str) -> None:
        pass

    @abstractmethod
    def trigger_cell(self, row_number: int, column_numbed: int) -> None:
        pass

    @abstractmethod
    def increment_generation(self) -> None:
        pass

    @abstractmethod
    def randomize_cells_state(self) -> None:
        pass
