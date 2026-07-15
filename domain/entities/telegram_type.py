# domain/entities/telegram_type.py
from enum import StrEnum


class TelegramType(StrEnum):
    BANKING_0100_100 = "A1-0100-100"
    BANKING_0400_100 = "A1-0400-100"
    BANKING_0600_400 = "A1-0600-400"
    CARD_NIT_0200 = "C3-NIT-0200"
