"""Module represents Console Version of the Game."""
import logging
import os

from gameoflifeapi.api.abstract_definitions import (AbstractController,
                                                    AbstractPersistance)
from gameoflifeapi.api.game_controller import GameLifeController
from gameoflifeapi.api.persistance import GamePicklePersistance
from gameoflifeapi.logic.data.field import Field
from gameoflifeapi.logic.data.state import CellState

from .logic.data.dtos import NewGameDataDto

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')


def print_game_state(game_field: Field) -> None:
    """Generate view for the Game Field.

    Args:
        game_field (list[list[GameLifeCell]]): Game Field
    """
    os.system('clear')

    print('_________________________________________________________')
    rows = range(0, game_field.rows)
    cols = range(0, game_field.columns)
    field = game_field.all_cells
    for row in rows:
        for col in cols:
            cell = field[(row, col)]
            symb = '*|' if cell.state == CellState.ALIVE else ' |'
            print(symb, end='')
        print()
    print('_________________________________________________________')


def main():
    """Define entry point for the console game."""
    rows: int = int(input('Type number of the ROWS: '))
    cols: int = int(input('Type number of the COLUMNS: '))

    game_persistance: AbstractPersistance = GamePicklePersistance()
    game_controller: AbstractController = GameLifeController(game_persistance,
                                                             lambda: print())

    game_controller.start_new_game(NewGameDataDto(rows, cols, True))

    while True:
        print_game_state(game_controller.game_state.game_field)
        to_exit: str = input(
            'Type exit to finish or just press enter to continue: ')
        if to_exit == 'exit':
            break
        game_controller.increment_generation()


if __name__ == '__main__':
    main()
