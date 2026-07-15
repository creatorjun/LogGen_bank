# application/dto/log_result_dto.py
from dataclasses import dataclass


@dataclass(frozen=True)
class LogResultDto:
    raw_log: str
    byte_length: int
    success: bool
    message: str
