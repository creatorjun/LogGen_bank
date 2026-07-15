# main.py
import sys
import asyncio
from pathlib import Path
from qasync import QEventLoop, QApplication
from PyQt6.QtGui import QIcon
from presentation.main_window import MainWindow


def _app_icon() -> QIcon:
    svg_path = Path(__file__).parent / "resources" / "icon.svg"
    return QIcon(str(svg_path))


def main() -> None:
    app = QApplication(sys.argv)
    app.setWindowIcon(_app_icon())

    event_loop = QEventLoop(app)
    asyncio.set_event_loop(event_loop)

    window = MainWindow()
    window.show()

    with event_loop:
        event_loop.run_forever()


if __name__ == "__main__":
    main()
