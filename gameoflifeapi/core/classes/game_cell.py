"""Definition of Cell used by Game."""
import logging
from beartype import beartype
from gameoflifeapi.core.classes.game_enums import GameLifeCellState

log: logging.Logger = logging.getLogger(__name__)


class GameLifeCell:
    """Represent Game Cell and its position and state."""

    @beartype
    def __init__(self, row: int, col: int,
                 state: GameLifeCellState = GameLifeCellState.DEAD) -> None:
        """Initialize Game Cell.

        Args:
            row (int): Number of Row
            col (int): Number of Column
            state (GameLifeCellState, optional): Cell State.
                Defaults to GameLifeCellState.DEAD.
        """
        self._row: int = row
        self._col: int = col
        self._state: GameLifeCellState = state
        log.info('GameLifeCell is initialized, row: %d, col:%d, state: %s',
                 self._row, self._col, self._state)

    @property
    def row(self) -> int:
        """Define ROW property with readonly access.

        Returns:
            int: ROW number
        """
        log.debug('row property was called. Returned: %d', self._row)
        return self._row

    @property
    def col(self) -> int:
        """Define COLUMN property with readonly access.

        Returns:
            int: COLUMN number
        """
        log.debug('col property was called. Returned: %d', self._col)
        return self._col

    @property
    def state(self) -> GameLifeCellState:
        """Define STATE property with readonly access.

        Returns:
            GameLifeCellState: Current Cell State
        """
        log.debug('state property was called. Returned: %s', self._state)
        return self._state

    @beartype
    def change_state(self, state: GameLifeCellState) -> None:
        """Change cell state to passed as parameter.

        Args:
            state (GameLifeCellState): Game State
        """
        log.debug('change_state: state: %s', state)
        self._state = state

    @beartype
    def make_alive(self) -> None:
        """Change Cell State to ALIVE."""
        self.change_state(GameLifeCellState.ALIVE)
        log.debug('make_alive')

    @beartype
    def make_dead(self) -> None:
        """Change Cell State to DEAD."""
        self.change_state(GameLifeCellState.DEAD)
        log.debug('make_dead')

    @beartype
    def __repr__(self) -> str:
        """Override of the default repr function.

        Returns:
            str: String representation of the class
        """
        return f'{self.row},{self.col},{self.state}'
