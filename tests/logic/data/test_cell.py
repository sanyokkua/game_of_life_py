"""Tests related to functionality of the Cell DTO."""
import unittest

from gameoflifeapi.logic.data.cell import Cell
from gameoflifeapi.logic.data.state import CellState


class TestCell(unittest.TestCase):
    """Test Cell functionality."""

    def test_cell_creation(self) -> None:
        """Test creation of the Cell."""
        cell = Cell(10, 11, CellState.ALIVE)

        self.assertEqual(10, cell.row)
        self.assertEqual(11, cell.column)
        self.assertEqual(CellState.ALIVE, cell.state)
        self.assertEqual(0, cell.neighbours)

    def test_cell_modification(self) -> None:
        """Test modification of the Cell."""
        cell = Cell(10, 11, CellState.ALIVE)
        cell.state = CellState.DEAD
        cell.neighbours = 5

        with self.assertRaises(AttributeError):
            cell.row = 5
        with self.assertRaises(AttributeError):
            cell.column = 5
        self.assertEqual(CellState.DEAD, cell.state)
        self.assertEqual(5, cell.neighbours)
