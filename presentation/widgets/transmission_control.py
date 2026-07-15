# presentation/widgets/transmission_control.py
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PyQt6.QtCore import pyqtSignal


class TransmissionControl(QWidget):
    start_requested = pyqtSignal()
    stop_requested = pyqtSignal()
    copy_requested = pyqtSignal()
    clear_requested = pyqtSignal()
    person_edit_requested = pyqtSignal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self) -> None:
        lay = QHBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(6)

        self._btn_start = QPushButton("전송 시작")
        self._btn_start.setObjectName("btn_start")
        self._btn_start.setMinimumWidth(100)

        self._btn_stop = QPushButton("전송 중지")
        self._btn_stop.setObjectName("btn_stop")
        self._btn_stop.setMinimumWidth(100)
        self._btn_stop.setEnabled(False)

        self._btn_copy = QPushButton("복사")
        self._btn_copy.setMinimumWidth(64)

        self._btn_clear = QPushButton("클리어")
        self._btn_clear.setMinimumWidth(64)

        self._btn_person = QPushButton("Person 편집")
        self._btn_person.setMinimumWidth(90)

        lay.addWidget(self._btn_start)
        lay.addWidget(self._btn_stop)
        lay.addStretch()
        lay.addWidget(self._btn_copy)
        lay.addWidget(self._btn_clear)
        lay.addWidget(self._btn_person)

        self._btn_start.clicked.connect(self._on_start)
        self._btn_stop.clicked.connect(self._on_stop)
        self._btn_copy.clicked.connect(self.copy_requested)
        self._btn_clear.clicked.connect(self.clear_requested)
        self._btn_person.clicked.connect(self.person_edit_requested)

    def _on_start(self) -> None:
        self.start_requested.emit()

    def _on_stop(self) -> None:
        self.stop_requested.emit()

    def set_running(self, running: bool) -> None:
        self._btn_start.setEnabled(not running)
        self._btn_stop.setEnabled(running)
