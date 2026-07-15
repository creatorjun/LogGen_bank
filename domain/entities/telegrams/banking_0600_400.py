# domain/entities/telegrams/banking_0600_400.py
from dataclasses import dataclass


@dataclass
class Banking0600400Body:
    trs_ymd: str
    bank_cod2: str
    actnum: str
    act_nm: str
    rrn: str
    res_reg_no_chk_yn: str
    socact_nm: str
    bank_cod_3: str
    resv2: str
    co_use_inf: str
    hngl_use_inf: str
    conn_bank_resv: str

    FIELD_LENGTHS: tuple = (4, 2, 15, 22, 13, 2, 20, 3, 20, 20, 1, 4)
    RECORD_END: str = "@@"

    def to_raw(self) -> str:
        values = [
            self.trs_ymd, self.bank_cod2, self.actnum, self.act_nm,
            self.rrn, self.res_reg_no_chk_yn, self.socact_nm,
            self.bank_cod_3, self.resv2, self.co_use_inf,
            self.hngl_use_inf, self.conn_bank_resv,
        ]
        raw = "".join(
            v.ljust(length) for v, length in zip(values, self.FIELD_LENGTHS)
        )
        return raw + self.RECORD_END
