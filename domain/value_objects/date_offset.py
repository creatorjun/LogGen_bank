# domain/value_objects/date_offset.py
from dataclasses import dataclass
from datetime import date, timedelta


@dataclass(frozen=True)
class DateOffset:
    sign: int
    days: int

    SIGN_POSITIVE: int = 1
    SIGN_NEGATIVE: int = -1

    def __post_init__(self) -> None:
        if self.sign not in (self.SIGN_POSITIVE, self.SIGN_NEGATIVE):
            raise ValueError(f"sign must be 1 or -1, got {self.sign}")
        if self.days < 0:
            raise ValueError(f"days must be >= 0, got {self.days}")

    def resolve_date(self) -> date:
        return date.today() + timedelta(days=self.sign * self.days)

    def resolve_yyyymmdd(self) -> str:
        return self.resolve_date().strftime("%Y%m%d")

    def resolve_mmdd(self) -> str:
        return self.resolve_date().strftime("%m%d")
