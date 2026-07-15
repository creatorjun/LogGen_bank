# domain/ports/log_sender_port.py
from abc import ABC, abstractmethod


class LogSenderPort(ABC):
    @abstractmethod
    async def send(self, host: str, port: int, payload: bytes) -> bool:
        ...
