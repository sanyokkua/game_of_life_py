"""Tests related to functionality of the CellState formatting."""
import unittest

from gameoflifeapi.logic.data.state import CellState


class TestCellState(unittest.TestCase):
    """Tests of the __repr__ of the enum."""

    def test_repr_of_cell_state(self) -> None:
        """Validate __repr__ method."""
        dead = CellState.DEAD.__repr__()
        alive = CellState.ALIVE.__repr__()

        self.assertEqual('DEAD', dead)
        self.assertEqual('ALIVE', alive)
