# presentation/widgets/control_panel.py
from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QGroupBox,
    QLabel, QLineEdit, QSpinBox, QPushButton,
)
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QIntValidator


class ControlPanel(QWidget):
    target_changed = pyqtSignal(str, int)
    offset_changed = pyqtSignal(int, int)
    interval_changed = pyqtSignal(float)

    DEFAULT_HOST: str = "127.0.0.1"
    DEFAULT_PORT: str = "514"
    DEFAULT_OFFSET: int = 0
    DEFAULT_INTERVAL_MS: int = 500
    MIN_INTERVAL_MS: int = 1
    MAX_INTERVAL_MS: int = 99999
    MAX_OFFSET_DAYS: int = 999

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._build_ui()
        self._connect()

    def _build_ui(self) -> None:
        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(8)

        root.addWidget(self._make_target_group())
        root.addWidget(self._make_offset_group())
        root.addWidget(self._make_interval_group())
        root.addStretch()

    def _make_target_group(self) -> QGroupBox:
        grp = QGroupBox("전송 대상")
        lay = QHBoxLayout(grp)
        lay.setContentsMargins(10, 16, 10, 10)
        lay.setSpacing(8)

        self._edit_host = QLineEdit(self.DEFAULT_HOST)
        self._edit_host.setFixedWidth(150)
        self._edit_host.setPlaceholderText("Host / IP")

        self._edit_port = QLineEdit(self.DEFAULT_PORT)
        self._edit_port.setFixedWidth(60)
        self._edit_port.setPlaceholderText("Port")
        self._edit_port.setValidator(QIntValidator(1, 65535))

        lay.addWidget(QLabel("Host"))
        lay.addWidget(self._edit_host)
        lay.addSpacing(8)
        lay.addWidget(QLabel("Port"))
        lay.addWidget(self._edit_port)
        return grp

    def _make_offset_group(self) -> QGroupBox:
        grp = QGroupBox("날짜 오프셋")
        lay = QHBoxLayout(grp)
        lay.setContentsMargins(10, 16, 10, 10)
        lay.setSpacing(6)

        self._btn_sign = QPushButton("+")
        self._btn_sign.setFixedSize(34, 28)
        self._btn_sign.setCheckable(True)

        self._spin_offset = QSpinBox()
        self._spin_offset.setRange(0, self.MAX_OFFSET_DAYS)
        self._spin_offset.setValue(self.DEFAULT_OFFSET)
        self._spin_offset.setFixedWidth(70)
        self._spin_offset.setFixedHeight(28)

        lbl_day = QLabel("일")

        lay.addWidget(self._btn_sign)
        lay.addWidget(self._spin_offset)
        lay.addWidget(lbl_day)
        return grp

    def _make_interval_group(self) -> QGroupBox:
        grp = QGroupBox("전송 간격")
        lay = QHBoxLayout(grp)
        lay.setContentsMargins(10, 16, 10, 10)
        lay.setSpacing(6)

        self._spin_interval = QSpinBox()
        self._spin_interval.setRange(self.MIN_INTERVAL_MS, self.MAX_INTERVAL_MS)
        self._spin_interval.setValue(self.DEFAULT_INTERVAL_MS)
        self._spin_interval.setSuffix(" ms")
        self._spin_interval.setFixedWidth(100)
        self._spin_interval.setFixedHeight(28)

        lay.addWidget(self._spin_interval)
        return grp

    def _connect(self) -> None:
        self._edit_host.editingFinished.connect(self._emit_target)
        self._edit_port.editingFinished.connect(self._emit_target)
        self._btn_sign.toggled.connect(self._on_sign_toggled)
        self._spin_offset.valueChanged.connect(self._emit_offset)
        self._spin_interval.valueChanged.connect(
            lambda v: self.interval_changed.emit(v / 1000.0)
        )

    def _on_sign_toggled(self, checked: bool) -> None:
        self._btn_sign.setText("-" if checked else "+")
        self._emit_offset()

    def _emit_target(self) -> None:
        self.target_changed.emit(self._edit_host.text().strip(), self.get_port())

    def _emit_offset(self) -> None:
        self.offset_changed.emit(self.get_offset_sign(), self._spin_offset.value())

    def get_host(self) -> str:
        return self._edit_host.text().strip()

    def get_port(self) -> int:
        text = self._edit_port.text().strip()
        return int(text) if text.isdigit() else 514

    def get_offset_sign(self) -> int:
        return -1 if self._btn_sign.isChecked() else 1

    def get_offset_days(self) -> int:
        return self._spin_offset.value()

    def get_interval_seconds(self) -> float:
        return self._spin_interval.value() / 1000.0
