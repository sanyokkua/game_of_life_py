"""Tests related to functionality of the GameData DTOs."""
import unittest

from gameoflifeapi.logic.data.dtos import (GameDataDto, GameStateDto,
                                           LoadGameDataDto, NewGameDataDto)
from gameoflifeapi.logic.data.field import Field


class TestDtos(unittest.TestCase):
    """Test Game DTOs."""

    def test_game_data_dto(self) -> None:
        """Test GameDataDto common class."""
        game_data = GameDataDto(
            number_of_rows=11,
            number_of_columns=12,
            is_random_first_generation=True,
            generation=5,
            game_field=Field(11, 12)
        )

        self.assertEqual(11, game_data.number_of_rows)
        self.assertEqual(12, game_data.number_of_columns)
        self.assertEqual(5, game_data.generation)
        self.assertEqual(11, game_data.game_field.rows)
        self.assertEqual(12, game_data.game_field.columns)
        self.assertTrue(game_data.is_random_first_generation)

        with self.assertRaises(AttributeError):
            game_data.number_of_rows = 25
        with self.assertRaises(AttributeError):
            game_data.number_of_columns = 35
        with self.assertRaises(AttributeError):
            game_data.generation = 45
        with self.assertRaises(AttributeError):
            game_data.is_random_first_generation = False
        with self.assertRaises(AttributeError):
            game_data.game_field = None

    def test_new_game_data_dto(self) -> None:
        """Test NewGameDataDto class."""
        game_data = NewGameDataDto(
            number_of_rows=11,
            number_of_columns=12,
            is_random_first_generation=True
        )

        self.assertEqual(11, game_data.number_of_rows)
        self.assertEqual(12, game_data.number_of_columns)
        self.assertEqual(0, game_data.generation)
        self.assertTrue(game_data.is_random_first_generation)
        self.assertIsNone(game_data.game_field)

        with self.assertRaises(AttributeError):
            game_data.number_of_rows = 25
        with self.assertRaises(AttributeError):
            game_data.number_of_columns = 35
        with self.assertRaises(AttributeError):
            game_data.generation = 45
        with self.assertRaises(AttributeError):
            game_data.is_random_first_generation = False
        with self.assertRaises(AttributeError):
            game_data.game_field = None

    def test_load_game_data_dto(self) -> None:
        """Test LoadGameDataDto class."""
        game_field = Field(15, 16)
        game_data = LoadGameDataDto(
            generation=5,
            game_field=game_field
        )

        self.assertEqual(15, game_data.number_of_rows)
        self.assertEqual(16, game_data.number_of_columns)
        self.assertEqual(5, game_data.generation)
        self.assertEqual(15, game_data.game_field.rows)
        self.assertEqual(16, game_data.game_field.columns)
        self.assertFalse(game_data.is_random_first_generation)

        with self.assertRaises(AttributeError):
            game_data.number_of_rows = 25
        with self.assertRaises(AttributeError):
            game_data.number_of_columns = 35
        with self.assertRaises(AttributeError):
            game_data.generation = 45
        with self.assertRaises(AttributeError):
            game_data.is_random_first_generation = False
        with self.assertRaises(AttributeError):
            game_data.game_field = None

    def test_game_state_dto(self) -> None:
        """Test GameStateDto class."""
        game_field = Field(15, 16)
        game_state = GameStateDto(game_field, 3)

        self.assertEqual(15, game_state.game_field.rows)
        self.assertEqual(16, game_state.game_field.columns)
        self.assertEqual(3, game_state.generation)
        with self.assertRaises(AttributeError):
            game_state.generation = 45
        with self.assertRaises(AttributeError):
            game_state.game_field = None
