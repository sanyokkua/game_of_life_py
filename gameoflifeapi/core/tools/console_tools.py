"""Module contains tools required for console version of the game."""
import os

from gameoflifeapi.core.classes.game_cell import GameLifeCell
from gameoflifeapi.core.classes.game_enums import GameLifeCellState


def print_game_state(game_field: list[list[GameLifeCell]]) -> None:
    """Generate view for the Game Field.

    Args:
        game_field (list[list[GameLifeCell]]): Game Field
    """
    os.system('clear')

    print('_________________________________________________________')
    for row in game_field:
        for col in row:
            symb = '|*|' if col.state == GameLifeCellState.ALIVE else '| |'
            print(symb, end='')
        print()
    print('_________________________________________________________')
