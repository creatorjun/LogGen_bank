# domain/entities/telegrams/card_nit_0200.py
from dataclasses import dataclass


@dataclass
class CardNit0200BizBody:
    wcc: str
    track: str
    inst_mtcnt: str
    srvc_fee: str
    tex: str
    trs_amt: str
    org_apv_num: str
    trs_apvdt: str
    org_num: str
    bbk_pwd: str
    rrn: str
    pin_num: str
    domain: str
    ip_adr: str

    FIELD_LENGTHS: tuple = (
        1, 42, 2, 9, 9, 9, 8, 6, 12, 10, 13, 16, 30, 20
    )
    RECORD_END: str = "@@"

    def to_raw(self) -> str:
        values = [
            self.wcc, self.track, self.inst_mtcnt, self.srvc_fee,
            self.tex, self.trs_amt, self.org_apv_num, self.trs_apvdt,
            self.org_num, self.bbk_pwd, self.rrn, self.pin_num,
            self.domain, self.ip_adr,
        ]
        raw = "".join(
            v.ljust(length) for v, length in zip(values, self.FIELD_LENGTHS)
        )
        return raw + self.RECORD_END
