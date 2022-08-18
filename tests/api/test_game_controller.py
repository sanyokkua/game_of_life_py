"""Tests related to the Game controller."""
import unittest
import unittest.mock as mock

from gameoflifeapi.api.game_controller import GameLifeController
from gameoflifeapi.logic.data.dtos import (LoadGameDataDto, NewGameDataDto,
                                           SaveGameDataDto)
from gameoflifeapi.logic.data.field import Field
from gameoflifeapi.logic.data.state import CellState


class TestGameLifeController(unittest.TestCase):
    """Tests related to the Game controller Class."""

    def test_creation_of_controller(self) -> None:
        """Test creation of the controller."""
        game_field = Field()
        load_game = LoadGameDataDto(5, game_field)

        mock_persistance = mock.Mock()
        attrs = {'save_game.return_value': None, 'load_game.return_value': load_game}
        mock_persistance.configure_mock(**attrs)
        mock_on_generation = mock.Mock()

        controller = GameLifeController(
            persistance=mock_persistance,
            on_generation_created=mock_on_generation
        )

        self.assertIsNone(controller._game_flow)
        mock_on_generation.assert_not_called()

    def test_start_new_game(self) -> None:
        """Test starting of the new game."""
        new_game = NewGameDataDto(10, 10, True)
        mock_persistance = mock.Mock()
        mock_on_generation = mock.Mock()
        controller = GameLifeController(
            persistance=mock_persistance,
            on_generation_created=mock_on_generation
        )
        controller.start_new_game(new_game)

        self.assertIsNotNone(controller._game_flow)
        self.assertEqual(10, controller._game_flow.game_field.rows)
        self.assertEqual(10, controller._game_flow.game_field.columns)
        self.assertEqual(10, controller.rows)
        self.assertEqual(10, controller.columns)
        self.assertEqual(0, controller.game_state.generation)
        mock_on_generation.assert_called_once()

    def test_load_game(self) -> None:
        """Test loading of the game."""
        save_file_name = 'test_path'
        game_field = Field()
        load_game = LoadGameDataDto(5, game_field)

        mock_persistance = mock.Mock()
        mock_persistance.load_game = mock.Mock()
        mock_persistance.load_game.return_value = load_game
        mock_on_generation = mock.Mock()

        controller = GameLifeController(
            persistance=mock_persistance,
            on_generation_created=mock_on_generation
        )
        controller.load_game(save_file_name)

        self.assertIsNotNone(controller._game_flow)
        self.assertEqual(10, controller._game_flow.game_field.rows)
        self.assertEqual(10, controller._game_flow.game_field.columns)
        self.assertEqual(10, controller.rows)
        self.assertEqual(10, controller.columns)
        self.assertEqual(5, controller.game_state.generation)
        mock_persistance.load_game.assert_called_with(save_file_name)
        mock_on_generation.assert_called()

    @mock.patch('gameoflifeapi.api.game_controller.SaveGameDataDto')
    def test_save_game(self, save_game_data_mock) -> None:
        """Test saving of the game."""
        save_file_name = 'test_save_path'
        new_game = NewGameDataDto(10, 10, True)
        mock_persistance = mock.Mock()
        mock_persistance.save_game = mock.Mock()
        mock_on_generation = mock.Mock()
        controller = GameLifeController(
            persistance=mock_persistance,
            on_generation_created=mock_on_generation
        )
        controller.start_new_game(new_game)
        save_game_data = SaveGameDataDto(
            generation=controller.game_state.generation,
            game_field=controller.game_state.game_field
        )
        save_game_data_mock.return_value = save_game_data

        controller.save_game(save_file_name)

        self.assertIsNotNone(controller._game_flow)
        mock_persistance.save_game.assert_called_with(save_file_name, save_game_data)
        mock_on_generation.assert_called()

    def test_trigger_cell(self) -> None:
        """Test triggering cell."""
        new_game = NewGameDataDto(10, 10, False)
        mock_persistance = mock.Mock()
        mock_on_generation = mock.Mock()
        controller = GameLifeController(
            persistance=mock_persistance,
            on_generation_created=mock_on_generation
        )
        controller.start_new_game(new_game)

        controller.trigger_cell(0, 0)
        controller.trigger_cell(2, 3)
        controller.trigger_cell(5, 7)

        self.assertEqual(CellState.ALIVE, controller.game_state.game_field.all_cells[(0, 0)].state)
        self.assertEqual(CellState.ALIVE, controller.game_state.game_field.all_cells[(2, 3)].state)
        self.assertEqual(CellState.ALIVE, controller.game_state.game_field.all_cells[(5, 7)].state)
        mock_on_generation.assert_not_called()

    def test_increment_generation(self) -> None:
        """Test incrementing (creation) of the new generation."""
        new_game = NewGameDataDto(10, 10, False)
        mock_persistance = mock.Mock()
        mock_on_generation = mock.Mock()
        mock_create_next_generation = mock.Mock()
        controller = GameLifeController(
            persistance=mock_persistance,
            on_generation_created=mock_on_generation
        )
        controller.start_new_game(new_game)
        controller._game_flow = mock.Mock()
        controller._game_flow.create_next_generation = mock_create_next_generation

        controller.increment_generation()

        mock_create_next_generation.assert_called_once()

    def test_randomize_cells_state(self) -> None:
        """Test randomizing field cell states."""
        new_game = NewGameDataDto(10, 10, False)
        mock_persistance = mock.Mock()
        mock_on_generation = mock.Mock()
        mock_randomize_next_generation = mock.Mock()
        controller = GameLifeController(
            persistance=mock_persistance,
            on_generation_created=mock_on_generation
        )
        controller.start_new_game(new_game)
        controller._game_flow = mock.Mock()
        controller._game_flow.randomize_next_generation = mock_randomize_next_generation

        controller.randomize_cells_state()

        mock_randomize_next_generation.assert_called_once()
