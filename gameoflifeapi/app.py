"""Module represents Console Version of the Game"""

from gameoflifeapi.core.classes.game_life import GameLife
from gameoflifeapi.core.tools.console_tools import print_game_state

import logging
import random

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')


def main():
    rows: int = int(input('Type number of the ROWS:\t'))
    cols: int = int(input('Type number of the COLUMNS:\t'))
    game: GameLife = GameLife(rows, cols)
    initial_state: list[tuple[int, int]] = []

    option: str = input(
        'If you want random state - type rand, or will be manual creation of the initial state:\t')

    if option == 'rand':
        number_of_iterations: int = random.randrange(5, rows * cols)
        while number_of_iterations > 0:
            random_row = random.randrange(0, rows)
            random_col: int = random.randrange(0, cols)
            initial_state.append((random_row, random_col))
            number_of_iterations -= 1
    else:
        while True:
            print_game_state(game.field)
            print(initial_state)
            print('Type Coordinates:')
            row: int = int(input('Type ROW:\t'))
            col: int = int(input('Type COLUMNS:\t'))
            initial_state.append((row, col))
            to_exit: str = input(
                'Type exit to finish creating initial state or just press enter to continue:\t')
            if to_exit == 'exit':
                break
            game.create_new_generation()
    game.set_alive_cells(initial_state)

    while True:
        print_game_state(game.field)
        to_exit: str = input(
            'Type exit to finish or just press enter to continue:\t')
        if to_exit == 'exit':
            break
        game.create_new_generation()


main()
