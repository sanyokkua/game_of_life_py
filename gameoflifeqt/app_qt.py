import logging
import sys

from PyQt6.QtCore import QSize, QTimer
from PyQt6.QtGui import QAction, QColor, QColorConstants, QPalette
from PyQt6.QtWidgets import (QApplication, QCheckBox, QGridLayout, QGroupBox,
                             QLabel, QMainWindow, QMenu, QMenuBar, QPushButton,
                             QSizePolicy, QSpinBox, QVBoxLayout, QWidget)

from gameoflifeapi.core.api.controller import GameLifeController
from gameoflifeapi.core.api.persistance import GameLifePicklePersistance
from gameoflifeapi.core.classes.game_enums import GameLifeCellState

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s')

log: logging.Logger = logging.getLogger(__name__)


class GameOfLifeQtFieldWidget(QWidget):
    """Define main Field QT Widget for game."""

    def __init__(self, controller: GameLifeController) -> None:
        """Initialize Field Widget."""
        QWidget.__init__(self)
        self._controller: GameLifeController = controller
        self._field_buttons: list[list[QPushButton]] = []
        self._init_view()

    def _init_view(self) -> None:
        """Initialize View of the Widget."""
        self._main_layout: QVBoxLayout = QVBoxLayout()
        self._field_group: QGroupBox = QGroupBox()
        self._field_group_layout: QGridLayout = QGridLayout()
        self._field_group.setLayout(self._field_group_layout)
        self._main_layout.addWidget(self._field_group)
        self.setLayout(self._main_layout)

    def generate_field_view(self) -> None:
        """
        Build view for passed field.

        Initializes GRID of buttons for game field.
        """
        log.debug('generate_field_view()')
        if self._controller.game_field:
            field = self._controller.game_field
            size_policy = QSizePolicy(
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Expanding)
            for row_index, row in enumerate(field):
                row_buttons: list[QPushButton] = []
                for col_index, col in enumerate(field[row_index]):
                    btn: QPushButton = QPushButton()
                    btn.setSizePolicy(size_policy)
                    btn.setMinimumSize(100, 100)
                    log.debug('generate_field_view, row: %d, col: %d',
                              row_index, col_index)
                    btn.clicked.connect(lambda state, row=row_index, col=col_index,
                                        button=btn: self._on_field_click(row, col, button))
                    self._make_button_gray(btn)
                    self._field_group_layout.addWidget(
                        btn, row_index, col_index)
                    self._field_group_layout.setColumnMinimumWidth(
                        col_index, 100)
                    row_buttons.append(btn)
                self._field_buttons.append(row_buttons)
        else:
            raise Exception('Game Is Not Started')

    def _on_field_click(self, row: int, col: int, btn: QPushButton) -> None:
        state = self._controller.switch_state(row, col)
        color = QColorConstants.Green if state is GameLifeCellState.ALIVE else QColorConstants.Gray
        palette = QPalette(color)
        btn.setAutoFillBackground(True)
        btn.setPalette(palette)
        btn.update()

    def _change_button_color(self, button: QPushButton, color: QColor) -> None:
        palette: QPalette = QPalette(color)
        button.setAutoFillBackground(True)
        button.setPalette(palette)
        button.update()

    def _make_button_green(self, button: QPushButton):
        self._change_button_color(button, QColorConstants.Green)

    def _make_button_gray(self, button: QPushButton):
        self._change_button_color(button, QColorConstants.Gray)

    def update_view_state(self) -> None:
        field = self._controller.game_field
        buttons = self._field_buttons
        for row_index, row in enumerate(field):
            for col_index, col in enumerate(field[row_index]):
                cell = field[row_index][col_index]
                btn = buttons[row_index][col_index]
                if cell.state is GameLifeCellState.ALIVE:
                    self._make_button_green(btn)
                else:
                    self._make_button_gray(btn)

    def clear_field(self) -> None:
        """Remove all the buttons from the GRID."""
        for row_buttons in self._field_buttons:
            for button in row_buttons:
                self._field_group_layout.removeWidget(button)
        del self._field_buttons
        self._field_buttons = []


