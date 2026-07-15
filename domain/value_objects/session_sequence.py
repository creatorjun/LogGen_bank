# domain/value_objects/session_sequence.py

MAX_SEQUENCE: int = 999999


class SessionSequence:
    def __init__(self) -> None:
        self._counters: dict[str, int] = {}

    def next(self, key: str) -> int:
        current = self._counters.get(key, 0)
        next_val = current + 1
        if next_val > MAX_SEQUENCE:
            next_val = 1
        self._counters[key] = next_val
        return next_val

    def reset(self, key: str) -> None:
        self._counters[key] = 0

    def reset_all(self) -> None:
        self._counters.clear()
