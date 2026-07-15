# presentation/main_window.py
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QSplitter
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCloseEvent
from presentation.styles.fluent import FLUENT_STYLESHEET
from presentation.widgets.control_panel import ControlPanel
from presentation.widgets.transmission_control import TransmissionControl
from presentation.widgets.log_preview import LogPreview
from presentation.widgets.stats_panel import StatsPanel
from presentation.widgets.status_bar import AppStatusBar
from presentation.widgets.person_editor_dialog import PersonEditorDialog
from infrastructure.data.person_fixture import PERSONS
from domain.entities.person import Person
import copy


class MainWindow(QMainWindow):
    WINDOW_TITLE: str = "LogGen Bank — 금융거래 TR 로그 생성기"
    WINDOW_MIN_WIDTH: int = 1000
    WINDOW_MIN_HEIGHT: int = 660

    def __init__(self) -> None:
        super().__init__()
        self.setStyleSheet(FLUENT_STYLESHEET)
        self._persons: list[Person] = [copy.copy(p) for p in PERSONS]
        self._build_ui()
        self._connect_signals()

    def _build_ui(self) -> None:
        self.setWindowTitle(self.WINDOW_TITLE)
        self.setMinimumSize(self.WINDOW_MIN_WIDTH, self.WINDOW_MIN_HEIGHT)

        central = QWidget()
        root = QVBoxLayout(central)
        root.setContentsMargins(12, 12, 12, 8)
        root.setSpacing(8)

        self._control_panel = ControlPanel()
        root.addWidget(self._control_panel)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        self._log_preview = LogPreview()
        self._stats_panel = StatsPanel()
        splitter.addWidget(self._log_preview)
        splitter.addWidget(self._stats_panel)
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 1)
        root.addWidget(splitter, stretch=1)

        self._tx_control = TransmissionControl()
        root.addWidget(self._tx_control)

        self._status_bar = AppStatusBar()
        self.setStatusBar(self._status_bar)
        self.setCentralWidget(central)

    def _connect_signals(self) -> None:
        self._tx_control.person_edit_requested.connect(self._open_person_editor)

    def _open_person_editor(self) -> None:
        dlg = PersonEditorDialog(self._persons, parent=self)
        dlg.persons_updated.connect(self._on_persons_updated)
        dlg.exec()

    def _on_persons_updated(self, persons: list[Person]) -> None:
        self._persons = persons

    def closeEvent(self, event: QCloseEvent) -> None:
        event.accept()

    @property
    def control_panel(self) -> ControlPanel:
        return self._control_panel

    @property
    def tx_control(self) -> TransmissionControl:
        return self._tx_control

    @property
    def log_preview(self) -> LogPreview:
        return self._log_preview

    @property
    def stats_panel(self) -> StatsPanel:
        return self._stats_panel

    @property
    def status_bar_widget(self) -> AppStatusBar:
        return self._status_bar

    @property
    def persons(self) -> list[Person]:
        return self._persons
