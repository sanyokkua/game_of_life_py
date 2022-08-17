"""Defines rules used for state change in the game."""
import logging

from gameoflifeapi.logic.data.cell import Cell
from gameoflifeapi.logic.data.state import CellState

log: logging.Logger = logging.getLogger(__name__)


def _rule_alive_from_0_to_1(field_cell: Cell) -> None:
    """Change Statte of the Cell.

    Alive	->	0-1 Alive Neighbour	->	Dead

    Args:
        field_cell (FieldCell): Cell that should be processed
    """
    field_cell.state = CellState.DEAD
    log.debug('0 or 1 Alive: Cell (%d, %d) make_dead',
              field_cell.row, field_cell.column)


def _rule_alive_from_2_to_3(field_cell: Cell) -> None:
    """Change Statte of the Cell.

    Alive	->	2-3 Alive Neighbour	->	Alive

    Args:
        field_cell (FieldCell): Cell that should be processed
    """
    field_cell.state = CellState.ALIVE
    log.debug('2 or 3 Alive: Cell (%d, %d) make_alive',
              field_cell.row, field_cell.column)


def _rule_alive_from_4_to_8(field_cell: Cell) -> None:
    """Change Statte of the Cell.

    Alive	->	4-8 Alive Neighbour	->	Dead

    Args:
        field_cell (FieldCell): Cell that should be processed
    """
    field_cell.state = CellState.DEAD
    log.debug('3 or more 4, 5, 6, 7, 8 Alive: Cell (%d, %d) make_dead',
              field_cell.row, field_cell.column)


def _rule_dead_equal_to_3(field_cell: Cell) -> None:
    """Change Statte of the Cell.

    Dead	->	==3 Alive Neighbour	->	Alive

    Args:
        field_cell (FieldCell): Cell that should be processed
    """
    field_cell.state = CellState.ALIVE
    log.debug('alive neighbours = 3: Cell (%d, %d) make_alive',
              field_cell.row, field_cell.column)


def _apply_rules_to_alive_cell(field_cell: Cell) -> None:
    """Process rules related to the only Alive cell.

    Alive	->	0-1 Alive Neighbour	->	Dead
    Alive	->	2-3 Alive Neighbour	->	Alive
    Alive	->	4-8 Alive Neighbour	->	Dead

    Args:
        field_cell (FieldCell): Cell that should be processed
    """
    log.debug('In _apply_rules_to_alive_cell')
    if field_cell.neighbours in [0, 1]:  # 0 or 1
        _rule_alive_from_0_to_1(field_cell)
    elif (field_cell.neighbours in [2, 3]
          and field_cell.neighbours <= 3):  # 2 or 3
        _rule_alive_from_2_to_3(field_cell)
    elif field_cell.neighbours > 3:  # 3 or more 4, 5, 6, 7, 8
        _rule_alive_from_4_to_8(field_cell)
    log.debug('Out _apply_rules_to_alive_cell')


def _apply_rules_to_dead_cell(field_cell: Cell) -> None:
    """Process rules related to the only Dead cell.

    Dead	->	==3 Alive Neighbour	->	Alive
    Args:
        field_cell (FieldCell): Cell that should be processed
    """
    log.debug('In _apply_rules_to_dead_cell')
    if field_cell.neighbours == 3:
        _rule_dead_equal_to_3(field_cell)
    log.debug('Out _apply_rules_to_dead_cell')


def apply_rules_and_change_state(field_cell: Cell) -> None:
    """Process cell state based on the rules of game.

    Rules:
    Alive	->	0-1 Alive Neighbour	->	Dead
    Alive	->	2-3 Alive Neighbour	->	Alive
    Alive	->	4-8 Alive Neighbour	->	Dead
    Dead	->	==3 Alive Neighbour	->	Alive

    Args:
        field_cell (FieldCell): Cell that should be processed
    """
    log.debug('In apply_rules_and_change_state')
    state_processors = {
        CellState.ALIVE: _apply_rules_to_alive_cell,
        CellState.DEAD: _apply_rules_to_dead_cell,
    }
    state_processors[field_cell.state](field_cell)
    log.debug('Out apply_rules_and_change_state')
