# domain/entities/log_header.py
from dataclasses import dataclass


@dataclass
class LogHeader:
    log_pk: str
    server_id: str
    instance_id: str
    log_date: str
    log_time: str
    unique_key: str
    telegram_id: str
    sr_type: str

    def to_raw(self) -> str:
        return (
            "["
            + self.log_pk.ljust(14)
            + " "
            + self.server_id.ljust(20)
            + self.instance_id.ljust(12)
            + self.log_date
            + self.log_time
            + self.unique_key.ljust(5)
            + self.telegram_id.ljust(10)
            + self.sr_type.ljust(5)
            + "/"
        )
