# presentation/view_models/main_view_model.py
import asyncio
from PyQt6.QtCore import QObject, pyqtSignal
from domain.entities.telegram_type import TelegramType
from application.use_cases.generate_log_use_case import GenerateLogUseCase
from application.use_cases.send_log_use_case import SendLogUseCase


class MainViewModel(QObject):
    log_generated = pyqtSignal(str)
    send_result = pyqtSignal(bool, str)

    def __init__(
        self,
        generate_uc: GenerateLogUseCase,
        send_uc: SendLogUseCase,
    ) -> None:
        super().__init__()
        self._generate_uc = generate_uc
        self._send_uc = send_uc
        self._current_log: str = ""

    def generate(self, telegram_type: str, params: dict) -> None:
        try:
            t_type = TelegramType(telegram_type)
            self._current_log = self._generate_uc.execute(t_type, params)
            self.log_generated.emit(self._current_log)
        except (ValueError, KeyError) as e:
            self.log_generated.emit(f"[ERROR] {e}")

    def send(self, host: str, port: int) -> None:
        if not self._current_log:
            self.send_result.emit(False, "전송할 로그가 없습니다. 먼저 생성하세요.")
            return
        asyncio.ensure_future(self._async_send(host, port))

    async def _async_send(self, host: str, port: int) -> None:
        success = await self._send_uc.execute(host, port, self._current_log)
        msg = "전송 성공" if success else "전송 실패 (연결 오류)"
        self.send_result.emit(success, msg)
