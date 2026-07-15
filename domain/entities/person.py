# domain/entities/person.py
from dataclasses import dataclass


@dataclass
class Person:
    name: str
    rrn: str

    log_pk: str
    entr_cod: str
    server_id: str
    instance_id: str
    bank_cod: str
    bank_cod_3: str
    bank_resp_cod: str
    dfmt_actnum: str
    bbk_pwd: str
    pwd_mrk: str
    dps_act: str
    dps_bank_cod: str
    dps_bank_cod_3: str
    dpsr_nm: str
    bank_tlgrm_num: str

    card_number: str
    card_expiry: str
    track: str
    tid_prefix: str
    br_num: str
    trs_amt: str
