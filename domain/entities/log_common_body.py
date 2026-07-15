# domain/entities/log_common_body.py
from dataclasses import dataclass


@dataclass
class LogCommonBody:
    dsc_cod: str
    entr_cod: str
    bank_cod: str
    msg_cod: str
    bz_sctn: str
    trsm_numtm: str
    tlgrm_num: str
    trms_ymd: str
    trms_hms: str
    resp_cod: str
    bank_resp_cod: str
    inq_ymd: str
    inq_num: str
    bank_tlgrm_num: str
    bank_cod_3: str
    resv: str

    FIELD_LENGTHS: tuple = (
        9, 8, 2, 4, 3, 1, 6, 8, 6, 4, 4, 8, 6, 15, 3, 13
    )
    RECORD_END: str = "]"

    def to_raw(self) -> str:
        values = [
            self.dsc_cod, self.entr_cod, self.bank_cod, self.msg_cod,
            self.bz_sctn, self.trsm_numtm, self.tlgrm_num, self.trms_ymd,
            self.trms_hms, self.resp_cod, self.bank_resp_cod, self.inq_ymd,
            self.inq_num, self.bank_tlgrm_num, self.bank_cod_3, self.resv,
        ]
        raw = "".join(
            v.ljust(l) for v, l in zip(values, self.FIELD_LENGTHS)
        )
        return raw + self.RECORD_END
