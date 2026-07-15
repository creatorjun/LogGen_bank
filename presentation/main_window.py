# presentation/main_window.py
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from presentation.widgets.control_panel import ControlPanel
from presentation.widgets.log_preview import LogPreview
from presentation.widgets.status_bar import AppStatusBar
from presentation.view_models.main_view_model import MainViewModel
from infrastructure.builders.log_builder import LogBuilder
from infrastructure.network.tcp_sender import TcpSender
from application.use_cases.generate_log_use_case import GenerateLogUseCase
from application.use_cases.send_log_use_case import SendLogUseCase


class MainWindow(QMainWindow):
    WINDOW_TITLE: str = "LogGen Bank - 금융거래 TR 로그 생성기"
    WINDOW_MIN_WIDTH: int = 900
    WINDOW_MIN_HEIGHT: int = 700

    def __init__(self) -> None:
        super().__init__()
        self._init_dependencies()
        self._init_ui()
        self._connect_signals()

    def _init_dependencies(self) -> None:
        builder = LogBuilder()
        sender = TcpSender()
        generate_uc = GenerateLogUseCase(builder)
        send_uc = SendLogUseCase(sender)
        self._view_model = MainViewModel(generate_uc, send_uc)

    def _init_ui(self) -> None:
        self.setWindowTitle(self.WINDOW_TITLE)
        self.setMinimumSize(self.WINDOW_MIN_WIDTH, self.WINDOW_MIN_HEIGHT)

        central = QWidget()
        layout = QVBoxLayout(central)
        layout.setSpacing(8)
        layout.setContentsMargins(12, 12, 12, 12)

        self._control_panel = ControlPanel()
        self._log_preview = LogPreview()
        self._status_bar = AppStatusBar()

        layout.addWidget(self._control_panel)
        layout.addWidget(self._log_preview, stretch=1)
        self.setStatusBar(self._status_bar)
        self.setCentralWidget(central)

    def _connect_signals(self) -> None:
        self._control_panel.generate_requested.connect(self._on_generate)
        self._control_panel.send_requested.connect(self._on_send)
        self._view_model.log_generated.connect(self._log_preview.set_log)
        self._view_model.send_result.connect(self._status_bar.show_result)

    def _on_generate(self, telegram_type: str, params: dict) -> None:
        self._view_model.generate(telegram_type, params)

    def _on_send(self, host: str, port: int) -> None:
        self._view_model.send(host, port)
