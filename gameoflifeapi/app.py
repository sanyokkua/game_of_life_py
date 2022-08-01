import enum
import os
import time


class GameLifeCellState(enum.Enum):
    ALIVE = 0
    DEAD = 1


class GameLifeCell:

    def __init__(self, row: int, col: int,
                 state: GameLifeCellState = GameLifeCellState.DEAD) -> None:
        self._row: int = row
        self._col: int = col
        self._state: GameLifeCellState = state

    def change_state(self, state: GameLifeCellState) -> None:
        self._state = state

    def make_alive(self) -> None:
        self.change_state(GameLifeCellState.ALIVE)

    def make_dead(self) -> None:
        self.change_state(GameLifeCellState.DEAD)

    @property
    def row(self) -> int:
        return self._row

    @property
    def col(self) -> int:
        return self._col

    @property
    def state(self) -> GameLifeCellState:
        return self._state


class GameLife:
    def __init__(self, number_of_rows: int, number_of_cells: int) -> None:
        self._field: list[list[GameLifeCell]] = []
        self._number_of_rows: int = number_of_rows
        self._number_of_cells: int = number_of_cells
        self._life_increment: int = 0
        self._init_field()

    def _init_field(self) -> None:
        row_counter: int = 0
        while row_counter < self._number_of_rows:
            col_counter: int = 0
            field_row: list[GameLifeCell] = []
            while col_counter < self._number_of_cells:
                field_row.append(GameLifeCell(
                    row=row_counter, col=col_counter))
                col_counter += 1
            self._field.append(field_row)
            row_counter += 1

    @property
    def field(self) -> list[list[GameLifeCell]]:
        return self._field

    @property
    def rows(self) -> int:
        return len(self._field)

    @property
    def cols(self) -> int:
        try:
            return len(self._field[0])
        except IndexError:
            return 0

    @property
    def life_increment(self) -> int:
        return self._life_increment

    def set_game_state(self, state_field: list[GameLifeCell]) -> None:
        rows = range(self.rows)
        cols = range(self.cols)
        for game_cell in state_field:
            current_row: int = game_cell.row
            current_col: int = game_cell.col
            if current_row in rows and current_col in cols:
                self._field[current_row][current_col].change_state(
                    game_cell.state)
            else:
                raise Exception('Incorrect coordinates')

    def increment_state(self) -> None:
        for row in self.field:
            for col in row:
                alive_neighbours = self._cont_alive_neighbour(col.row, col.col)
                self._apply_rules_and_change_state(col, alive_neighbours)
        self._life_increment += 1
        print(f'increment = {self.life_increment}')

    def _cont_alive_neighbour(self, cell_row: int, cell_col: int) -> int:
        rows = range(self.rows)
        cols = range(self.cols)
        # -1 -1    -1 0     -1 +1
        #  0 -1     0 0      0 +1
        # +1 -1    +1 0     +1 +1
        coordinates_diff = (
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        )
        number_of_alive = 0
        for (x_row, x_col) in coordinates_diff:
            row_to_check = cell_row + x_row
            col_to_check = cell_col + x_col
            if row_to_check in rows and col_to_check in cols:
                game_cell = self.field[row_to_check][col_to_check]
                state = game_cell.state
                if state is GameLifeCellState.ALIVE:
                    number_of_alive += 1
        return number_of_alive

    def _apply_rules_and_change_state(self, cell: GameLifeCell, number_of_alive_neighbours: int) -> None:
        if cell.state is GameLifeCellState.ALIVE and number_of_alive_neighbours < 2:
            cell.make_dead()
        elif cell.state is GameLifeCellState.ALIVE and number_of_alive_neighbours > 2 and number_of_alive_neighbours < 4:
            cell.make_alive()
        elif cell.state is GameLifeCellState.ALIVE and number_of_alive_neighbours > 3:
            cell.make_dead()
        elif cell.state is GameLifeCellState.DEAD and number_of_alive_neighbours == 3:
            cell.make_alive()
        else:
            pass


def print_matrix(matrix: list[list[GameLifeCell]]):
    time.sleep(1)
    os.system('clear')
    for row in matrix:
        for col in row:
            symb = '|*|' if col.state == GameLifeCellState.ALIVE else '|_|'
            print(symb, end='')
        print()
    print('_________________________________________________________-')


def main():
    game = GameLife(15, 15)
    print_matrix(game.field)
    game.set_game_state([
        GameLifeCell(0, 0, GameLifeCellState.ALIVE),
        GameLifeCell(1, 1, GameLifeCellState.ALIVE),
        GameLifeCell(2, 1, GameLifeCellState.ALIVE),
        GameLifeCell(3, 2, GameLifeCellState.ALIVE),
        GameLifeCell(1, 0, GameLifeCellState.ALIVE),
        GameLifeCell(0, 2, GameLifeCellState.ALIVE),
        GameLifeCell(1, 3, GameLifeCellState.ALIVE),
        GameLifeCell(4, 12, GameLifeCellState.ALIVE),
        GameLifeCell(4, 10, GameLifeCellState.ALIVE),
        GameLifeCell(4, 11, GameLifeCellState.ALIVE),
        GameLifeCell(8, 9, GameLifeCellState.ALIVE),
        GameLifeCell(8, 8, GameLifeCellState.ALIVE),
        GameLifeCell(8, 1, GameLifeCellState.ALIVE),
        GameLifeCell(5, 5, GameLifeCellState.ALIVE),
        GameLifeCell(5, 2, GameLifeCellState.ALIVE)
    ])
    print_matrix(game.field)
    game.increment_state()
    print_matrix(game.field)
    game.increment_state()
    print_matrix(game.field)
    game.increment_state()
    print_matrix(game.field)
    game.increment_state()
    print_matrix(game.field)
    game.increment_state()
    print_matrix(game.field)
    game.increment_state()
    print_matrix(game.field)
    game.increment_state()
    print_matrix(game.field)
    game.increment_state()
    print_matrix(game.field)
    game.increment_state()
    print_matrix(game.field)
    game.increment_state()
    print_matrix(game.field)
    game.increment_state()
    print_matrix(game.field)
    game.increment_state()
    print_matrix(game.field)
    game.increment_state()
    print_matrix(game.field)
    game.increment_state()
    print_matrix(game.field)
    game.increment_state()
    print_matrix(game.field)
    game.increment_state()
    print_matrix(game.field)
    game.increment_state()
    print_matrix(game.field)


main()
