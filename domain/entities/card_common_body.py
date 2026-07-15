# domain/entities/card_common_body.py
from dataclasses import dataclass


@dataclass
class CardCommonBody:
    tlgrm_len: str
    tlgrm_txt: str
    tid: str
    tlgrm_gbn: str
    trs_sctn: str
    ter_gbn: str
    ter_num: str
    br_num: str

    FIELD_LENGTHS: tuple = (4, 3, 20, 4, 2, 2, 10, 10)
    RECORD_END: str = "]"

    def to_raw(self) -> str:
        values = [
            self.tlgrm_len,
            self.tlgrm_txt,
            self.tid,
            self.tlgrm_gbn,
            self.trs_sctn,
            self.ter_gbn,
            self.ter_num,
            self.br_num,
        ]
        raw = "".join(
            v.ljust(length) for v, length in zip(values, self.FIELD_LENGTHS)
        )
        return raw + self.RECORD_END
