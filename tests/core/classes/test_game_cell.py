import unittest
from gameoflifeapi.core.classes.game_cell import GameLifeCell
from gameoflifeapi.core.classes.game_enums import GameLifeCellState


class TestGameCell(unittest.TestCase):

    def test_init_functionality(self) -> None:
        game_life_cell = GameLifeCell(3, 3)
        self.assertIsNotNone(game_life_cell)
        self.assertEqual(3, game_life_cell.row)
        self.assertEqual(3, game_life_cell.col)
        self.assertEqual(GameLifeCellState.DEAD, game_life_cell.state)

        game_life_cell = GameLifeCell(10, 10, GameLifeCellState.ALIVE)
        self.assertIsNotNone(game_life_cell)
        self.assertEqual(10, game_life_cell.row)
        self.assertEqual(10, game_life_cell.col)
        self.assertEqual(GameLifeCellState.ALIVE, game_life_cell.state)

    def test_row_property_get(self) -> None:
        game_life_cell = GameLifeCell(5, 5)
        self.assertEqual(5, game_life_cell.row)

    def test_row_property_set(self) -> None:
        game_life_cell = GameLifeCell(5, 5)
        with self.assertRaises(AttributeError):
            game_life_cell.row = 10

    def test_column_property_get(self) -> None:
        game_life_cell = GameLifeCell(5, 5)
        self.assertEqual(5, game_life_cell.col)

    def test_column_property_set(self) -> None:
        game_life_cell = GameLifeCell(5, 5)
        with self.assertRaises(AttributeError):
            game_life_cell.col = 10

    def test_state_property_get(self) -> None:
        game_life_cell = GameLifeCell(5, 5, GameLifeCellState.ALIVE)
        self.assertEqual(GameLifeCellState.ALIVE, game_life_cell.state)

    def test_state_property_set(self) -> None:
        game_life_cell = GameLifeCell(5, 5)
        with self.assertRaises(AttributeError):
            game_life_cell.state = GameLifeCellState.DEAD

    def test_change_state(self) -> None:
        game_life_cell = GameLifeCell(5, 5)
        game_life_cell.change_state(GameLifeCellState.ALIVE)
        self.assertEqual(GameLifeCellState.ALIVE, game_life_cell.state)

        game_life_cell.change_state(GameLifeCellState.DEAD)
        self.assertEqual(GameLifeCellState.DEAD, game_life_cell.state)

    def test_make_alive(self) -> None:
        game_life_cell = GameLifeCell(5, 5, GameLifeCellState.DEAD)
        game_life_cell.make_alive()
        self.assertEqual(GameLifeCellState.ALIVE, game_life_cell.state)

    def test_make_dead(self) -> None:
        game_life_cell = GameLifeCell(5, 5, GameLifeCellState.ALIVE)
        game_life_cell.make_dead()
        self.assertEqual(GameLifeCellState.DEAD, game_life_cell.state)
