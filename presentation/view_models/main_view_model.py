# presentation/view_models/main_view_model.py
import asyncio
from PyQt6.QtCore import QObject, pyqtSignal
from domain.entities.person import Person
from domain.entities.telegram_type import TelegramType
from domain.value_objects.session_sequence import SessionSequence
from domain.value_objects.date_offset import DateOffset
from application.services.transmission_loop import TransmissionLoop, TransmissionStats
from application.services.log_file_writer import LogFileWriter
from application.use_cases.generate_log_use_case import GenerateLogUseCase
from application.use_cases.send_log_use_case import SendLogUseCase
from application.services.person_telegram_mapper import PersonTelegramMapper
from infrastructure.network.udp_sender import UdpSender


class MainViewModel(QObject):
    log_appended = pyqtSignal(str, bool)
    stats_updated = pyqtSignal(TransmissionStats)
    state_changed = pyqtSignal(str)
    send_result = pyqtSignal(bool, str)

    STATE_IDLE: str = "IDLE"
    STATE_RUNNING: str = "RUNNING"
    STATE_PAUSED: str = "PAUSED"

    def __init__(self, persons: list[Person], parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._persons = persons
        self._host: str = "127.0.0.1"
        self._port: int = 514
        self._date_offset: DateOffset = DateOffset(sign=1, days=0)
        self._state: str = self.STATE_IDLE
        self._loop: TransmissionLoop | None = None
        self._build_loop()

    def _build_loop(self) -> None:
        sequence = SessionSequence()
        mapper = PersonTelegramMapper(sequence=sequence, date_offset=self._date_offset)
        generate_uc = GenerateLogUseCase(mapper)
        send_uc = SendLogUseCase(UdpSender())
        writer = LogFileWriter()
        self._loop = TransmissionLoop(
            persons=self._persons,
            telegram_types=list(TelegramType),
            generate_use_case=generate_uc,
            send_use_case=send_uc,
            log_file_writer=writer,
            on_log_generated=self._on_log_generated,
            on_stats_updated=self._on_stats_updated,
        )

    def _on_log_generated(self, raw_log: str, success: bool) -> None:
        self.log_appended.emit(raw_log, success)
        msg = "전송 성공" if success else "전송 실패"
        self.send_result.emit(success, msg)

    def _on_stats_updated(self, stats: TransmissionStats) -> None:
        self.stats_updated.emit(stats)

    def update_persons(self, persons: list[Person]) -> None:
        self._persons = persons
        was_running = self._loop.is_running if self._loop else False
        asyncio.ensure_future(self._restart_loop(was_running))

    async def _restart_loop(self, resume: bool) -> None:
        if self._loop:
            await self._loop.stop()
        self._build_loop()
        if self._loop:
            self._loop.set_target(self._host, self._port)
            if resume:
                self._loop.start()
                self._set_state(self.STATE_RUNNING)
            else:
                self._set_state(self.STATE_IDLE)

    def set_target(self, host: str, port: int) -> None:
        self._host = host
        self._port = port
        if self._loop:
            self._loop.set_target(host, port)

    def set_interval(self, seconds: float) -> None:
        if self._loop:
            self._loop.set_interval(seconds)

    def set_date_offset(self, sign: int, days: int) -> None:
        self._date_offset = DateOffset(sign=sign, days=days)
        if self._loop:
            self._loop.set_date_offset(sign, days)

    def start(self) -> None:
        if self._loop and self._state == self.STATE_IDLE:
            self._loop.set_target(self._host, self._port)
            self._loop.start()
            self._set_state(self.STATE_RUNNING)

    def stop(self) -> None:
        if self._loop and self._state != self.STATE_IDLE:
            asyncio.ensure_future(self._do_stop())

    async def _do_stop(self) -> None:
        if self._loop:
            await self._loop.stop()
        self._set_state(self.STATE_IDLE)

    def _set_state(self, state: str) -> None:
        self._state = state
        self.state_changed.emit(state)

    @property
    def state(self) -> str:
        return self._state
