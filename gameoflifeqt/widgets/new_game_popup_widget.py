import logging

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QCheckBox, QDialog, QDialogButtonBox, QGridLayout,
                             QGroupBox, QLabel, QSizePolicy, QSpinBox,
                             QVBoxLayout)

log: logging.Logger = logging.getLogger(__name__)


class QtNewGamePopUpWidget(QDialog):

    def __init__(self) -> None:
        QDialog.__init__(self)
        log.debug('QtNewGamePopUpWidget.__init__')
        self._current_row_number: int = 10
        self._current_col_number: int = 10
        self._randomize_on_start: bool = False

        width: int = 200
        height: int = 150

        form_widgets_group: QGroupBox = QGroupBox()
        lbl_row: QLabel = QLabel('Number of ROWS')
        lbl_columns: QLabel = QLabel('Number of Columns')
        self._spin_box_rows: QSpinBox = QSpinBox()
        self._spin_box_columns: QSpinBox = QSpinBox()
        self._checkbox_random: QCheckBox = QCheckBox('Randomize on start')

        self._spin_box_rows.textChanged.connect(self._on_spin_box_rows)
        self._spin_box_columns.textChanged.connect(self._on_spin_box_columns)
        self._checkbox_random.stateChanged.connect(self._on_checkbox_random_state)

        expanding_policy = QSizePolicy.Policy.Expanding
        common_policy = QSizePolicy(expanding_policy, expanding_policy)

        lbl_row.setSizePolicy(common_policy)
        lbl_columns.setSizePolicy(common_policy)
        self._spin_box_rows.setSizePolicy(common_policy)
        self._spin_box_columns.setSizePolicy(common_policy)
        self._checkbox_random.setSizePolicy(common_policy)

        self._spin_box_rows.setMinimum(10)
        self._spin_box_rows.setMaximum(50)
        self._spin_box_columns.setMinimum(10)
        self._spin_box_columns.setMaximum(50)

        grid_layout_group: QGridLayout = QGridLayout()
        grid_layout_group.addWidget(lbl_row, 0, 0)
        grid_layout_group.addWidget(self._spin_box_rows, 0, 1)
        grid_layout_group.addWidget(lbl_columns, 1, 0)
        grid_layout_group.addWidget(self._spin_box_columns, 1, 1)
        grid_layout_group.addWidget(self._checkbox_random, 2, 0)

        form_widgets_group.setLayout(grid_layout_group)
        form_widgets_group.setMinimumSize(width, height)
        form_widgets_group.setMaximumSize(width, height)
        form_widgets_group.resize(width, height)

        main_layout: QVBoxLayout = QVBoxLayout()
        main_layout.addWidget(form_widgets_group)
        self.setLayout(main_layout)

        dialog_buttons_box: QDialogButtonBox = QDialogButtonBox(self)
        btn_ok = QDialogButtonBox.StandardButton.Ok
        btn_cancell = QDialogButtonBox.StandardButton.Cancel
        btns = btn_cancell | btn_ok
        dialog_buttons_box.setStandardButtons(btns)

        self.layout().addWidget(dialog_buttons_box)

        dialog_buttons_box.accepted.connect(self.accept)
        dialog_buttons_box.rejected.connect(self.reject)

        self.setWindowTitle('Start New Game')
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        dial_width: int = width + 40
        dial_height: int = height + 80
        self.setMaximumSize(dial_width, dial_height)
        self.setMinimumSize(dial_width, dial_height)
        self.resize(dial_width, dial_height)
        log.debug('QtNewGamePopUpWidget.__init__.exit')

    def _on_spin_box_rows(self) -> None:
        log.debug('QtNewGamePopUpWidget._on_spin_box_rows')
        self._current_row_number = self._spin_box_rows.value()
        log.debug('QtNewGamePopUpWidget._on_spin_box_rows.exit')

    def _on_spin_box_columns(self) -> None:
        log.debug('QtNewGamePopUpWidget._on_spin_box_columns')
        self._current_col_number = self._spin_box_columns.value()
        log.debug('QtNewGamePopUpWidget._on_spin_box_columns.exit')

    def _on_checkbox_random_state(self) -> None:
        log.debug('QtNewGamePopUpWidget._on_checkbox_random_state')
        if self._checkbox_random.isChecked():
            self._randomize_on_start = True
        else:
            self._randomize_on_start = False
        log.debug('QtNewGamePopUpWidget._on_checkbox_random_state.exit')

    @property
    def number_of_rows(self) -> int:
        return self._current_row_number

    @property
    def number_of_columns(self) -> int:
        return self._current_col_number

    @property
    def randomize_on_start(self) -> bool:
        return self._randomize_on_start
