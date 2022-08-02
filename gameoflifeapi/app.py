"""Module represents Console Version of the Game"""

from gameoflifeapi.core.api.abstract.definitions import AbstractPersistance
from gameoflifeapi.core.api.controller import GameLifeController
from gameoflifeapi.core.api.persistance import GameLifePicklePersistance
from gameoflifeapi.core.classes.game_enums import GameLifeCellState
from gameoflifeapi.core.tools.console_tools import print_game_state

import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')


def main():
    rows: int = int(input('Type number of the ROWS:\t'))
    cols: int = int(input('Type number of the COLUMNS:\t'))

    game_persistance: AbstractPersistance = GameLifePicklePersistance()
    game_controller: GameLifeController = GameLifeController(game_persistance)
    game_controller.start_new_game(rows, cols)

    option: str = input(
        'If you want random state - type rand, or will be manual creation of the initial state: ')

    if option == 'rand':
        game_controller.make_random_cell_states()
    else:
        initial_state: list[tuple[int, int]] = []
        while True:
            print_game_state(game_controller.game_field)
            print(initial_state)
            print('Type Coordinates:')
            row: int = int(input('Type ROW: '))
            col: int = int(input('Type COLUMNS: '))
            initial_state.append((row, col))
            to_exit: str = input(
                'Type exit to finish creating initial state or just press enter to continue: ')
            if to_exit == 'exit':
                break
        game_controller.edit_current_field_state(initial_state,
                                                 GameLifeCellState.ALIVE)

    while True:
        print_game_state(game_controller.game_field)
        to_exit: str = input(
            'Type exit to finish or just press enter to continue: ')
        if to_exit == 'exit':
            break
        game_controller.increment_generation()


main()
