# infrastructure/builders/log_builder.py
from domain.entities.person import Person
from domain.entities.telegram_type import TelegramType
from domain.ports.log_builder_port import LogBuilderPort
from application.services.person_telegram_mapper import PersonTelegramMapper
from domain.value_objects.date_offset import DateOffset
from domain.value_objects.session_sequence import SessionSequence


class LogBuilder(LogBuilderPort):
    def __init__(
        self,
        mapper: PersonTelegramMapper,
    ) -> None:
        self._mapper = mapper

    def build(self, telegram_type: TelegramType, params: dict) -> str:
        person: Person = params["person"]
        return self._mapper.build_log(person, telegram_type)
