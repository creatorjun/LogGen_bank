# application/services/person_telegram_mapper.py
from datetime import datetime
from domain.entities.person import Person
from domain.entities.telegram_type import TelegramType
from domain.entities.log_header import LogHeader
from domain.entities.log_common_body import LogCommonBody
from domain.entities.card_common_body import CardCommonBody
from domain.entities.telegrams.banking_0100_100 import Banking0100100Body
from domain.entities.telegrams.banking_0400_100 import Banking0400100Body
from domain.entities.telegrams.banking_0600_400 import Banking0600400Body
from domain.entities.telegrams.card_nit_0200 import CardNit0200BizBody
from domain.value_objects.date_offset import DateOffset
from domain.value_objects.session_sequence import SessionSequence


class PersonTelegramMapper:
    TRSM_NUMTM: str = "1"
    RESP_COD: str = "    "
    RESV_BANKING: str = "             "
    SR_TYPE_MB: str = "MB"
    SR_TYPE_API: str = "API"

    def __init__(
        self,
        sequence: SessionSequence,
        date_offset: DateOffset,
    ) -> None:
        self._seq = sequence
        self._offset = date_offset

    def build_log(
        self,
        person: Person,
        telegram_type: TelegramType,
    ) -> str:
        now = datetime.now()
        yyyymmdd = self._offset.resolve_yyyymmdd()
        hhmmss = now.strftime("%H%M%S")
        mmdd = self._offset.resolve_mmdd()
        tlgrm_num = self._seq.next_tlgrm_num()
        inq_num = self._seq.next_inq_num()
        log_pk_seq = self._seq.next_log_pk_seq(person.name)
        tid_seq = self._seq.next_tid_seq()

        dispatch = {
            TelegramType.BANKING_0100_100: self._banking_0100_100,
            TelegramType.BANKING_0400_100: self._banking_0400_100,
            TelegramType.BANKING_0600_400: self._banking_0600_400,
            TelegramType.CARD_NIT_0200: self._card_nit_0200,
        }
        builder = dispatch.get(telegram_type)
        if builder is None:
            raise ValueError(f"Unsupported TelegramType: {telegram_type}")

        ctx = {
            "yyyymmdd": yyyymmdd,
            "hhmmss": hhmmss,
            "mmdd": mmdd,
            "tlgrm_num": tlgrm_num,
            "inq_num": inq_num,
            "log_pk_seq": log_pk_seq,
            "tid_seq": tid_seq,
        }
        return builder(person, ctx)

    def _make_header(
        self,
        person: Person,
        ctx: dict,
        telegram_id: str,
        sr_type: str,
    ) -> LogHeader:
        unique_key = person.bank_cod + ctx["log_pk_seq"]
        return LogHeader(
            log_pk=person.log_pk + ctx["log_pk_seq"],
            server_id=person.server_id,
            instance_id=person.instance_id,
            log_date=ctx["yyyymmdd"],
            log_time=ctx["hhmmss"],
            unique_key=unique_key,
            telegram_id=telegram_id,
            sr_type=sr_type,
        )

    def _make_common_body(
        self,
        person: Person,
        ctx: dict,
        dsc_cod: str,
        msg_cod: str,
        bz_sctn: str,
        bank_resp_cod: str,
    ) -> LogCommonBody:
        return LogCommonBody(
            dsc_cod=dsc_cod,
            entr_cod=person.entr_cod,
            bank_cod=person.bank_cod,
            msg_cod=msg_cod,
            bz_sctn=bz_sctn,
            trsm_numtm=self.TRSM_NUMTM,
            tlgrm_num=ctx["tlgrm_num"],
            trms_ymd=ctx["yyyymmdd"],
            trms_hms=ctx["hhmmss"],
            resp_cod=self.RESP_COD,
            bank_resp_cod=bank_resp_cod,
            inq_ymd=ctx["yyyymmdd"],
            inq_num=ctx["inq_num"],
            bank_tlgrm_num=person.bank_tlgrm_num,
            bank_cod_3=person.bank_cod_3,
            resv=self.RESV_BANKING,
        )

    def _banking_0100_100(self, person: Person, ctx: dict) -> str:
        header = self._make_header(person, ctx, "0100-100", self.SR_TYPE_MB)
        common = self._make_common_body(
            person, ctx,
            dsc_cod=person.log_pk,
            msg_cod="0100",
            bz_sctn="100",
            bank_resp_cod="0400",
        )
        biz = Banking0100100Body(
            dfmt_actnum=person.dfmt_actnum,
            bbk_pwd=person.bbk_pwd,
            pwd_mrk=person.pwd_mrk,
            outamt_amt=person.trs_amt.rjust(13),
            outamt_aft_rmd_mrk="-",
            dfmt_aft_rmd="         6000",
            dps_bank_cod=person.dps_bank_cod,
            dps_act=person.dps_act,
            coms="       15",
            trsf_time=ctx["hhmmss"],
            dpsr_nm=person.dpsr_nm,
            cms_cod="                ",
            rrn=person.rrn,
            autrsf_sctn="  ",
            dps_act_inf=person.dps_act,
            dps_bank_cod_3=person.dps_bank_cod_3,
            resv2="                                      ",
        )
        return header.to_raw() + common.to_raw() + biz.to_raw()

    def _banking_0400_100(self, person: Person, ctx: dict) -> str:
        header = self._make_header(person, ctx, "0400-100", self.SR_TYPE_API)
        common = self._make_common_body(
            person, ctx,
            dsc_cod=person.log_pk,
            msg_cod="0400",
            bz_sctn="100",
            bank_resp_cod="0N10",
        )
        biz = Banking0400100Body(
            orgn_trs_tlgrm_num=ctx["tlgrm_num"],
            dfmt_actnum=person.dfmt_actnum,
            dps_actnum=person.dps_act,
            req_amt=person.trs_amt.rjust(13),
            dps_bank_cod=person.dps_bank_cod,
            noml_dlng_amt="          200",
            dlng_imp_amt="          300",
            ptil_dlng_cnt="02",
            ptil_dlng_num="01",
            othr_bank_tlgrm_num="AC1000",
            dps_imp_ntc_amt="      300",
            err_cod="005",
            dps_bank_cod_3=person.dps_bank_cod_3,
            resv2="NNNN       1",
        )
        return header.to_raw() + common.to_raw() + biz.to_raw()

    def _banking_0600_400(self, person: Person, ctx: dict) -> str:
        header = self._make_header(person, ctx, "0600-400", self.SR_TYPE_MB)
        common = self._make_common_body(
            person, ctx,
            dsc_cod=person.log_pk,
            msg_cod="0600",
            bz_sctn="400",
            bank_resp_cod="0600",
        )
        biz = Banking0600400Body(
            trs_ymd=ctx["mmdd"],
            bank_cod2=person.dps_bank_cod,
            actnum=person.dfmt_actnum,
            act_nm=person.name.ljust(22),
            rrn=person.rrn,
            res_reg_no_chk_yn="02",
            socact_nm=person.dfmt_actnum.ljust(20),
            bank_cod_3=person.bank_cod_3,
            resv2="                    ",
            co_use_inf="                    ",
            hngl_use_inf=" ",
            conn_bank_resv="0001",
        )
        return header.to_raw() + common.to_raw() + biz.to_raw()

    def _card_nit_0200(self, person: Person, ctx: dict) -> str:
        header = self._make_header(person, ctx, "NIT-0200", self.SR_TYPE_MB)
        tid = person.tid_prefix + ctx["yyyymmdd"] + ctx["tid_seq"]
        card_common = CardCommonBody(
            tlgrm_len="5948",
            tlgrm_txt="NIT",
            tid=tid,
            tlgrm_gbn="0200",
            trs_sctn="12",
            ter_gbn="H1",
            ter_num="NULL      ",
            br_num=person.br_num,
        )
        biz = CardNit0200BizBody(
            wcc="@",
            track=person.track,
            inst_mtcnt="00",
            srvc_fee="NULL     ",
            tex="NULL     ",
            trs_amt=person.trs_amt.rjust(9),
            org_apv_num="NULL    ",
            trs_apvdt="NULL  ",
            org_num="NULL        ",
            bbk_pwd="NULL      ",
            rrn=person.rrn,
            pin_num="NULL            ",
            domain="NULL                          ",
            ip_adr="NULL                ",
        )
        return header.to_raw() + card_common.to_raw() + biz.to_raw()
