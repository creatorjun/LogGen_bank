# presentation/widgets/status_bar.py
from PyQt6.QtWidgets import QStatusBar, QLabel
from PyQt6.QtGui import QColor
from PyQt6.QtCore import QTimer


class AppStatusBar(QStatusBar):
    COLOR_SUCCESS: str = "#107C10"
    COLOR_FAILURE: str = "#D13438"
    COLOR_INFO: str = "#0078D4"
    AUTO_CLEAR_MS: int = 5000

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._lbl = QLabel("준비")
        self.addWidget(self._lbl, 1)
        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(lambda: self.show_info("준비"))

    def show_result(self, success: bool, message: str) -> None:
        color = self.COLOR_SUCCESS if success else self.COLOR_FAILURE
        self._lbl.setStyleSheet(f"color: {color}; font-weight: 600;")
        self._lbl.setText(message)
        self._timer.start(self.AUTO_CLEAR_MS)

    def show_info(self, message: str) -> None:
        self._lbl.setStyleSheet(f"color: {self.COLOR_INFO};")
        self._lbl.setText(message)
