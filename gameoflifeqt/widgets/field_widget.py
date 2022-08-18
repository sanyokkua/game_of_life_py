"""Represents game field."""
import logging

from PyQt6.QtGui import QColorConstants
from PyQt6.QtWidgets import QGridLayout, QPushButton, QSizePolicy, QWidget

from gameoflifeapi.api.game_controller import GameLifeController
from gameoflifeapi.logic.data.field import Field
from gameoflifeapi.logic.data.state import CellState
from gameoflifeapi.logic.exceptions import GameIsNotStartedException

log: logging.Logger = logging.getLogger(__name__)


GREEN_STYLE: str = 'background-color: #7FFF00; border-color: #000000; border-width: 6px; padding: 5px;'
GRAY_STYLE: str = 'background-color: #F0FFFF; border-color: #000000; border-width: 6px; padding: 5px;'


class QtGameFieldWidget(QWidget):
    """Define main Field QT Widget for game."""

    def __init__(self, controller: GameLifeController) -> None:
        """Initialize Field Widget."""
        QWidget.__init__(self)
        log.debug('QtGameFieldWidget.__init__')
        self._controller: GameLifeController = controller
        self._field_buttons: dict[tuple[int, int], QPushButton] = {}
        self._init_view()
        log.debug('QtGameFieldWidget.__init__.exit')

    def _init_view(self) -> None:
        """Initialize widget view."""
        log.debug('QtGameFieldWidget._init_view')
        self._field_grid_layout: QGridLayout = QGridLayout()
        self.setLayout(self._field_grid_layout)
        log.debug('QtGameFieldWidget._init_view.exit')

    def generate_field_view(self) -> None:
        """Build view for passed field.

        Initializes GRID of buttons for game field.
        """
        log.debug('QtGameFieldWidget.generate_field_view')
        if self._controller.game_state:
            field: Field = self._controller.game_state.game_field
            size_policy: QSizePolicy = QSizePolicy(
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Expanding
            )
            for row_index in range(0, field.rows):
                for col_index in range(0, field.columns):
                    btn: QPushButton = QPushButton()
                    btn.setSizePolicy(size_policy)
                    btn.setMinimumSize(10, 10)
                    btn.clicked.connect(lambda _state, row=row_index, col=col_index,
                                        button=btn: self._on_field_click(row, col, button))
                    self._make_button_gray(btn)
                    self.layout().addWidget(btn, row_index, col_index)
                    self.layout().setColumnMinimumWidth(col_index, 10)
                    self._field_buttons[(row_index, col_index)] = btn
        else:
            raise GameIsNotStartedException('Game Is Not Started')
        log.debug('QtGameFieldWidget.generate_field_view.exit')

    def _on_field_click(self, row: int, col: int, btn: QPushButton) -> None:
        """Process on field cell click event.

        Args:
            row (int): Number of row
            col (int): Number of column
            btn (QPushButton): Current button
        """
        log.debug('QtGameFieldWidget._on_field_click')
        self._controller.trigger_cell(row, col)
        field = self._controller.game_state.game_field
        cell = field.all_cells[(row, col)]
        style: str = GREEN_STYLE if cell.state is CellState.ALIVE else GRAY_STYLE
        self._change_button_color(btn, style)
        log.debug('QtGameFieldWidget._on_field_click.exit')

    def _change_button_color(self, button: QPushButton, style: str) -> None:
        """Change color of the button to one passed as param.

        Args:
            button (QPushButton): button to change color
            color (QColor): color that will be applied
        """
        button.setStyleSheet(style)

    def _make_button_green(self, button: QPushButton) -> None:
        """Change color of the passed button to GREEN.

        Args:
            button (QPushButton): current button
        """
        log.debug('QtGameFieldWidget._make_button_green')
        self._change_button_color(button, GREEN_STYLE)
        log.debug('QtGameFieldWidget._make_button_green.exit')

    def _make_button_gray(self, button: QPushButton) -> None:
        """Change color of the passed button to GRAY.

        Args:
            button (QPushButton): current button
        """
        log.debug('QtGameFieldWidget._make_button_gray')
        self._change_button_color(button, GRAY_STYLE)
        log.debug('QtGameFieldWidget._make_button_gray.exit')

    def update_view_state(self) -> None:
        """Update current state of the field widget."""
        log.debug('QtGameFieldWidget.update_view_state')
        if not self._field_buttons or len(self._field_buttons) == 0:
            self.generate_field_view()

        field = self._controller.game_state.game_field
        buttons = self._field_buttons
        if buttons and len(buttons) > 0:
            for (coordinates, cell) in field.all_cells.items():
                btn = buttons[coordinates]
                if cell.state is CellState.ALIVE:
                    self._make_button_green(btn)
                else:
                    self._make_button_gray(btn)
        else:
            log.warn('QtGameFieldWidget.update_view_state. Buttons are not created')
        log.debug('QtGameFieldWidget.update_view_state.exit')

    def clear_field(self) -> None:
        """Remove all the buttons from the GRID."""
        log.debug('QtGameFieldWidget.clear_field')
        while self.layout().count():
            layout_item = self.layout().takeAt(0)
            if layout_item.widget():
                layout_item.widget().deleteLater()
        del self._field_buttons
        self._field_buttons = {}
        self.layout().update()
        log.debug('QtGameFieldWidget.clear_field.exit')
