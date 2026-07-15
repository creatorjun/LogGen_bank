# domain/ports/log_builder_port.py
from abc import ABC, abstractmethod
from domain.entities.telegram_type import TelegramType


class LogBuilderPort(ABC):
    @abstractmethod
    def build(self, telegram_type: TelegramType, params: dict) -> str:
        ...
