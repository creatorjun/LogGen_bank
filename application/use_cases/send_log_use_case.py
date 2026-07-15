# application/use_cases/send_log_use_case.py
from domain.ports.log_sender_port import LogSenderPort


class SendLogUseCase:
    ENCODING: str = "utf-8"

    def __init__(self, sender: LogSenderPort) -> None:
        self._sender = sender

    async def execute(self, host: str, port: int, log: str) -> bool:
        payload = log.encode(self.ENCODING, errors="replace")
        return await self._sender.send(host, port, payload)
