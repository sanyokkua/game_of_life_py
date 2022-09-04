"""Module contains QFieldButtonCell class."""
import logging

from PyQt6.QtWidgets import QPushButton, QSizePolicy, QWidget

from gameoflifeapi.logic.data.cell import Cell
from gameoflifeapi.logic.data.state import CellState

log: logging.Logger = logging.getLogger(__name__)

_STYLE_BORDER: str = 'border: 1px solid black;'
_STYLE_GREEN: str = 'background-color: #7FFF00;'
_STYLE_GRAY: str = 'background-color: #F0FFFF;'


class QFieldButtonCell(QPushButton):
    """Custom button to represent Field Cell.

    Args:
        QPushButton (_type_): parent class.
    """

    def __init__(self, parent: QWidget, cell: Cell) -> None:
        """Initialize button."""
        QPushButton.__init__(self, parent)
        self._cell: Cell = cell
        size_policy: QSizePolicy = QSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
        size_policy.setHeightForWidth(True)
        size_policy.setWidthForHeight(True)
        self.setSizePolicy(size_policy)
        self.setMinimumSize(10, 10)
        self.update_button_state()

    def _apply_style(self, color: str):
        style: str = ' '.join([color, _STYLE_BORDER])
        self.setStyleSheet(style)

    def _apply_style_gray(self):
        self._apply_style(_STYLE_GRAY)

    def _apply_style_green(self):
        self._apply_style(_STYLE_GREEN)

    def update_button_state(self):
        """Calculate and update button color."""
        if self._cell.state is CellState.ALIVE:
            self._apply_style_green()
        else:
            self._apply_style_gray()

    @property
    def cell(self) -> Cell:
        """Return cell related to the current button."""
        return self._cell
