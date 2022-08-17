"""Module contains persistance functionality for the Game."""
import logging
import pickle

from gameoflifeapi.api.abstract_definitions import AbstractPersistance
from gameoflifeapi.logic.data.dtos import LoadGameDataDto, SaveGameDataDto
from gameoflifeapi.logic.data.field import Field

log: logging.Logger = logging.getLogger(__name__)


class GamePicklePersistance(AbstractPersistance):
    """Represent functionality of the loading and saving game."""

    def save_game(self, file_name: str,
                  save_game_data: SaveGameDataDto) -> None:
        """Save the game.

        Saves passed instance of the game.

        Args:
            file_name (str): Name of the file where game will be saved
            save_game_data (SaveGameDataDto): Instance data of the game
        """
        log.debug('save_game: Game will be saved, file=%s, game_inst: %s',
                  file_name, save_game_data)
        file_name: str = f'{file_name}'
        with open(file_name, 'wb') as file:
            pickle.dump(save_game_data, file)
            log.debug('save_game: file dumped to file: %s',
                      file_name)

    def load_game(self, file_name: str) -> LoadGameDataDto:
        """Load game instance.

        Load saved instance of the game from file.

        Args:
            file_name (str): Name of the Saved Game file

        Returns:
            LoadGameDataDto: Instance data of the game
        """
        save_game_data: SaveGameDataDto = None
        file_name: str = f'{file_name}'

        with open(file_name, 'rb') as file:
            save_game_data: SaveGameDataDto = pickle.load(file)
            log.debug('load_game: file loaded from file: %s',
                      file_name)

        generation: int = save_game_data.generation
        field: Field = save_game_data.game_field
        return LoadGameDataDto(generation, field)
