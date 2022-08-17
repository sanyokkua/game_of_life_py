import logging

from PyQt6.QtGui import QColor, QColorConstants, QPalette
from PyQt6.QtWidgets import QGridLayout, QPushButton, QSizePolicy, QWidget

from gameoflifeapi.api.game_controller import GameLifeController
from gameoflifeapi.logic.data.field import Field
from gameoflifeapi.logic.data.state import CellState

log: logging.Logger = logging.getLogger(__name__)


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
        """Initialize View of the Widget."""
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
            raise Exception('Game Is Not Started')
        log.debug('QtGameFieldWidget.generate_field_view.exit')

    def _on_field_click(self, row: int, col: int, btn: QPushButton) -> None:
        log.debug('QtGameFieldWidget._on_field_click')
        self._controller.trigger_cell(row, col)
        field = self._controller.game_state.game_field
        cell = field.all_cells[(row, col)]
        color = QColorConstants.Green if cell.state is CellState.ALIVE else QColorConstants.Gray
        self._change_button_color(btn, color)
        log.debug('QtGameFieldWidget._on_field_click.exit')

    def _change_button_color(self, button: QPushButton, color: QColor) -> None:
        palette: QPalette = QPalette(color)
        button.setAutoFillBackground(True)
        button.setPalette(palette)
        button.update()

    def _make_button_green(self, button: QPushButton) -> None:
        log.debug('QtGameFieldWidget._make_button_green')
        self._change_button_color(button, QColorConstants.Green)
        log.debug('QtGameFieldWidget._make_button_green.exit')

    def _make_button_gray(self, button: QPushButton) -> None:
        log.debug('QtGameFieldWidget._make_button_gray')
        self._change_button_color(button, QColorConstants.Gray)
        log.debug('QtGameFieldWidget._make_button_gray.exit')

    def update_view_state(self) -> None:
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
