# presentation/widgets/log_preview.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QTextEdit, QLabel
from PyQt6.QtGui import QFont


class LogPreview(QWidget):
    FONT_FAMILY: str = "Courier New"
    FONT_SIZE: int = 10

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        group = QGroupBox("생성된 로그 미리보기")
        inner = QVBoxLayout(group)

        self._text_edit = QTextEdit()
        self._text_edit.setReadOnly(True)
        self._text_edit.setFont(QFont(self.FONT_FAMILY, self.FONT_SIZE))
        self._label_length = QLabel("Byte 길이: 0")

        inner.addWidget(self._text_edit)
        inner.addWidget(self._label_length)
        layout.addWidget(group)

    def set_log(self, raw_log: str) -> None:
        self._text_edit.setPlainText(raw_log)
        byte_len = len(raw_log.encode("euc-kr", errors="replace"))
        self._label_length.setText(f"Byte 길이: {byte_len}")
