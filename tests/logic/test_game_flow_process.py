"""Tests for covering game flow process class."""
import unittest

from gameoflifeapi.logic.data.field import Field
from gameoflifeapi.logic.data.state import CellState
from gameoflifeapi.logic.exceptions import GenerationValueException
from gameoflifeapi.logic.game_flow_process import GameFlowProcess


def _on_generation_created_stub() -> None:
    """Make stub or executions."""
    print('STUB')


class TestGameFlowProcess(unittest.TestCase):
    """Tests for covering game flow process class functionality."""

    def test_creation_of_game_flow_process(self) -> None:
        """Test creation of the Game Flow."""
        field = Field()
        game = GameFlowProcess(
            rows=10,
            columns=10,
            generation=0,
            game_field=field,
            on_generation_created=_on_generation_created_stub
        )

        self.assertEqual(10, game.game_field.rows)
        self.assertEqual(10, game.game_field.columns)
        self.assertEqual(0, game.generation)
        self.assertEqual(field, game.game_field)

    def test_validation_of_game_flow_creation(self) -> None:
        """Test validation of parameters during creation of the Game Flow."""
        field = Field()

        with self.assertRaises(GenerationValueException):
            GameFlowProcess(10, 10, -10, field, _on_generation_created_stub)

    def test_game_flow_process_property_game_field(self) -> None:
        """Test Game Flow property game_field readonly."""
        game = GameFlowProcess()

        with self.assertRaises(AttributeError):
            game.game_field = None

    def test_game_flow_process_property_generation(self) -> None:
        """Test Game Flow property generation readonly."""
        game = GameFlowProcess()

        with self.assertRaises(AttributeError):
            game.generation = 10

    def test_creation_of_game_flow_process_defaults(self) -> None:
        """Test creation of the GameFlow with default values."""
        game = GameFlowProcess()

        self.assertIsNotNone(game.game_field)
        self.assertIsNotNone(game._on_generation_created)
        self.assertEqual(10, game.game_field.rows)
        self.assertEqual(10, game.game_field.columns)
        self.assertEqual(0, game.generation)

    def test_switch_cell_state(self) -> None:
        """Test Game Flow switch state functionality."""
        game = GameFlowProcess()
        game.switch_cell_state(0, 1)
        game.switch_cell_state(1, 0)
        game.switch_cell_state(1, 1)

        self.assertEqual(CellState.ALIVE, game.game_field.all_cells[(0, 1)].state)
        self.assertEqual(CellState.ALIVE, game.game_field.all_cells[(1, 1)].state)
        self.assertEqual(CellState.ALIVE, game.game_field.all_cells[(1, 1)].state)

        game.switch_cell_state(0, 1)
        game.switch_cell_state(1, 0)
        game.switch_cell_state(1, 1)

        self.assertEqual(CellState.DEAD, game.game_field.all_cells[(0, 1)].state)
        self.assertEqual(CellState.DEAD, game.game_field.all_cells[(1, 1)].state)
        self.assertEqual(CellState.DEAD, game.game_field.all_cells[(1, 1)].state)

    def test_create_next_generation(self) -> None:
        """Test creation of the new generation."""
        game = GameFlowProcess()

        self.assertEqual(0, game.generation)

        #   0  1  2  3  4  5  6  7  8  9
        # 0 *  *  *  -  -  -  -  -  -  -
        # 1 -  -  -  -  -  -  -  -  -  -
        # 2 -  -  -  -  -  -  -  -  -  -
        # 3 -  -  -  -  -  -  -  -  -  -
        # 4 -  -  -  -  -  -  -  -  -  -
        # 5 -  -  -  -  -  -  -  -  -  -
        # 6 -  -  -  -  -  -  -  -  -  -
        # 7 -  -  -  -  -  -  -  -  -  -
        # 8 -  -  -  -  -  -  -  -  -  -
        # 9 -  -  -  -  -  -  -  -  -  -
        game.switch_cell_state(0, 0)  # 3N, 1Alive
        game.switch_cell_state(0, 1)  # 5N, 2Alive
        game.switch_cell_state(0, 2)  # 5N, 1Alive

        game._count_neighbours_for_field()
        game.create_next_generation()

        self.assertEqual(1, game.generation)
        self.assertEqual(CellState.DEAD, game.game_field.all_cells[(0, 0)].state)
        self.assertEqual(CellState.ALIVE, game.game_field.all_cells[(0, 1)].state)
        self.assertEqual(CellState.DEAD, game.game_field.all_cells[(0, 2)].state)

        game = GameFlowProcess()
        #   0  1  2  3  4  5  6  7  8  9
        # 0 *  *  *  -  -  -  -  -  -  -
        # 1 *  *  -  -  -  -  -  -  -  -
        # 2 -  *  -  -  -  -  -  -  -  -
        # 3 -  -  -  -  -  -  -  -  -  -
        # 4 -  -  -  -  -  -  -  -  -  -
        # 5 -  -  -  -  -  -  -  -  -  -
        # 6 -  -  -  -  -  -  -  -  -  -
        # 7 -  -  -  -  -  -  -  -  -  -
        # 8 -  -  -  -  -  -  -  -  -  -
        # 9 -  -  -  -  -  -  -  -  -  -
        game.switch_cell_state(0, 0)
        game.switch_cell_state(0, 1)
        game.switch_cell_state(0, 2)
        game.switch_cell_state(1, 0)
        game.switch_cell_state(1, 1)
        game.switch_cell_state(2, 1)
        game._count_neighbours_for_field()
        game.create_next_generation()

        self.assertEqual(CellState.ALIVE, game.game_field.all_cells[(0, 0)].state)
        self.assertEqual(CellState.DEAD,  game.game_field.all_cells[(0, 1)].state)
        self.assertEqual(CellState.ALIVE,  game.game_field.all_cells[(0, 2)].state)
        self.assertEqual(CellState.DEAD, game.game_field.all_cells[(1, 0)].state)
        self.assertEqual(CellState.DEAD, game.game_field.all_cells[(1, 1)].state)
        self.assertEqual(CellState.ALIVE, game.game_field.all_cells[(2, 1)].state)
        self.assertEqual(CellState.ALIVE, game.game_field.all_cells[(2, 0)].state)
        self.assertEqual(1, game.generation)

    def test_randomize_next_generation(self) -> None:
        """Test Game Flow randomize functionality."""
        game_1 = GameFlowProcess()
        game_1.randomize_next_generation()
        count_1 = 0
        for (_coordinates, cell) in game_1.game_field.all_cells.items():
            if cell.state is CellState.ALIVE:
                count_1 += 1
        self.assertGreater(count_1, 0)

    def test__count_neighbours_for_field(self) -> None:
        """Test counting of neighbours for whole field.

          0  1  2  3  4  5  6  7  8  9
        0 *  *  *  -  -  -  -  -  -  -
        1 -  *  -  -  -  -  -  -  -  -
        2 -  *  -  -  -  -  -  -  -  -
        3 -  -  -  -  -  -  -  -  -  -
        4 -  -  -  -  -  -  -  -  -  -
        5 -  -  -  -  -  -  -  -  -  -
        6 -  -  -  -  -  -  -  -  -  -
        7 -  -  -  -  -  -  -  -  -  -
        8 -  -  -  -  -  -  -  -  -  -
        9 -  -  -  -  -  -  -  -  -  -
        """
        game = GameFlowProcess()

        self.assertEqual(0, game.generation)

        game.switch_cell_state(0, 0)
        game.switch_cell_state(0, 1)
        game.switch_cell_state(0, 2)
        game.switch_cell_state(1, 1)
        game.switch_cell_state(2, 1)

        game._count_neighbours_for_field()

        self.assertEqual(2, game.game_field.all_cells[(0, 0)].neighbours)
        self.assertEqual(3, game.game_field.all_cells[(0, 1)].neighbours)
        self.assertEqual(2, game.game_field.all_cells[(0, 2)].neighbours)
        self.assertEqual(4, game.game_field.all_cells[(1, 1)].neighbours)
        self.assertEqual(1, game.game_field.all_cells[(2, 1)].neighbours)

    def test__count_neighbours_for_cell(self) -> None:
        """Test counting of neighbours for field.

          0  1  2  3  4  5  6  7  8  9
        0 *  *  *  -  -  -  -  -  -  -
        1 *  *  -  -  -  -  -  -  -  -
        2 -  *  -  -  -  -  -  -  -  -
        3 -  -  -  -  -  -  -  -  -  -
        4 -  -  -  -  -  -  -  -  -  -
        5 -  -  -  -  -  -  -  -  -  -
        6 -  -  -  -  -  -  -  -  -  -
        7 -  -  -  -  -  -  -  -  -  -
        8 -  -  -  -  -  -  -  -  -  -
        9 -  -  -  -  -  -  -  -  -  -
        """
        game = GameFlowProcess()

        self.assertEqual(0, game.generation)

        game.switch_cell_state(0, 0)
        game.switch_cell_state(0, 1)
        game.switch_cell_state(0, 2)
        game.switch_cell_state(1, 0)
        game.switch_cell_state(1, 1)
        game.switch_cell_state(2, 1)
        game._count_neighbours_for_cell(game.game_field.all_cells[(1, 1)])

        self.assertEqual(5, game.game_field.all_cells[(1, 1)].neighbours)

    def test__get_neighbour_cells(self) -> None:
        """Test creating neighbours list."""
        game = GameFlowProcess()

        #   0  1  2  3  4  5  6  7  8  9 | C -> Cell, N -> Neighboud, D - Not Neighbour
        # 0 C  N  -  -  -  -  -  -  -  -
        # 1 N  N  -  -  -  -  -  -  -  -
        # 2 -  -  -  -  -  -  -  -  -  -
        # 3 -  -  -  -  -  -  -  -  -  -
        # 4 -  -  -  -  -  -  -  -  -  -
        # 5 -  -  -  -  -  -  -  -  -  -
        # 6 -  -  -  -  -  -  -  -  -  -
        # 7 -  -  -  -  -  -  -  -  -  -
        # 8 -  -  -  -  -  -  -  -  -  -
        # 9 -  -  -  -  -  -  -  -  -  -
        res_0_0 = game._get_neighbour_cells(0, 0)
        self.assertEqual(3, len(res_0_0))
        self.assertTrue((0, 1) in res_0_0.keys())
        self.assertTrue((1, 1) in res_0_0.keys())
        self.assertTrue((1, 0) in res_0_0.keys())
        self.assertFalse((0, 2) in res_0_0.keys())
        self.assertFalse((0, 0) in res_0_0.keys())
        self.assertFalse((2, 0) in res_0_0.keys())

        #   0  1  2  3  4  5  6  7  8  9 | C -> Cell, N -> Neighboud, D - Not Neighbour
        # 0 -  -  -  -  -  -  -  -  -  -
        # 1 -  -  -  -  -  -  -  -  -  -
        # 2 -  -  -  -  -  -  -  -  -  -
        # 3 -  -  -  -  -  -  -  -  -  -
        # 4 -  -  -  -  -  -  -  -  -  -
        # 5 -  -  -  -  -  -  -  -  -  -
        # 6 -  -  -  -  -  -  -  -  -  -
        # 7 -  -  -  -  -  -  -  -  -  D
        # 8 -  -  -  -  -  -  -  -  N  N
        # 9 -  -  -  -  -  -  -  -  N  C
        res_9_9 = game._get_neighbour_cells(9, 9)
        self.assertEqual(3, len(res_9_9))
        self.assertTrue((8, 8) in res_9_9.keys())
        self.assertTrue((8, 9) in res_9_9.keys())
        self.assertTrue((9, 8) in res_9_9.keys())
        self.assertFalse((9, 9) in res_9_9.keys())
        self.assertFalse((7, 9) in res_9_9.keys())

        #   0  1  2  3  4  5  6  7  8  9 | C -> Cell, N -> Neighboud, D - Not Neighbour
        # 0 -  -  -  -  -  -  -  D  N  C
        # 1 -  -  -  -  -  -  -  -  N  N
        # 2 -  -  -  -  -  -  -  -  -  -
        # 3 -  -  -  -  -  -  -  -  -  -
        # 4 -  -  -  -  -  -  -  -  -  -
        # 5 -  -  -  -  -  -  -  -  -  -
        # 6 -  -  -  -  -  -  -  -  -  -
        # 7 -  -  -  -  -  -  -  -  -  -
        # 8 -  -  -  -  -  -  -  -  -  -
        # 9 -  -  -  -  -  -  -  -  -  -
        res_0_9 = game._get_neighbour_cells(0, 9)
        self.assertEqual(3, len(res_0_9))
        self.assertTrue((0, 8) in res_0_9.keys())
        self.assertTrue((1, 8) in res_0_9.keys())
        self.assertTrue((1, 9) in res_0_9.keys())
        self.assertFalse((0, 7) in res_0_9.keys())
        self.assertFalse((0, 9) in res_0_9.keys())

        #   0  1  2  3  4  5  6  7  8  9 | C -> Cell, N -> Neighboud, D - Not Neighbour
        # 0 -  -  -  -  -  -  -  -  -  -
        # 1 -  -  -  -  -  -  -  -  -  -
        # 2 -  -  -  -  -  -  -  -  -  -
        # 3 -  -  -  -  -  -  -  -  -  -
        # 4 -  -  -  -  -  -  -  -  -  -
        # 5 -  -  -  -  -  -  -  -  -  -
        # 6 -  -  -  -  -  -  -  -  -  -
        # 7 D  -  -  -  -  -  -  -  -  -
        # 8 N  N  -  -  -  -  -  -  -  -
        # 9 C  N  -  -  -  -  -  -  -  -
        res_9_0 = game._get_neighbour_cells(9, 0)
        self.assertEqual(3, len(res_9_0))
        self.assertTrue((8, 0) in res_9_0.keys())
        self.assertTrue((8, 1) in res_9_0.keys())
        self.assertTrue((9, 1) in res_9_0.keys())
        self.assertFalse((9, 0) in res_9_0.keys())
        self.assertFalse((7, 0) in res_9_0.keys())

        #   0  1  2  3  4  5  6  7  8  9 | C -> Cell, N -> Neighboud, D - Not Neighbour
        # 0 -  -  -  -  -  -  -  -  -  -
        # 1 -  -  -  -  -  -  -  -  -  -
        # 2 -  -  -  -  D  -  -  -  -  -
        # 3 -  -  -  N  N  N  -  -  -  -
        # 4 -  -  -  N  C  N  -  -  -  -
        # 5 -  -  -  N  N  N  -  -  -  -
        # 6 -  -  -  -  -  -  -  -  -  -
        # 7 -  -  -  -  -  -  -  -  -  -
        # 8 -  -  -  -  -  -  -  -  -  -
        # 9 -  -  -  -  -  -  -  -  -  -
        res_4_4 = game._get_neighbour_cells(4, 4)
        self.assertEqual(8, len(res_4_4))
        self.assertTrue((3, 3) in res_4_4.keys())
        self.assertTrue((3, 4) in res_4_4.keys())
        self.assertTrue((3, 5) in res_4_4.keys())
        self.assertTrue((4, 3) in res_4_4.keys())
        self.assertTrue((4, 5) in res_4_4.keys())
        self.assertTrue((5, 3) in res_4_4.keys())
        self.assertTrue((5, 4) in res_4_4.keys())
        self.assertTrue((5, 5) in res_4_4.keys())
        self.assertFalse((4, 4) in res_4_4.keys())
        self.assertFalse((2, 4) in res_4_4.keys())
