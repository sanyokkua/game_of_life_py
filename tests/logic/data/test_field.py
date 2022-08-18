"""Tests related to functionality of the Field object."""
import unittest

from gameoflifeapi.logic.data.field import Field
from gameoflifeapi.logic.data.state import CellState
from gameoflifeapi.logic.exceptions import GameFieldSizeException


class TestGameField(unittest.TestCase):
    """Test Game Field functionality."""

    def test_game_field_creation(self) -> None:
        """Test creation of the field."""
        field = Field()

        self.assertEqual(10, field.rows)
        self.assertEqual(10, field.columns)
        self.assertIsNotNone(field.all_cells)
        self.assertEqual(100, len(field.all_cells))
        for (coordinates, cell) in field.all_cells.items():
            self.assertEqual(CellState.DEAD, cell.state,
                             f'Cell with coordinates {coordinates} is not DEAD')

    def test_game_field_creation_validation(self) -> None:
        """Test game field creation validation."""
        with self.assertRaises(GameFieldSizeException):
            Field(None, None)
        with self.assertRaises(GameFieldSizeException):
            Field(0, 0)
        with self.assertRaises(GameFieldSizeException):
            Field(5, 5)

    def test_game_field_creation_custom_size(self) -> None:
        """Test game field creation with non-default parameters."""
        num_of_rows = 12
        num_of_cols = 13
        num_of_cells = num_of_rows * num_of_cols
        field = Field(num_of_rows, num_of_cols)

        self.assertEqual(num_of_rows, field.rows)
        self.assertEqual(num_of_cols, field.columns)
        self.assertIsNotNone(field.all_cells)
        self.assertEqual(num_of_cells, len(field.all_cells))
        for (coordinates, cell) in field.all_cells.items():
            self.assertEqual(CellState.DEAD, cell.state,
                             f'Cell with coordinates {coordinates} is not DEAD')

    def test_game_field_property_rows(self) -> None:
        """Test readonly row property of the field."""
        field = Field()
        with self.assertRaises(AttributeError):
            field.rows = 3

    def test_game_field_property_columns(self) -> None:
        """Test readonly column property of the field."""
        field = Field()
        with self.assertRaises(AttributeError):
            field.columns = 3

    def test_game_field_property_all_cells(self) -> None:
        """Test readonly all_cells property of the field."""
        field = Field()
        with self.assertRaises(AttributeError):
            field.all_cells = {}
