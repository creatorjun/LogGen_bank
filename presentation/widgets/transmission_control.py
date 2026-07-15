# presentation/widgets/transmission_control.py
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PyQt6.QtCore import pyqtSignal


class TransmissionControl(QWidget):
    start_requested = pyqtSignal()
    stop_requested = pyqtSignal()
    copy_requested = pyqtSignal()
    clear_requested = pyqtSignal()
    person_edit_requested = pyqtSignal()

    _LABEL_START: str = "전송 시작"
    _LABEL_STOP: str = "전송 중지"

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._running: bool = False
        self._build_ui()

    def _build_ui(self) -> None:
        lay = QHBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(6)

        self._btn_toggle = QPushButton(self._LABEL_START)
        self._btn_toggle.setObjectName("btn_start")
        self._btn_toggle.setMinimumWidth(110)
        self._btn_toggle.setMinimumHeight(32)

        self._btn_copy = QPushButton("복사")
        self._btn_copy.setMinimumWidth(64)

        self._btn_clear = QPushButton("클리어")
        self._btn_clear.setMinimumWidth(64)

        self._btn_person = QPushButton("Person 편집")
        self._btn_person.setMinimumWidth(90)

        lay.addWidget(self._btn_toggle)
        lay.addStretch()
        lay.addWidget(self._btn_copy)
        lay.addWidget(self._btn_clear)
        lay.addWidget(self._btn_person)

        self._btn_toggle.clicked.connect(self._on_toggle)
        self._btn_copy.clicked.connect(self.copy_requested)
        self._btn_clear.clicked.connect(self.clear_requested)
        self._btn_person.clicked.connect(self.person_edit_requested)

    def _on_toggle(self) -> None:
        if self._running:
            self.stop_requested.emit()
        else:
            self.start_requested.emit()

    def set_running(self, running: bool) -> None:
        self._running = running
        if running:
            self._btn_toggle.setText(self._LABEL_STOP)
            self._btn_toggle.setObjectName("btn_stop")
        else:
            self._btn_toggle.setText(self._LABEL_START)
            self._btn_toggle.setObjectName("btn_start")
        self._btn_toggle.style().unpolish(self._btn_toggle)
        self._btn_toggle.style().polish(self._btn_toggle)
