import logging

from gameoflifeqt.widgets.application_widget import GameOfLifeQtApplication

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s [%(name)s %(funcName)s] %(message)s')

log: logging.Logger = logging.getLogger(__name__)


def start_game() -> None:
    """Start the Qt Game."""
    app: GameOfLifeQtApplication = GameOfLifeQtApplication()
    app.exec()


start_game()
