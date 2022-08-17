import logging
import sys

from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (QFileDialog, QGridLayout, QGroupBox, QMainWindow,
                             QMenu, QMenuBar, QPushButton, QSizePolicy,
                             QVBoxLayout, QWidget)

from gameoflifeapi.api.game_controller import GameLifeController
from gameoflifeapi.api.persistance import GamePicklePersistance
from gameoflifeapi.logic.data.dtos import GameDataDto, NewGameDataDto
from gameoflifeqt.widgets.field_widget import QtGameFieldWidget
from gameoflifeqt.widgets.new_game_popup_widget import QtNewGamePopUpWidget

log: logging.Logger = logging.getLogger(__name__)

TEXT_AUTO_UPDATE_UP: str = 'Activate Auto Genearation'
TEXT_AUTO_UPDATE_DOWN: str = 'Disable Auto Genearation'


class QtGameControlWidget(QMainWindow):
    """Class represents main app widget with all controls."""

    def __init__(self, width: int, height: int) -> None:
        """Initialize Main Control widget."""
        QMainWindow.__init__(self)
        log.debug('QtGameControlWidget.__init__')
        self._width: int = width
        self._height: int = height
        self._game_persistence: GamePicklePersistance = GamePicklePersistance()
        self._controller: GameLifeController = GameLifeController(
            self._game_persistence,
            self._on_generation_created)
        self._field_widget = QtGameFieldWidget(self._controller)

        self._timer: QTimer = QTimer(self)
        self._timer.setInterval(300)
        self._timer.timeout.connect(self._on_timer_update)

        self._init_menu()
        self._init_controls()
        self._init_main_layout()
        log.debug('QtGameControlWidget.__init__.exit')

    def _init_menu(self) -> None:
        log.debug('QtGameControlWidget._init_menu')
        menu_bar: QMenuBar = self.menuBar()
        menu_game: QMenu = QMenu('Menu', menu_bar)

        action_new_game: QAction = QAction('&New Game', menu_game)
        action_save_game: QAction = QAction('&Save Game', menu_game)
        action_load_game: QAction = QAction('&Load Game', menu_game)
        action_exit: QAction = QAction('&Exit Game', menu_game)

        action_new_game.triggered.connect(self._on_action_new_game)
        action_save_game.triggered.connect(self._on_action_save_game)
        action_load_game.triggered.connect(self._on_action_load_game)
        action_exit.triggered.connect(self._on_action_exit)

        action_save_game.setShortcut('Ctrl+S')
        action_save_game.setStatusTip('Save Game to File')

        menu_game.addActions([
            action_new_game,
            action_save_game,
            action_load_game,
            action_exit
        ])
        menu_bar.addMenu(menu_game)
        log.debug('QtGameControlWidget._init_menu.exit')

    def _init_controls(self) -> None:
        log.debug('QtGameControlWidget._init_controls')
        self._control_widget_group: QGroupBox = QGroupBox()

        self._button_next_gen: QPushButton = QPushButton(
            'Generate new Generation')
        self._button_toggle_autoupdate: QPushButton = QPushButton(
            TEXT_AUTO_UPDATE_UP)

        self._button_next_gen.setEnabled(False)
        self._button_toggle_autoupdate.setEnabled(False)

        self._button_next_gen.clicked.connect(self._on_button_next_gen)
        self._button_toggle_autoupdate.clicked.connect(
            self._on_button_toggle_autoupdate)

        self._button_next_gen.setSizePolicy(QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
        self._button_toggle_autoupdate.setSizePolicy(QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))

        grid_layout_group: QGridLayout = QGridLayout()
        grid_layout_group.addWidget(self._button_next_gen, 0, 0)
        grid_layout_group.addWidget(self._button_toggle_autoupdate, 0, 1)

        self._control_widget_group.setLayout(grid_layout_group)
        self._control_widget_group.setMinimumSize(150, 50)
        self._control_widget_group.setMaximumHeight(50)
        log.debug('QtGameControlWidget._init_controls.exit')

    def _init_main_layout(self) -> None:
        log.debug('QtGameControlWidget._init_main_layout')
        main_layout: QVBoxLayout = QVBoxLayout()
        main_layout.addWidget(self.menuBar())
        main_layout.addWidget(self._control_widget_group)
        main_layout.addWidget(self._field_widget)
        main_widget: QWidget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        log.debug('QtGameControlWidget._init_main_layout.exit')

    def _stop_timer(self) -> None:
        if self._timer.isActive():
            self._timer.stop()
            self._button_toggle_autoupdate.setDown(False)
            self._button_toggle_autoupdate.setText(TEXT_AUTO_UPDATE_UP)
            self._button_next_gen.setEnabled(True)

    def _start_timer(self) -> None:
        if not self._timer.isActive():
            self._timer.start()
            self._button_toggle_autoupdate.setDown(True)
            self._button_toggle_autoupdate.setText(TEXT_AUTO_UPDATE_DOWN)
            self._button_next_gen.setEnabled(False)

    def _on_action_new_game(self) -> None:
        log.debug('QtGameControlWidget._on_action_new_game')
        self._stop_timer()
        dial: QtNewGamePopUpWidget = QtNewGamePopUpWidget()
        dial_res: int = dial.exec()

        if dial_res:
            new_game: NewGameDataDto = NewGameDataDto(
                number_of_columns=dial.number_of_columns,
                number_of_rows=dial.number_of_rows,
                is_random_first_generation=dial.randomize_on_start
            )
            self._before_game_start(new_game)
            self._controller.start_new_game(new_game)
        log.debug('QtGameControlWidget._on_action_new_game.exit')

    def _before_game_start(self, game_data: GameDataDto) -> None:
        log.debug('QtGameControlWidget._start_game')
        self._field_widget.clear_field()
        self._button_next_gen.setEnabled(True)
        self._button_toggle_autoupdate.setEnabled(True)

        rows: int = game_data.number_of_rows
        cols: int = game_data.number_of_columns
        width: int = self._width // rows
        height: int = self._height // cols
        size_w = width * rows
        size_h = height * cols - 50
        final_w = size_w if size_w < self._width else self._width
        final_h = size_h if size_h < self._height else self._height
        self.resize(final_w, final_h)
        self.move(0, 0)
        log.debug('QtGameControlWidget._start_game.exit')

    def _on_action_save_game(self) -> None:
        log.debug('QtGameControlWidget._on_action_save_game')
        self._stop_timer()

        file_name, _ = QFileDialog.getSaveFileName(None, 'Save File', './', 'GameSave (*.gsave)')
        self._controller.save_game(file_name)
        log.debug('QtGameControlWidget._on_action_save_game.exit')

    def _on_action_load_game(self) -> None:
        log.debug('QtGameControlWidget._on_action_load_game')
        self._stop_timer()

        file_name, _ = QFileDialog.getOpenFileName(None, 'Open Save File', './', 'GameSave (*.gsave)')
        self._controller.load_game(file_name)
        game_data = GameDataDto(
            number_of_rows=self._controller.game_state.game_field.rows,
            number_of_columns=self._controller.game_state.game_field.columns,
            is_random_first_generation=False,
            generation=self._controller.game_state.generation,
            game_field=self._controller.game_state.game_field
        )
        self._before_game_start(game_data)
        self._field_widget.update_view_state()
        self._button_next_gen.setEnabled(True)
        self._button_toggle_autoupdate.setEnabled(True)
        log.debug('QtGameControlWidget._on_action_load_game.exit')

    def _on_action_exit(self) -> None:
        log.debug('QtGameControlWidget._on_action_exit')
        self._stop_timer()
        log.debug('QtGameControlWidget._on_action_exit.exit')
        sys.exit()

    def _on_button_next_gen(self) -> None:
        log.debug('QtGameControlWidget._on_button_next_gen')
        self._controller.increment_generation()
        log.debug('QtGameControlWidget._on_button_next_gen.exit')

    def _on_button_toggle_autoupdate(self) -> None:
        log.debug('QtGameControlWidget._on_button_toggle_autoupdate')
        if self._timer.isActive():
            self._stop_timer()
        else:
            self._start_timer()
        log.debug('QtGameControlWidget._on_button_toggle_autoupdate.exit')

    def _on_timer_update(self) -> None:
        log.debug('QtGameControlWidget._on_auto_update')
        self._on_button_next_gen()
        log.debug('QtGameControlWidget._on_auto_update.exit')

    def _on_generation_created(self) -> None:
        log.debug('QtGameControlWidget._on_generation_created')
        self._field_widget.update_view_state()
        self.setWindowTitle(f'Current Generation: {self._controller.game_state.generation}')
        log.debug('QtGameControlWidget._on_generation_created.exit')
