# domain/entities/telegrams/banking_0400_100.py
from dataclasses import dataclass


@dataclass
class Banking0400100Body:
    orgn_trs_tlgrm_num: str
    dfmt_actnum: str
    dps_actnum: str
    req_amt: str
    dps_bank_cod: str
    noml_dlng_amt: str
    dlng_imp_amt: str
    ptil_dlng_cnt: str
    ptil_dlng_num: str
    othr_bank_tlgrm_num: str
    dps_imp_ntc_amt: str
    err_cod: str
    dps_bank_cod_3: str
    resv2: str

    FIELD_LENGTHS: tuple = (
        6, 15, 15, 13, 2, 13, 13, 2, 2, 6, 9, 3, 3, 12
    )
    RECORD_END: str = "@@"

    def to_raw(self) -> str:
        values = [
            self.orgn_trs_tlgrm_num, self.dfmt_actnum, self.dps_actnum,
            self.req_amt, self.dps_bank_cod, self.noml_dlng_amt,
            self.dlng_imp_amt, self.ptil_dlng_cnt, self.ptil_dlng_num,
            self.othr_bank_tlgrm_num, self.dps_imp_ntc_amt,
            self.err_cod, self.dps_bank_cod_3, self.resv2,
        ]
        raw = "".join(
            v.ljust(length) for v, length in zip(values, self.FIELD_LENGTHS)
        )
        return raw + self.RECORD_END
