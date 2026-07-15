# presentation/widgets/control_panel.py
from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QGroupBox,
    QLabel, QLineEdit, QSpinBox, QPushButton, QButtonGroup,
)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QIntValidator, QFont


class ControlPanel(QWidget):
    target_changed = pyqtSignal(str, int)
    offset_changed = pyqtSignal(int, int)
    interval_changed = pyqtSignal(float)

    DEFAULT_HOST: str = "127.0.0.1"
    DEFAULT_PORT: str = "514"
    DEFAULT_OFFSET: int = 0
    DEFAULT_INTERVAL_MS: int = 50
    MIN_INTERVAL_MS: int = 1
    MAX_INTERVAL_MS: int = 99999
    MAX_OFFSET_DAYS: int = 999
    WIDGET_HEIGHT: int = 28
    SIGN_BTN_W: int = 26
    SIGN_BTN_H: int = 24

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._build_ui()
        self._connect()

    def _sign_font(self) -> QFont:
        f = QFont()
        f.setBold(True)
        f.setPointSize(11)
        return f

    def _build_ui(self) -> None:
        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(8)
        root.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        root.addWidget(self._make_target_group())
        root.addWidget(self._make_offset_group())
        root.addWidget(self._make_interval_group())
        root.addStretch()

    def _make_target_group(self) -> QGroupBox:
        grp = QGroupBox("전송 대상")
        lay = QHBoxLayout(grp)
        lay.setContentsMargins(12, 8, 12, 8)
        lay.setSpacing(8)
        lay.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self._edit_host = QLineEdit(self.DEFAULT_HOST)
        self._edit_host.setFixedSize(150, self.WIDGET_HEIGHT)
        self._edit_host.setPlaceholderText("Host / IP")

        self._edit_port = QLineEdit(self.DEFAULT_PORT)
        self._edit_port.setFixedSize(64, self.WIDGET_HEIGHT)
        self._edit_port.setPlaceholderText("514")
        self._edit_port.setValidator(QIntValidator(1, 65535))

        for lbl_text, widget in [("전송 대상", None), ("Host", self._edit_host), ("Port", self._edit_port)]:
            if lbl_text == "전송 대상":
                continue
            lbl = QLabel(lbl_text)
            lbl.setFixedHeight(self.WIDGET_HEIGHT)
            lbl.setAlignment(Qt.AlignmentFlag.AlignVCenter)
            lay.addWidget(lbl)
            lay.addWidget(widget)
            if lbl_text == "Host":
                lay.addSpacing(4)
        return grp

    def _make_offset_group(self) -> QGroupBox:
        grp = QGroupBox("날짜 오프셋")
        lay = QHBoxLayout(grp)
        lay.setContentsMargins(12, 8, 12, 8)
        lay.setSpacing(4)
        lay.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self._btn_plus = QPushButton("+")
        self._btn_plus.setFixedSize(self.SIGN_BTN_W, self.SIGN_BTN_H)
        self._btn_plus.setFont(self._sign_font())
        self._btn_plus.setCheckable(True)
        self._btn_plus.setChecked(True)

        self._btn_minus = QPushButton("-")
        self._btn_minus.setFixedSize(self.SIGN_BTN_W, self.SIGN_BTN_H)
        self._btn_minus.setFont(self._sign_font())
        self._btn_minus.setCheckable(True)

        self._sign_group = QButtonGroup(self)
        self._sign_group.setExclusive(True)
        self._sign_group.addButton(self._btn_plus)
        self._sign_group.addButton(self._btn_minus)

        self._spin_offset = QSpinBox()
        self._spin_offset.setRange(0, self.MAX_OFFSET_DAYS)
        self._spin_offset.setValue(self.DEFAULT_OFFSET)
        self._spin_offset.setFixedSize(68, self.WIDGET_HEIGHT)

        lbl_day = QLabel("일")
        lbl_day.setFixedHeight(self.WIDGET_HEIGHT)
        lbl_day.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        lay.addWidget(self._btn_plus)
        lay.addWidget(self._btn_minus)
        lay.addSpacing(4)
        lay.addWidget(self._spin_offset)
        lay.addWidget(lbl_day)
        return grp

    def _make_interval_group(self) -> QGroupBox:
        grp = QGroupBox("전송 간격")
        lay = QHBoxLayout(grp)
        lay.setContentsMargins(12, 8, 12, 8)
        lay.setSpacing(6)
        lay.setAlignment(Qt.AlignmentFlag.AlignVCenter)

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
        self._sign_group.buttonToggled.connect(lambda _btn, _chk: self._emit_offset())
        self._spin_offset.valueChanged.connect(self._emit_offset)
        self._spin_interval.valueChanged.connect(
            lambda v: self.interval_changed.emit(v / 1000.0)
        )

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
        return 1 if self._btn_plus.isChecked() else -1

    def get_offset_days(self) -> int:
        return self._spin_offset.value()

    def get_interval_seconds(self) -> float:
        return self._spin_interval.value() / 1000.0
