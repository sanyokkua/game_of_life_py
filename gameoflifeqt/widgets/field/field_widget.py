"""Exports QtGameFieldWidget."""
import logging

from PyQt6.QtWidgets import QGridLayout, QLayoutItem, QWidget

from gameoflifeapi.api.game_controller import GameLifeController
from gameoflifeapi.logic.exceptions import GameIsNotStartedException
from gameoflifeqt.widgets.field.button import QFieldButtonCell

log: logging.Logger = logging.getLogger(__name__)


class QtGameFieldWidget(QWidget):
    """Define main Field QT Widget for game."""

    def __init__(self, parent, controller: GameLifeController) -> None:
        """Initialize Field Widget."""
        QWidget.__init__(self, parent)
        log.debug('__init__')
        self._controller: GameLifeController = controller
        self._init_widget_layout()
        self._init_field_buttons()

    def _init_widget_layout(self) -> None:
        self._field_grid_layout: QGridLayout = QGridLayout(self)
        self._field_grid_layout.setContentsMargins(0, 0, 0, 0)
        self._field_grid_layout.setSpacing(0)
        self.setLayout(self._field_grid_layout)

    def _init_field_buttons(self) -> None:
        self._field_buttons: dict[tuple[int, int], QFieldButtonCell] = {}

    def generate_field_view(self) -> None:
        """Build view for passed field.

        Initializes GRID of buttons for game field.
        """
        if self._controller.game_state is not None:
            self.clear_field()
            field = self._controller.game_state.game_field.all_cells.values()
            for cell in field:
                btn: QFieldButtonCell = QFieldButtonCell(self, cell)

                def handler(_state, button=btn):
                    self._on_field_click(button)

                btn.clicked.connect(handler)
                self._field_grid_layout.addWidget(btn, cell.row, cell.column)
                self._field_buttons[(cell.row, cell.column)] = btn
        else:
            raise GameIsNotStartedException('Game Is Not Started')

    def _on_field_click(self, btn: QFieldButtonCell) -> None:
        """Process on field cell click event.

        Args:
            btn (QFieldButtonCell): Current button
        """
        log.debug('QtGameFieldWidget._on_field_click')
        self._controller.trigger_cell(btn.cell.row, btn.cell.column)
        btn.update_button_state()
        log.debug('QtGameFieldWidget._on_field_click.exit')

    def update_view_state(self) -> None:
        """Update current state of the field widget."""
        log.debug('QtGameFieldWidget.update_view_state')
        if not self._field_buttons or len(self._field_buttons) == 0:
            self.generate_field_view()
        else:
            for btn in self._field_buttons.values():
                btn.update_button_state()
        log.debug('QtGameFieldWidget.update_view_state.exit')

    def clear_field(self) -> None:
        """Remove all the buttons from the GRID."""
        while self.layout().count():
            layout_item: QLayoutItem = self.layout().takeAt(0)
            if layout_item.widget():
                layout_item.widget().deleteLater()
        self._field_buttons.clear()
        self.layout().update()
