# application/services/transmission_loop.py
import asyncio
from dataclasses import dataclass
from domain.entities.person import Person
from domain.entities.telegram_type import TelegramType
from domain.value_objects.date_offset import DateOffset
from application.use_cases.generate_log_use_case import GenerateLogUseCase
from application.use_cases.send_log_use_case import SendLogUseCase
from application.services.log_file_writer import LogFileWriter
from typing import Callable


@dataclass
class TransmissionStats:
    total: int = 0
    failed: int = 0
    current_person: str = ""
    current_telegram_type: str = ""


class TransmissionLoop:
    DEFAULT_INTERVAL: float = 0.05

    def __init__(
        self,
        persons: list[Person],
        telegram_types: list[TelegramType],
        generate_use_case: GenerateLogUseCase,
        send_use_case: SendLogUseCase,
        log_file_writer: LogFileWriter,
        on_log_generated: Callable[[str, bool], None] | None = None,
        on_stats_updated: Callable[[TransmissionStats], None] | None = None,
    ) -> None:
        self._persons = persons
        self._telegram_types = telegram_types
        self._generate = generate_use_case
        self._send = send_use_case
        self._writer = log_file_writer
        self._on_log_generated = on_log_generated
        self._on_stats_updated = on_stats_updated

        self._combos: list[tuple[Person, TelegramType]] = [
            (p, t) for p in persons for t in telegram_types
        ]
        self._combo_index: int = 0
        self._interval: float = self.DEFAULT_INTERVAL
        self._host: str = "127.0.0.1"
        self._port: int = 514
        self._date_offset: DateOffset = DateOffset(sign=1, days=0)

        self._run_event = asyncio.Event()
        self._task: asyncio.Task | None = None
        self._stats = TransmissionStats()

    @property
    def stats(self) -> TransmissionStats:
        return self._stats

    @property
    def is_running(self) -> bool:
        return self._run_event.is_set()

    def set_interval(self, seconds: float) -> None:
        self._interval = max(0.001, seconds)

    def set_target(self, host: str, port: int) -> None:
        self._host = host
        self._port = port

    def set_date_offset(self, sign: int, days: int) -> None:
        self._date_offset = DateOffset(sign=sign, days=days)

    def start(self) -> None:
        self._run_event.set()
        if self._task is None or self._task.done():
            self._writer.open_session()
            self._stats = TransmissionStats()
            self._task = asyncio.ensure_future(self._loop())

    def pause(self) -> None:
        self._run_event.clear()

    def resume(self) -> None:
        self._run_event.set()

    async def stop(self) -> None:
        self._run_event.clear()
        if self._task and not self._task.done():
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
            except Exception:
                pass
        self._task = None
        self._writer.close_session()

    def _next_combo(self) -> tuple[Person, TelegramType]:
        combo = self._combos[self._combo_index % len(self._combos)]
        self._combo_index += 1
        return combo

    async def _loop(self) -> None:
        while True:
            await self._run_event.wait()
            person, telegram_type = self._next_combo()
            self._stats.current_person = person.name
            self._stats.current_telegram_type = str(telegram_type)

            try:
                raw_log = self._generate.execute(person, telegram_type)
                success = await self._send.execute(self._host, self._port, raw_log)
                if success:
                    await self._writer.write(raw_log)
                    self._stats.total += 1
                else:
                    self._stats.failed += 1
                if self._on_log_generated:
                    self._on_log_generated(raw_log, success)
            except asyncio.CancelledError:
                raise
            except OSError:
                self._stats.failed += 1
                if self._on_log_generated:
                    self._on_log_generated("", False)
            except Exception:
                self._stats.failed += 1
                if self._on_log_generated:
                    self._on_log_generated("", False)

            if self._on_stats_updated:
                self._on_stats_updated(self._stats)

            await asyncio.sleep(self._interval)
