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

    LOG_PK_LEN: int = 15
    SERVER_ID_LEN: int = 20
    INSTANCE_ID_LEN: int = 12
    LOG_DATE_LEN: int = 8
    LOG_TIME_LEN: int = 6
    UNIQUE_KEY_LEN: int = 5
    TELEGRAM_ID_LEN: int = 10
    SR_TYPE_LEN: int = 5
    HEADER_IDENT: str = "/"

    def to_raw(self) -> str:
        return (
            "["
            + self.log_pk.ljust(self.LOG_PK_LEN)
            + self.server_id.ljust(self.SERVER_ID_LEN)
            + self.instance_id.ljust(self.INSTANCE_ID_LEN)
            + self.log_date.ljust(self.LOG_DATE_LEN)
            + self.log_time.ljust(self.LOG_TIME_LEN)
            + self.unique_key.ljust(self.UNIQUE_KEY_LEN)
            + self.telegram_id.ljust(self.TELEGRAM_ID_LEN)
            + self.sr_type.ljust(self.SR_TYPE_LEN)
            + self.HEADER_IDENT
        )
