import logging

from PyQt6.QtWidgets import QApplication

from gameoflifeqt.widgets.control_widget import QtGameControlWidget

log: logging.Logger = logging.getLogger(__name__)


class GameOfLifeQtApplication(QApplication):

    def __init__(self) -> None:
        """Initialize Application."""
        super().__init__([])
        log.debug('GameOfLifeQtApplication.__init__')
        screen_resolution = self.primaryScreen().geometry()
        width, height = screen_resolution.width(), screen_resolution.height()
        self.w_control: QtGameControlWidget = QtGameControlWidget(width, height)
        self.w_control.show()
        log.debug('GameOfLifeQtApplication.__init__.exit')
