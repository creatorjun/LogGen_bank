# domain/entities/telegrams/card_nit_0200.py
from dataclasses import dataclass


@dataclass
class CardNit0200CommonBody:
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
            self.tlgrm_len, self.tlgrm_txt, self.tid, self.tlgrm_gbn,
            self.trs_sctn, self.ter_gbn, self.ter_num, self.br_num,
        ]
        raw = "".join(
            v.ljust(l) for v, l in zip(values, self.FIELD_LENGTHS)
        )
        return raw + self.RECORD_END


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
            v.ljust(l) for v, l in zip(values, self.FIELD_LENGTHS)
        )
        return raw + self.RECORD_END
