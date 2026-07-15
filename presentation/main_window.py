# presentation/main_window.py
import asyncio
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
from presentation.view_models.main_view_model import MainViewModel
from infrastructure.data.person_fixture import PERSONS
from application.services.transmission_loop import TransmissionStats
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
        self._view_model = MainViewModel(self._persons)
        self._closing: bool = False
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
        cp = self._control_panel
        tx = self._tx_control
        vm = self._view_model

        cp.target_changed.connect(vm.set_target)
        cp.interval_changed.connect(vm.set_interval)
        cp.offset_changed.connect(vm.set_date_offset)

        tx.start_requested.connect(self._on_start)
        tx.stop_requested.connect(self._on_stop)
        tx.copy_requested.connect(self._on_copy)
        tx.clear_requested.connect(self._log_preview.clear)
        tx.person_edit_requested.connect(self._open_person_editor)

        vm.log_appended.connect(self._log_preview.append_log)
        vm.stats_updated.connect(self._on_stats_updated)
        vm.state_changed.connect(self._on_state_changed)
        vm.send_result.connect(self._status_bar.show_result)

    def _on_start(self) -> None:
        self._view_model.start()

    def _on_stop(self) -> None:
        self._view_model.stop()

    def _on_copy(self) -> None:
        from PyQt6.QtWidgets import QApplication
        text = self._log_preview.get_all_text()
        if text:
            QApplication.clipboard().setText(text)
            self._status_bar.show_info("클립보드에 복사되었습니다")

    def _on_stats_updated(self, stats: TransmissionStats) -> None:
        self._stats_panel.update_stats(
            person=stats.current_person,
            telegram_type=stats.current_telegram_type,
            total=stats.total,
            failed=stats.failed,
            state=self._view_model.state,
        )

    def _on_state_changed(self, state: str) -> None:
        self._tx_control.set_running(state == MainViewModel.STATE_RUNNING)
        loop = self._view_model._loop
        self._stats_panel.update_stats(
            person=loop.stats.current_person if loop else "",
            telegram_type=loop.stats.current_telegram_type if loop else "",
            total=loop.stats.total if loop else 0,
            failed=loop.stats.failed if loop else 0,
            state=state,
        )
        msg_map = {
            MainViewModel.STATE_RUNNING: "전송 시작됨",
            MainViewModel.STATE_IDLE: "전송 중지됨",
        }
        if state in msg_map:
            self._status_bar.show_info(msg_map[state])

    def _open_person_editor(self) -> None:
        dlg = PersonEditorDialog(self._persons, parent=self)
        dlg.persons_updated.connect(self._on_persons_updated)
        dlg.exec()

    def _on_persons_updated(self, persons: list[Person]) -> None:
        self._persons = persons
        self._view_model.update_persons(persons)

    def closeEvent(self, event: QCloseEvent) -> None:
        if self._closing:
            event.accept()
            return
        self._closing = True
        loop = self._view_model._loop
        if loop and (loop.is_running or (loop._task and not loop._task.done())):
            event.ignore()
            asyncio.ensure_future(self._async_close())
        else:
            event.accept()

    async def _async_close(self) -> None:
        try:
            await self._view_model._loop.stop()
        except Exception:
            pass
        finally:
            self.close()

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
