"""Module contains persistance functionality for the Game."""
import pickle
import logging

from beartype import beartype
from gameoflifeapi.core.classes.game_life import GameLife

log: logging.Logger = logging.getLogger(__name__)
FILE_SAVE_EXTENSION: str = '.gsave'


class GameLifePicklePersistance:
    """Represent functionality of the loading and saving game."""

    @beartype
    def save_game(self, file_name: str, game_instance: GameLife) -> None:
        """Save the game.

        Saves passed instance of the game.

        Args:
            file_name (str): Name of the file where game will be saved
            game_instance (GameLife): Instance of the game
        """
        log.debug('save_game: Game will be saved, file=%s, game_inst: %s',
                  file_name, game_instance)
        file_name = f'{file_name}{FILE_SAVE_EXTENSION}'
        with open(file_name, 'wb') as file:
            pickle.dump(game_instance, file)
            log.debug('save_game: file dumped to file: %s',
                      file_name)

    @beartype
    def load_game(self, file_name: str) -> GameLife:
        """Load game instance.

        Load saved instance of the game from file.

        Args:
            file_name (str): Name of the Saved Game file

        Returns:
            GameLife: Instance of the game
        """
        game_life_loaded: GameLife = None
        file_name = f'{file_name}{FILE_SAVE_EXTENSION}'
        with open(file_name, 'rb') as file:
            game_life_loaded = pickle.load(file)
            log.debug('load_game: file loaded from file: %s',
                      file_name)
        return game_life_loaded
