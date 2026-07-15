# application/use_cases/generate_log_use_case.py
from domain.entities.telegram_type import TelegramType
from domain.ports.log_builder_port import LogBuilderPort


class GenerateLogUseCase:
    def __init__(self, builder: LogBuilderPort) -> None:
        self._builder = builder

    def execute(self, telegram_type: TelegramType, params: dict) -> str:
        return self._builder.build(telegram_type, params)
