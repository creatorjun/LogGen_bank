# presentation/widgets/log_preview.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLabel
from PyQt6.QtCore import Qt


class LogPreview(QWidget):
    MAX_LINES: int = 500

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._build_ui()
        self._line_count: int = 0

    def _build_ui(self) -> None:
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(4)

        self._lbl_count = QLabel("0 건")
        self._lbl_count.setAlignment(Qt.AlignmentFlag.AlignRight)

        self._text_edit = QTextEdit()
        self._text_edit.setReadOnly(True)
        self._text_edit.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)

        lay.addWidget(self._lbl_count)
        lay.addWidget(self._text_edit, stretch=1)

    def append_log(self, raw_log: str, success: bool) -> None:
        if self._line_count >= self.MAX_LINES:
            self._text_edit.clear()
            self._line_count = 0

        prefix = "[OK] " if success else "[ERR]"
        self._text_edit.append(f"{prefix} {raw_log}")
        self._line_count += 1
        self._lbl_count.setText(f"{self._line_count} 건")

    def get_all_text(self) -> str:
        return self._text_edit.toPlainText()

    def clear(self) -> None:
        self._text_edit.clear()
        self._line_count = 0
        self._lbl_count.setText("0 건")
