# application/services/token_resolver.py
from datetime import datetime
from domain.entities.person import Person
from domain.value_objects.date_offset import DateOffset
from domain.value_objects.session_sequence import SessionSequence


class TokenResolutionError(Exception):
    pass


class FieldLengthError(Exception):
    pass


class TokenResolver:
    def __init__(
        self,
        sequence: SessionSequence,
        date_offset: DateOffset,
    ) -> None:
        self._sequence = sequence
        self._date_offset = date_offset

    def resolve(self, person: Person) -> dict[str, str]:
        now = datetime.now()
        yyyymmdd = self._date_offset.resolve_yyyymmdd()
        hhmmss = now.strftime("%H%M%S")
        mmdd = self._date_offset.resolve_mmdd()

        tid_seq = self._sequence.next_tid_seq()
        tid = person.tid_prefix + yyyymmdd + tid_seq

        tokens: dict[str, str] = {
            "LOG_DATE": yyyymmdd,
            "LOG_TIME": hhmmss,
            "TRMS_YMD": yyyymmdd,
            "TRMS_HMS": hhmmss,
            "INQ_YMD": yyyymmdd,
            "TRS_YMD_MMDD": mmdd,
            "TLGRM_NUM": self._sequence.next_tlgrm_num(),
            "INQ_NUM": self._sequence.next_inq_num(),
            "LOG_PK_SEQ": self._sequence.next_log_pk_seq(person.name),
            "TID_SEQ": tid_seq,
            "TID": tid,
            "NAME": person.name,
            "RRN": person.rrn,
            "LOG_PK": person.log_pk,
            "ENTR_COD": person.entr_cod,
            "SERVER_ID": person.server_id,
            "INSTANCE_ID": person.instance_id,
            "BANK_COD": person.bank_cod,
            "BANK_COD_3": person.bank_cod_3,
            "BANK_RESP_COD": person.bank_resp_cod,
            "DFMT_ACTNUM": person.dfmt_actnum,
            "BBK_PWD": person.bbk_pwd,
            "PWD_MRK": person.pwd_mrk,
            "DPS_ACT": person.dps_act,
            "DPS_BANK_COD": person.dps_bank_cod,
            "DPS_BANK_COD_3": person.dps_bank_cod_3,
            "DPSR_NM": person.dpsr_nm,
            "BANK_TLGRM_NUM": person.bank_tlgrm_num,
            "CARD_NUMBER": person.card_number,
            "CARD_EXPIRY": person.card_expiry,
            "TRACK": person.track,
            "TID_PREFIX": person.tid_prefix,
            "BR_NUM": person.br_num,
            "TRS_AMT": person.trs_amt,
        }
        return tokens
