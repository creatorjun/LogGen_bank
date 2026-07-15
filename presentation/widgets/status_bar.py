# presentation/widgets/status_bar.py
from PyQt6.QtWidgets import QStatusBar
from PyQt6.QtGui import QColor
from PyQt6.QtCore import QTimer


class AppStatusBar(QStatusBar):
    MSG_TIMEOUT_MS: int = 5000
    COLOR_SUCCESS: str = "#2ecc71"
    COLOR_FAILURE: str = "#e74c3c"

    def show_result(self, success: bool, message: str) -> None:
        color = self.COLOR_SUCCESS if success else self.COLOR_FAILURE
        self.setStyleSheet(f"background-color: {color}; color: white;")
        self.showMessage(message, self.MSG_TIMEOUT_MS)
        QTimer.singleShot(
            self.MSG_TIMEOUT_MS,
            lambda: self.setStyleSheet("")
        )
