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

    def to_raw(self) -> str:
        return (
            self.dsc_cod.ljust(9)
            + self.entr_cod.ljust(8)
            + self.bank_cod.ljust(2)
            + self.msg_cod.ljust(4)
            + self.bz_sctn.ljust(3)
            + self.trsm_numtm[:1]
            + self.tlgrm_num.zfill(6)
            + self.trms_ymd
            + self.trms_hms
            + self.resp_cod.ljust(4)
            + self.bank_resp_cod.ljust(4)
            + self.inq_ymd
            + self.inq_num.zfill(6)
            + self.bank_tlgrm_num.ljust(15)
            + self.bank_cod_3.ljust(3)
            + self.resv.ljust(13)
            + "]"
        )