class GameOfLifeQtControlWidget(QMainWindow):
    """Class represents main app widget with all controls."""

    def __init__(self, controller: GameLifeController) -> None:
        """Initialize Main Control widget."""
        QMainWindow.__init__(self)
        self._controller = controller
        self._field_widget: GameOfLifeQtFieldWidget = GameOfLifeQtFieldWidget(
            controller)
        self._current_row_number: int = 10
        self._current_col_number: int = 10
        self._randomize_on_start: bool = False

        self._timer: QTimer = QTimer(self)
        self._timer.setInterval(300)
        self._timer.timeout.connect(self._on_auto_update)

        self.setWindowTitle('Game Of Life')
        size: QSize = QSize(150, 150)
        self.setMinimumSize(size)
        self.setBaseSize(size)
        self._init_menu()
        self._init_controls()
        self._init_main_layout()

    def _init_menu(self) -> None:
        menu_bar: QMenuBar = self.menuBar()
        menu_game: QMenu = QMenu('Menu', menu_bar)

        action_new_game: QAction = QAction('New Game', menu_game)
        action_save_game: QAction = QAction('Save Game', menu_game)
        action_load_game: QAction = QAction('Load Game', menu_game)
        action_exit: QAction = QAction('Exit Game', menu_game)

        action_new_game.triggered.connect(self._on_action_new_game)
        action_save_game.triggered.connect(self._on_action_save_game)
        action_load_game.triggered.connect(self._on_action_load_game)
        action_exit.triggered.connect(self._on_action_exit)

        menu_game.addActions([
            action_new_game,
            action_save_game,
            action_load_game,
            action_exit
        ])
        menu_bar.addMenu(menu_game)

    def _init_controls(self) -> None:
        self._control_widget_group: QGroupBox = QGroupBox()

        self._label_rows: QLabel = QLabel('Number of ROWS')
        self._label_columns: QLabel = QLabel('Number of Columns')
        self._spin_box_rows: QSpinBox = QSpinBox()
        self._spin_box_columns: QSpinBox = QSpinBox()
        self._checkbox_random_state: QCheckBox = QCheckBox(
            'Randomize on start')
        self._button_next_gen: QPushButton = QPushButton(
            'Generate new Generation')
        self._button_toggle_autoupdate: QPushButton = QPushButton(
            'Automatic Update')

        self._button_next_gen.setEnabled(False)
        self._button_toggle_autoupdate.setEnabled(False)

        self._spin_box_rows.textChanged.connect(self._on_spin_box_rows)
        self._spin_box_columns.textChanged.connect(self._on_spin_box_columns)
        self._checkbox_random_state.stateChanged.connect(
            self._on_checkbox_random_state)
        self._button_next_gen.clicked.connect(self._on_button_next_gen)
        self._button_toggle_autoupdate.clicked.connect(
            self._on_button_toggle_autoupdate)

        self._label_rows.setSizePolicy(QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
        self._label_columns.setSizePolicy(QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
        self._spin_box_rows.setSizePolicy(QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
        self._spin_box_columns.setSizePolicy(QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
        self._checkbox_random_state.setSizePolicy(QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
        self._button_next_gen.setSizePolicy(QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
        self._button_toggle_autoupdate.setSizePolicy(QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))

        self._spin_box_rows.setMinimum(10)
        self._spin_box_rows.setMaximum(1000)
        self._spin_box_columns.setMinimum(10)
        self._spin_box_columns.setMaximum(1000)

        grid_layout_group: QGridLayout = QGridLayout()
        grid_layout_group.addWidget(self._label_rows, 0, 0)
        grid_layout_group.addWidget(self._spin_box_rows, 0, 1)
        grid_layout_group.addWidget(self._label_columns, 1, 0)
        grid_layout_group.addWidget(self._spin_box_columns, 1, 1)
        grid_layout_group.addWidget(self._checkbox_random_state, 2, 0)
        grid_layout_group.addWidget(self._button_next_gen, 2, 1)
        grid_layout_group.addWidget(self._button_toggle_autoupdate, 3, 0, 2, 0)

        self._control_widget_group.setLayout(grid_layout_group)
        self._control_widget_group.setMinimumSize(150, 150)
        self._control_widget_group.setMaximumHeight(150)

    def _init_main_layout(self) -> None:
        log.debug('_init_main_layout')
        main_layout: QVBoxLayout = QVBoxLayout()
        main_layout.addWidget(self.menuBar())
        main_layout.addWidget(self._control_widget_group)
        main_layout.addWidget(self._field_widget)
        main_widget: QWidget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def _on_action_new_game(self) -> None:
        log.debug('_on_action_new_game')
        self._button_next_gen.setEnabled(True)
        self._button_toggle_autoupdate.setEnabled(True)
        self._spin_box_rows.setEnabled(False)
        self._spin_box_columns.setEnabled(False)
        self._controller.start_new_game(
            self._current_row_number, self._current_col_number)
        self._field_widget.generate_field_view()
        if self._randomize_on_start:
            self._controller.make_random_cell_states()
        self._field_widget.clear_field()
        self._field_widget.generate_field_view()
        self._field_widget.update_view_state()

    def _on_action_save_game(self) -> None:
        log.debug('_on_action_save_game')

    def _on_action_load_game(self) -> None:
        log.debug('_on_action_load_game')
        self._button_next_gen.setEnabled(True)
        self._button_toggle_autoupdate.setEnabled(True)

    def _on_action_exit(self) -> None:
        log.debug('_on_action_exit')
        sys.exit()

    def _on_spin_box_rows(self) -> None:
        log.debug('_on_line_edit_rows')
        self._current_row_number = self._spin_box_rows.value()

    def _on_spin_box_columns(self) -> None:
        log.debug('_on_line_edit_columns')
        self._current_col_number = self._spin_box_columns.value()

    def _on_checkbox_random_state(self) -> None:
        log.debug('_on_checkbox_random_state')
        if self._checkbox_random_state.isChecked():
            self._randomize_on_start = True
        else:
            self._randomize_on_start = False

    def _on_button_next_gen(self) -> None:
        log.debug('_on_button_next_gen')
        self._controller.increment_generation()
        self._field_widget.update_view_state()

    def _on_button_toggle_autoupdate(self) -> None:
        log.debug('_on_button_toggle_autoupdate')
        if self._timer.isActive():
            self._timer.stop()
        else:
            self._timer.start()

    def _on_auto_update(self) -> None:
        log.debug('_on_auto_update')
        self._on_button_next_gen()


class GameOfLifeQtApplication(QApplication):

    def __init__(self) -> None:
        """Initialize Application."""
        super().__init__([])
        log.debug('GameOfLifeQtApplication.__init__')
        self.game_persistence = GameLifePicklePersistance()
        self.controller = GameLifeController(self.game_persistence)
        self.w_control = GameOfLifeQtControlWidget(self.controller)
        self.w_control.show()


def start_game() -> None:
    """Start the Qt Game."""
    app = GameOfLifeQtApplication()
    app.exec()


start_game()
