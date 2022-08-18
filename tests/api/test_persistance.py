"""Tests related to the persistance functionality."""
import os
import pathlib as pl
import tempfile
import unittest

from gameoflifeapi.api.persistance import GamePicklePersistance
from gameoflifeapi.logic.data.dtos import LoadGameDataDto, SaveGameDataDto
from gameoflifeapi.logic.data.field import Field
from gameoflifeapi.logic.data.state import CellState

SAVE_GAME_FILE_NAME: str = 'test_game_save_file.gsave'


class TestGamePicklePersistance(unittest.TestCase):
    """Tests related to the TestGamePicklePersistance functionality."""

    def setUp(self) -> None:
        """Prepare test case to the tests."""
        tmp_dir: str = tempfile.gettempdir()
        save_name = f'{tmp_dir}/{SAVE_GAME_FILE_NAME}'
        print(f'File Path for TEST SAVE FILE = {save_name}')
        if os.path.exists(save_name):
            print(f'File Path for TEST SAVE FILE = {save_name} is EXIST')
            os.remove(save_name)
        else:
            print(f'File Path for TEST SAVE FILE = {save_name} is NOT Exist')

    def tearDown(self) -> None:
        """Cleanup after tests."""
        tmp_dir: str = tempfile.gettempdir()
        save_name = f'{tmp_dir}/{SAVE_GAME_FILE_NAME}'
        if os.path.exists(save_name):
            os.remove(save_name)

    def test_save_game(self) -> None:
        """Test save game functionality."""
        tmp_dir: str = tempfile.gettempdir()
        save_name: str = f'{tmp_dir}/test_game_save_file.gsave'
        game_field: Field = Field()

        persistance = GamePicklePersistance()
        persistance.save_game(save_name, SaveGameDataDto(5, game_field))
        file_to_check = pl.Path(save_name).resolve()

        self.assertTrue(file_to_check.is_file())

    def test_load_game(self) -> None:
        """Test save and load game functionality."""
        tmp_dir: str = tempfile.gettempdir()
        save_name: str = f'{tmp_dir}/test_game_save_file.gsave'
        game_field: Field = Field()
        game_field.all_cells[(0, 0)].state = CellState.ALIVE
        game_field.all_cells[(1, 5)].state = CellState.ALIVE
        game_field.all_cells[(2, 7)].state = CellState.ALIVE
        game_field.all_cells[(3, 0)].state = CellState.ALIVE

        persistance = GamePicklePersistance()
        persistance.save_game(save_name, SaveGameDataDto(5, game_field))
        file_to_check = pl.Path(save_name).resolve()

        self.assertTrue(file_to_check.is_file())

        loaded: LoadGameDataDto = persistance.load_game(save_name)
        self.assertEqual(5, loaded.generation)
        self.assertEqual(10, loaded.number_of_rows)
        self.assertEqual(10, loaded.number_of_columns)
        self.assertEqual(CellState.ALIVE, loaded.game_field.all_cells[(0, 0)].state)
        self.assertEqual(CellState.ALIVE, loaded.game_field.all_cells[(1, 5)].state)
        self.assertEqual(CellState.ALIVE, loaded.game_field.all_cells[(2, 7)].state)
        self.assertEqual(CellState.ALIVE, loaded.game_field.all_cells[(3, 0)].state)
