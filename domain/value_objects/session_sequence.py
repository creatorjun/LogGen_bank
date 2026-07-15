# domain/value_objects/session_sequence.py

MAX_SEQ: int = 999999
MAX_TLGRM: int = 999999
MAX_INQ: int = 999999
MAX_TID: int = 9999


class SessionSequence:
    def __init__(self) -> None:
        self._tlgrm_num: int = 0
        self._inq_num: int = 0
        self._tid_seq: int = 0
        self._log_pk_seq: dict[str, int] = {}

    def next_tlgrm_num(self) -> str:
        self._tlgrm_num += 1
        if self._tlgrm_num > MAX_TLGRM:
            self._tlgrm_num = 1
        return str(self._tlgrm_num).zfill(6)

    def next_inq_num(self) -> str:
        self._inq_num += 1
        if self._inq_num > MAX_INQ:
            self._inq_num = 1
        return str(self._inq_num).zfill(6)

    def next_tid_seq(self) -> str:
        self._tid_seq += 1
        if self._tid_seq > MAX_TID:
            self._tid_seq = 1
        return str(self._tid_seq).zfill(4)

    def next_log_pk_seq(self, person_name: str) -> str:
        current = self._log_pk_seq.get(person_name, 0) + 1
        if current > MAX_SEQ:
            current = 1
        self._log_pk_seq[person_name] = current
        return str(current).zfill(6)

    def reset_all(self) -> None:
        self._tlgrm_num = 0
        self._inq_num = 0
        self._tid_seq = 0
        self._log_pk_seq.clear()
