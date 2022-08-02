import unittest
from gameoflifeapi.core.classes.game_life import GameLife
from gameoflifeapi.core.classes.game_cell import GameLifeCell
from gameoflifeapi.core.classes.game_enums import GameLifeCellState


class TestGameLife(unittest.TestCase):

    def test_initialization_of_functionality(self) -> None:
        game_life = GameLife()
        self.assertIsNotNone(game_life)
        self.assertEqual(10, game_life.rows)
        self.assertEqual(10, game_life.cols)
        self.assertEqual(10, len(game_life._game_field))
        self.assertEqual(10, len(game_life._game_field[0]))
        self.assertEqual(0, game_life.generation)

        game_life = GameLife(number_of_rows=4, number_of_cells=5)
        self.assertIsNotNone(game_life)
        self.assertEqual(4, game_life.rows)
        self.assertEqual(5, game_life.cols)
        self.assertEqual(4, len(game_life._game_field))
        self.assertEqual(5, len(game_life._game_field[0]))
        self.assertEqual(0, game_life.generation)

    def test_init_game_field(self) -> None:
        game_life = GameLife()
        for row in game_life.field:
            for cell in row:
                self.assertEqual(GameLifeCellState.DEAD, cell.state,
                                 f'Cell with coordinates row:{cell.row}, col:{cell.col} should be dead after initialization')

    def test_change_cell_state(self) -> None:
        game_life = GameLife()
        game_life._change_cell_state(
            [(0, 0), (5, 5), (9, 9)], GameLifeCellState.ALIVE)
        self.assertEqual(GameLifeCellState.ALIVE, game_life.field[0][0].state)
        self.assertEqual(GameLifeCellState.ALIVE, game_life.field[5][5].state)
        self.assertEqual(GameLifeCellState.ALIVE, game_life.field[9][9].state)

    def test_count_amount_alive_neighbour(self) -> None:
        game_life = GameLife()
        game_life.set_alive_cells([(0, 0), (0, 1), (1, 0)])
        value = game_life._count_amount_alive_neighbour(1, 1)
        self.assertEqual(3, value)

        game_life = GameLife()
        game_life.set_alive_cells([(5, 5)])
        value = game_life._count_amount_alive_neighbour(4, 5)
        self.assertEqual(1, value)

        game_life = GameLife()
        game_life.set_alive_cells([(0, 0), (0, 1), (0, 2),
                                   (1, 0), (1, 1), (1, 2),
                                   (2, 0), (2, 1), (2, 2)
                                   ])
        value = game_life._count_amount_alive_neighbour(1, 1)
        self.assertEqual(8, value)
        value = game_life._count_amount_alive_neighbour(9, 9)
        self.assertEqual(0, value)

    def test_apply_rules_and_change_state(self) -> None:
        game_life = GameLife()
        game_cell = GameLifeCell(0, 0, GameLifeCellState.ALIVE)

        game_life._apply_rules_and_change_state(game_cell, 0)
        self.assertEqual(GameLifeCellState.DEAD, game_cell.state)

        game_life._apply_rules_and_change_state(game_cell, 3)
        self.assertEqual(GameLifeCellState.ALIVE, game_cell.state)

    def test_apply_rules_to_alive_cell(self) -> None:
        game_life = GameLife()
        game_cell = GameLifeCell(0, 0, GameLifeCellState.ALIVE)

        game_cell.change_state(GameLifeCellState.ALIVE)
        game_life._apply_rules_to_alive_cell(game_cell, 0)
        self.assertEqual(GameLifeCellState.DEAD, game_cell.state)

        game_cell.change_state(GameLifeCellState.ALIVE)
        game_life._apply_rules_to_alive_cell(game_cell, 1)
        self.assertEqual(GameLifeCellState.DEAD, game_cell.state)

        game_cell.change_state(GameLifeCellState.ALIVE)
        game_life._apply_rules_to_alive_cell(game_cell, 2)
        self.assertEqual(GameLifeCellState.ALIVE, game_cell.state)

        game_cell.change_state(GameLifeCellState.ALIVE)
        game_life._apply_rules_to_alive_cell(game_cell, 3)
        self.assertEqual(GameLifeCellState.ALIVE, game_cell.state)

        game_cell.change_state(GameLifeCellState.ALIVE)
        game_life._apply_rules_to_alive_cell(game_cell, 4)
        self.assertEqual(GameLifeCellState.DEAD, game_cell.state)

        game_cell.change_state(GameLifeCellState.ALIVE)
        game_life._apply_rules_to_alive_cell(game_cell, 8)
        self.assertEqual(GameLifeCellState.DEAD, game_cell.state)

    def test_apply_rules_to_dead_cell(self) -> None:
        game_life = GameLife()
        game_cell = GameLifeCell(0, 0, GameLifeCellState.DEAD)

        game_cell.change_state(GameLifeCellState.DEAD)
        game_life._apply_rules_to_dead_cell(game_cell, 0)
        self.assertEqual(GameLifeCellState.DEAD, game_cell.state)

        game_cell.change_state(GameLifeCellState.DEAD)
        game_life._apply_rules_to_dead_cell(game_cell, 8)
        self.assertEqual(GameLifeCellState.DEAD, game_cell.state)

        game_cell.change_state(GameLifeCellState.DEAD)
        game_life._apply_rules_to_dead_cell(game_cell, 4)
        self.assertEqual(GameLifeCellState.DEAD, game_cell.state)

        game_cell.change_state(GameLifeCellState.ALIVE)
        game_life._apply_rules_to_dead_cell(game_cell, 3)
        self.assertEqual(GameLifeCellState.ALIVE, game_cell.state)

    def test_field_property_get(self) -> None:
        game_life = GameLife(3, 3)
        self.assertEqual(3, len(game_life.field))
        self.assertEqual(3, len(game_life.field[0]))

    def test_field_property_set(self) -> None:
        game_life = GameLife(3, 3)
        with self.assertRaises(AttributeError):
            game_life.field = []

    def test_rows_property_get(self) -> None:
        game_life = GameLife(3, 4)
        self.assertEqual(3, game_life.rows)

    def test_rows_property_set(self) -> None:
        game_life = GameLife(3, 3)
        with self.assertRaises(AttributeError):
            game_life.rows = 10

    def test_cols_property_get(self) -> None:
        game_life = GameLife(3, 4)
        self.assertEqual(4, game_life.cols)

    def test_cols_property_set(self) -> None:
        game_life = GameLife(3, 3)
        with self.assertRaises(AttributeError):
            game_life.cols = 10

    def test_game_life_generation_property_get(self) -> None:
        game_life = GameLife(3, 4)
        self.assertEqual(0, game_life.generation)

        game_life.create_new_generation()
        self.assertEqual(1, game_life.generation)

        game_life.create_new_generation()
        self.assertEqual(2, game_life.generation)

    def test_game_life_generation_property_set(self) -> None:
        game_life = GameLife(3, 3)
        with self.assertRaises(AttributeError):
            game_life.generation = 10

    def test_previous_field_property_get(self) -> None:
        game_life = GameLife(3, 3)
        self.assertEqual(3, len(game_life.previous_field))
        self.assertEqual(3, len(game_life.previous_field[0]))

    def test_previous_field_property_set(self) -> None:
        game_life = GameLife(3, 3)
        with self.assertRaises(AttributeError):
            game_life.previous_field = []

    def test_set_alive_cells(self) -> None:
        game_life = GameLife()

        game_life.set_alive_cells([(0, 0), (9, 5)])
        self.assertEqual(GameLifeCellState.ALIVE, game_life.field[0][0].state)
        self.assertEqual(GameLifeCellState.ALIVE, game_life.field[9][5].state)

    def test_set_dead_cells(self) -> None:
        game_life = GameLife()
        for row in game_life._game_field:
            for cell in row:
                cell.change_state(GameLifeCellState.ALIVE)
        self.assertEqual(GameLifeCellState.ALIVE, game_life.field[1][1].state)
        self.assertEqual(GameLifeCellState.ALIVE, game_life.field[3][9].state)

        game_life.set_dead_cells([(1, 1), (3, 9)])
        self.assertEqual(GameLifeCellState.DEAD, game_life.field[1][1].state)
        self.assertEqual(GameLifeCellState.DEAD, game_life.field[3][9].state)

    def test_create_new_generation(self) -> None:
        game_life = GameLife(4, 5)
        self.assertEqual(0, game_life.generation)

        game_life.set_alive_cells([(0, 0), (0, 1), (0, 2)])
        game_life.create_new_generation()
        self.assertEqual(1, game_life.generation)
        self.assertEqual(GameLifeCellState.DEAD, game_life.field[0][0].state)
        self.assertEqual(GameLifeCellState.DEAD, game_life.field[0][1].state)
        self.assertEqual(GameLifeCellState.DEAD, game_life.field[0][2].state)

        game_life.set_alive_cells([(0, 0), (0, 1), (0, 2),
                                   (1, 0), (1, 1),
                                   (2, 1)
                                   ])
        game_life.create_new_generation()
        self.assertEqual(GameLifeCellState.ALIVE, game_life.field[0][0].state)
        self.assertEqual(GameLifeCellState.DEAD, game_life.field[0][1].state)
        self.assertEqual(GameLifeCellState.DEAD, game_life.field[0][2].state)
        self.assertEqual(GameLifeCellState.ALIVE, game_life.field[1][0].state)
        self.assertEqual(GameLifeCellState.ALIVE, game_life.field[1][1].state)
        self.assertEqual(GameLifeCellState.ALIVE, game_life.field[2][0].state)
        self.assertEqual(2, game_life.generation)

    def test_is_the_final_generation(self) -> None:
        game_life = GameLife(5, 5)
        game_life.set_alive_cells([(0, 0), (0, 1), (0, 2), (1, 1)])
        game_life.create_new_generation()
        game_life.create_new_generation()
        game_life.create_new_generation()
        self.assertTrue(game_life.is_the_final_generation())
