import unittest
import unittest.mock as mock
import os
from gameoflifeapi.core.classes.game_enums import GameLifeCellState

from gameoflifeapi.core.tools.console_tools import print_game_state
from gameoflifeapi.core.classes.game_cell import GameLifeCell


class TestConsoleTools(unittest.TestCase):

    @mock.patch('builtins.print')
    @mock.patch('os.system')
    def test_print_game_state(self, os_system: mock.Mock,
                              mock_print: mock.Mock) -> None:
        game_field = [
            [GameLifeCell(0, 0), GameLifeCell(0, 1), GameLifeCell(0, 2)],
            [GameLifeCell(1, 0), GameLifeCell(
                1, 1, GameLifeCellState.ALIVE), GameLifeCell(1, 2)],
            [GameLifeCell(2, 0), GameLifeCell(2, 1), GameLifeCell(2, 2)]
        ]

        print_game_state(game_field)

        os_system.assert_called_once_with('clear')
        mock_print.assert_called()
        mock_print.assert_called_with(
            '_________________________________________________________')
        mock_print.assert_any_call('| |', end='')
        mock_print.assert_any_call('|*|', end='')
        mock_print.assert_any_call()
