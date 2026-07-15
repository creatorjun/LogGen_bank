# domain/value_objects/session_sequence.py
from dataclasses import dataclass, field


@dataclass
class SessionSequence:
    _counters: dict[str, int] = field(default_factory=dict, init=False, repr=False)

    MAX_6: int = 999999
    MAX_3: int = 999
    MAX_2: int = 99

    def next_tlgrm_num(self) -> str:
        return self._next("tlgrm_num", self.MAX_6, 6)

    def next_inq_num(self) -> str:
        return self._next("inq_num", self.MAX_6, 6)

    def next_log_pk_seq(self, person_id: str) -> str:
        key = f"log_pk_seq_{person_id}"
        return self._next(key, self.MAX_3, 3)

    def next_tid_seq(self) -> str:
        return self._next("tid_seq", self.MAX_2, 2)

    def _next(self, key: str, max_val: int, width: int) -> str:
        current = self._counters.get(key, 0) + 1
        if current > max_val:
            current = 1
        self._counters[key] = current
        return str(current).zfill(width)

    def reset(self) -> None:
        self._counters.clear()
