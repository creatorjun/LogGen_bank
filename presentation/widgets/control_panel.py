# presentation/widgets/control_panel.py
from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QGroupBox,
    QLabel, QLineEdit, QSpinBox, QPushButton,
)
from PyQt6.QtCore import pyqtSignal


class ControlPanel(QWidget):
    target_changed = pyqtSignal(str, int)
    offset_changed = pyqtSignal(int, int)
    interval_changed = pyqtSignal(float)

    DEFAULT_HOST: str = "127.0.0.1"
    DEFAULT_PORT: int = 514
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

    def _make_target_group(self) -> QGroupBox:
        grp = QGroupBox("전송 대상")
        lay = QHBoxLayout(grp)
        lay.setSpacing(6)
        self._edit_host = QLineEdit(self.DEFAULT_HOST)
        self._edit_host.setFixedWidth(140)
        self._edit_host.setPlaceholderText("Host / IP")
        self._spin_port = QSpinBox()
        self._spin_port.setRange(1, 65535)
        self._spin_port.setValue(self.DEFAULT_PORT)
        self._spin_port.setFixedWidth(72)
        lay.addWidget(QLabel("Host"))
        lay.addWidget(self._edit_host)
        lay.addWidget(QLabel("Port"))
        lay.addWidget(self._spin_port)
        return grp

    def _make_offset_group(self) -> QGroupBox:
        grp = QGroupBox("날짜 오프셋")
        lay = QHBoxLayout(grp)
        lay.setSpacing(6)
        self._btn_sign = QPushButton("+")
        self._btn_sign.setFixedWidth(32)
        self._btn_sign.setCheckable(True)
        self._spin_offset = QSpinBox()
        self._spin_offset.setRange(0, self.MAX_OFFSET_DAYS)
        self._spin_offset.setValue(self.DEFAULT_OFFSET)
        self._spin_offset.setFixedWidth(60)
        lay.addWidget(self._btn_sign)
        lay.addWidget(self._spin_offset)
        lay.addWidget(QLabel("일"))
        return grp

    def _make_interval_group(self) -> QGroupBox:
        grp = QGroupBox("전송 간격")
        lay = QHBoxLayout(grp)
        lay.setSpacing(6)
        self._spin_interval = QSpinBox()
        self._spin_interval.setRange(self.MIN_INTERVAL_MS, self.MAX_INTERVAL_MS)
        self._spin_interval.setValue(self.DEFAULT_INTERVAL_MS)
        self._spin_interval.setSuffix(" ms")
        self._spin_interval.setFixedWidth(90)
        lay.addWidget(self._spin_interval)
        return grp

    def _connect(self) -> None:
        self._edit_host.editingFinished.connect(self._emit_target)
        self._spin_port.valueChanged.connect(self._emit_target)
        self._btn_sign.toggled.connect(self._emit_offset)
        self._spin_offset.valueChanged.connect(self._emit_offset)
        self._spin_interval.valueChanged.connect(
            lambda v: self.interval_changed.emit(v / 1000.0)
        )

    def _emit_target(self) -> None:
        self.target_changed.emit(self._edit_host.text().strip(), self._spin_port.value())

    def _emit_offset(self) -> None:
        sign = -1 if self._btn_sign.isChecked() else 1
        if self._btn_sign.isChecked():
            self._btn_sign.setText("-")
        else:
            self._btn_sign.setText("+")
        self.offset_changed.emit(sign, self._spin_offset.value())

    def get_host(self) -> str:
        return self._edit_host.text().strip()

    def get_port(self) -> int:
        return self._spin_port.value()

    def get_offset_sign(self) -> int:
        return -1 if self._btn_sign.isChecked() else 1

    def get_offset_days(self) -> int:
        return self._spin_offset.value()

    def get_interval_seconds(self) -> float:
        return self._spin_interval.value() / 1000.0
