"""Tests related to testing game rules."""
import unittest

from gameoflifeapi.logic.data.cell import Cell
from gameoflifeapi.logic.data.state import CellState
from gameoflifeapi.logic.rules import apply_rules_and_change_state


class TestGameRules(unittest.TestCase):
    """Test Game Rules of switching cell state."""

    def test_rule_alive_0(self) -> None:
        """Alive -> 0-1 Alive Neighbour -> Dead."""
        field_cell = Cell(1, 1, CellState.ALIVE)
        field_cell.neighbours = 0

        apply_rules_and_change_state(field_cell)

        self.assertEqual(CellState.DEAD, field_cell.state)

    def test_rule_alive_1(self) -> None:
        """Alive -> 0-1 Alive Neighbour -> Dead."""
        field_cell = Cell(1, 1, CellState.ALIVE)
        field_cell.neighbours = 1

        apply_rules_and_change_state(field_cell)

        self.assertEqual(CellState.DEAD, field_cell.state)

    def test_rule_alive_2(self) -> None:
        """Alive -> 2-3 Alive Neighbour -> Alive."""
        field_cell = Cell(1, 1, CellState.ALIVE)
        field_cell.neighbours = 2

        apply_rules_and_change_state(field_cell)

        self.assertEqual(CellState.ALIVE, field_cell.state)

    def test_rule_alive_3(self) -> None:
        """Alive -> 2-3 Alive Neighbour -> Alive."""
        field_cell = Cell(1, 1, CellState.ALIVE)
        field_cell.neighbours = 3

        apply_rules_and_change_state(field_cell)

        self.assertEqual(CellState.ALIVE, field_cell.state)

    def test_rule_alive_4(self) -> None:
        """Alive -> 4-8 Alive Neighbour -> Dead."""
        field_cell = Cell(1, 1, CellState.ALIVE)
        field_cell.neighbours = 4

        apply_rules_and_change_state(field_cell)

        self.assertEqual(CellState.DEAD, field_cell.state)

    def test_rule_alive_5(self) -> None:
        """Alive -> 4-8 Alive Neighbour -> Dead."""
        field_cell = Cell(1, 1, CellState.ALIVE)
        field_cell.neighbours = 5

        apply_rules_and_change_state(field_cell)

        self.assertEqual(CellState.DEAD, field_cell.state)

    def test_rule_alive_6(self) -> None:
        """Alive -> 4-8 Alive Neighbour -> Dead."""
        field_cell = Cell(1, 1, CellState.ALIVE)
        field_cell.neighbours = 6

        apply_rules_and_change_state(field_cell)

        self.assertEqual(CellState.DEAD, field_cell.state)

    def test_rule_alive_7(self) -> None:
        """Alive -> 4-8 Alive Neighbour -> Dead."""
        field_cell = Cell(1, 1, CellState.ALIVE)
        field_cell.neighbours = 7

        apply_rules_and_change_state(field_cell)

        self.assertEqual(CellState.DEAD, field_cell.state)

    def test_rule_alive_8(self) -> None:
        """Alive -> 4-8 Alive Neighbour -> Dead."""
        field_cell = Cell(1, 1, CellState.ALIVE)
        field_cell.neighbours = 8

        apply_rules_and_change_state(field_cell)

        self.assertEqual(CellState.DEAD, field_cell.state)

    def test_rule_dead_1(self) -> None:
        """Dead -> ==3 Alive Neighbour -> Alive."""
        field_cell = Cell(1, 1, CellState.DEAD)
        field_cell.neighbours = 1

        apply_rules_and_change_state(field_cell)

        self.assertEqual(CellState.DEAD, field_cell.state)

    def test_rule_dead_3(self) -> None:
        """Dead -> ==3 Alive Neighbour -> Alive."""
        field_cell = Cell(1, 1, CellState.DEAD)
        field_cell.neighbours = 3

        apply_rules_and_change_state(field_cell)

        self.assertEqual(CellState.ALIVE, field_cell.state)

    def test_rule_dead_5(self) -> None:
        """Dead -> ==3 Alive Neighbour -> Alive."""
        field_cell = Cell(1, 1, CellState.DEAD)
        field_cell.neighbours = 5

        apply_rules_and_change_state(field_cell)

        self.assertEqual(CellState.DEAD, field_cell.state)
