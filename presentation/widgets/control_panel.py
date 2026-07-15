# presentation/widgets/control_panel.py
from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QGroupBox,
    QLabel, QLineEdit, QSpinBox, QPushButton,
)
from PyQt6.QtCore import pyqtSignal, Qt
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
    WIDGET_HEIGHT: int = 28

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
        lay.setContentsMargins(12, 8, 12, 8)
        lay.setSpacing(8)

        self._edit_host = QLineEdit(self.DEFAULT_HOST)
        self._edit_host.setFixedSize(150, self.WIDGET_HEIGHT)
        self._edit_host.setPlaceholderText("Host / IP")
        self._edit_host.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self._edit_port = QLineEdit(self.DEFAULT_PORT)
        self._edit_port.setFixedSize(64, self.WIDGET_HEIGHT)
        self._edit_port.setPlaceholderText("514")
        self._edit_port.setValidator(QIntValidator(1, 65535))
        self._edit_port.setAlignment(Qt.AlignmentFlag.AlignLeft)

        lbl_host = QLabel("Host")
        lbl_host.setFixedHeight(self.WIDGET_HEIGHT)
        lbl_port = QLabel("Port")
        lbl_port.setFixedHeight(self.WIDGET_HEIGHT)

        lay.addWidget(lbl_host)
        lay.addWidget(self._edit_host)
        lay.addSpacing(4)
        lay.addWidget(lbl_port)
        lay.addWidget(self._edit_port)
        return grp

    def _make_offset_group(self) -> QGroupBox:
        grp = QGroupBox("날짜 오프셋")
        lay = QHBoxLayout(grp)
        lay.setContentsMargins(12, 8, 12, 8)
        lay.setSpacing(6)

        self._btn_sign = QPushButton("+")
        self._btn_sign.setFixedSize(32, self.WIDGET_HEIGHT)
        self._btn_sign.setCheckable(True)

        self._spin_offset = QSpinBox()
        self._spin_offset.setRange(0, self.MAX_OFFSET_DAYS)
        self._spin_offset.setValue(self.DEFAULT_OFFSET)
        self._spin_offset.setFixedSize(68, self.WIDGET_HEIGHT)

        lbl_day = QLabel("일")
        lbl_day.setFixedHeight(self.WIDGET_HEIGHT)

        lay.addWidget(self._btn_sign)
        lay.addWidget(self._spin_offset)
        lay.addWidget(lbl_day)
        return grp

    def _make_interval_group(self) -> QGroupBox:
        grp = QGroupBox("전송 간격")
        lay = QHBoxLayout(grp)
        lay.setContentsMargins(12, 8, 12, 8)
        lay.setSpacing(6)

        self._spin_interval = QSpinBox()
        self._spin_interval.setRange(self.MIN_INTERVAL_MS, self.MAX_INTERVAL_MS)
        self._spin_interval.setValue(self.DEFAULT_INTERVAL_MS)
        self._spin_interval.setSuffix(" ms")
        self._spin_interval.setFixedSize(100, self.WIDGET_HEIGHT)

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
