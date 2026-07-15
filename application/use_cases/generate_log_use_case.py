# application/use_cases/generate_log_use_case.py
from domain.entities.person import Person
from domain.entities.telegram_type import TelegramType
from application.services.person_telegram_mapper import PersonTelegramMapper


class GenerateLogUseCase:
    def __init__(self, mapper: PersonTelegramMapper) -> None:
        self._mapper = mapper

    def execute(self, person: Person, telegram_type: TelegramType) -> str:
        return self._mapper.build_log(person, telegram_type)
