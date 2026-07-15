# domain/entities/telegrams/banking_0100_100.py
from dataclasses import dataclass


@dataclass
class Banking0100100Body:
    dfmt_actnum: str
    bbk_pwd: str
    pwd_mrk: str
    outamt_amt: str
    outamt_aft_rmd_mrk: str
    dfmt_aft_rmd: str
    dps_bank_cod: str
    dps_act: str
    coms: str
    trsf_time: str
    dpsr_nm: str
    cms_cod: str
    rrn: str
    autrsf_sctn: str
    dps_act_inf: str
    dps_bank_cod_3: str
    resv2: str

    FIELD_LENGTHS: tuple = (
        15, 8, 6, 13, 1, 13, 2, 15, 9, 6, 20, 16, 13, 2, 20, 3, 38
    )
    RECORD_END: str = "@@"

    def to_raw(self) -> str:
        values = [
            self.dfmt_actnum, self.bbk_pwd, self.pwd_mrk, self.outamt_amt,
            self.outamt_aft_rmd_mrk, self.dfmt_aft_rmd, self.dps_bank_cod,
            self.dps_act, self.coms, self.trsf_time, self.dpsr_nm,
            self.cms_cod, self.rrn, self.autrsf_sctn, self.dps_act_inf,
            self.dps_bank_cod_3, self.resv2,
        ]
        raw = "".join(
            v.ljust(l) for v, l in zip(values, self.FIELD_LENGTHS)
        )
        return raw + self.RECORD_END
