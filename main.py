# main.py
import sys
import asyncio
from qasync import QEventLoop, QApplication
from presentation.main_window import MainWindow


def main() -> None:
    app = QApplication(sys.argv)
    event_loop = QEventLoop(app)
    asyncio.set_event_loop(event_loop)

    window = MainWindow()
    window.show()

    with event_loop:
        event_loop.run_forever()


if __name__ == "__main__":
    main()
