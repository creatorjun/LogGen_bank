# infrastructure/builders/log_builder.py
from datetime import datetime
from domain.entities.telegram_type import TelegramType
from domain.entities.log_header import LogHeader
from domain.entities.log_common_body import LogCommonBody
from domain.entities.telegrams.banking_0100_100 import Banking0100100Body
from domain.entities.telegrams.banking_0400_100 import Banking0400100Body
from domain.entities.telegrams.banking_0600_400 import Banking0600400Body
from domain.entities.telegrams.card_nit_0200 import CardNit0200CommonBody, CardNit0200BizBody
from domain.ports.log_builder_port import LogBuilderPort


class LogBuilder(LogBuilderPort):
    _BUILDERS: dict = {}

    def __init__(self) -> None:
        self._BUILDERS = {
            TelegramType.BANKING_0100_100: self._build_banking_0100_100,
            TelegramType.BANKING_0400_100: self._build_banking_0400_100,
            TelegramType.BANKING_0600_400: self._build_banking_0600_400,
            TelegramType.CARD_NIT_0200: self._build_card_nit_0200,
        }

    def build(self, telegram_type: TelegramType, params: dict) -> str:
        builder_fn = self._BUILDERS.get(telegram_type)
        if builder_fn is None:
            raise ValueError(f"Unknown telegram type: {telegram_type}")
        return builder_fn(params)

    def _make_header(self, params: dict) -> LogHeader:
        now = datetime.now()
        return LogHeader(
            log_pk=params.get("log_pk", ""),
            server_id=params.get("server_id", ""),
            instance_id=params.get("instance_id", ""),
            log_date=params.get("log_date", now.strftime("%Y%m%d")),
            log_time=params.get("log_time", now.strftime("%H%M%S")),
            unique_key=params.get("unique_key", ""),
            telegram_id=params.get("telegram_id", ""),
            sr_type=params.get("sr_type", ""),
        )

    def _make_common_body(self, params: dict) -> LogCommonBody:
        now = datetime.now()
        return LogCommonBody(
            dsc_cod=params.get("dsc_cod", ""),
            entr_cod=params.get("entr_cod", ""),
            bank_cod=params.get("bank_cod", ""),
            msg_cod=params.get("msg_cod", ""),
            bz_sctn=params.get("bz_sctn", ""),
            trsm_numtm=params.get("trsm_numtm", "1"),
            tlgrm_num=params.get("tlgrm_num", "000001"),
            trms_ymd=params.get("trms_ymd", now.strftime("%Y%m%d")),
            trms_hms=params.get("trms_hms", now.strftime("%H%M%S")),
            resp_cod=params.get("resp_cod", "    "),
            bank_resp_cod=params.get("bank_resp_cod", ""),
            inq_ymd=params.get("inq_ymd", now.strftime("%Y%m%d")),
            inq_num=params.get("inq_num", ""),
            bank_tlgrm_num=params.get("bank_tlgrm_num", ""),
            bank_cod_3=params.get("bank_cod_3", ""),
            resv=params.get("resv", ""),
        )

    def _build_banking_0100_100(self, params: dict) -> str:
        header = self._make_header(params)
        common = self._make_common_body(params)
        biz = Banking0100100Body(
            dfmt_actnum=params.get("dfmt_actnum", ""),
            bbk_pwd=params.get("bbk_pwd", ""),
            pwd_mrk=params.get("pwd_mrk", ""),
            outamt_amt=params.get("outamt_amt", ""),
            outamt_aft_rmd_mrk=params.get("outamt_aft_rmd_mrk", "+"),
            dfmt_aft_rmd=params.get("dfmt_aft_rmd", ""),
            dps_bank_cod=params.get("dps_bank_cod", ""),
            dps_act=params.get("dps_act", ""),
            coms=params.get("coms", ""),
            trsf_time=params.get("trsf_time", ""),
            dpsr_nm=params.get("dpsr_nm", ""),
            cms_cod=params.get("cms_cod", ""),
            rrn=params.get("rrn", ""),
            autrsf_sctn=params.get("autrsf_sctn", ""),
            dps_act_inf=params.get("dps_act_inf", ""),
            dps_bank_cod_3=params.get("dps_bank_cod_3", ""),
            resv2=params.get("resv2", ""),
        )
        return header.to_raw() + common.to_raw() + biz.to_raw()

    def _build_banking_0400_100(self, params: dict) -> str:
        header = self._make_header(params)
        common = self._make_common_body(params)
        biz = Banking0400100Body(
            orgn_trs_tlgrm_num=params.get("orgn_trs_tlgrm_num", ""),
            dfmt_actnum=params.get("dfmt_actnum", ""),
            dps_actnum=params.get("dps_actnum", ""),
            req_amt=params.get("req_amt", ""),
            dps_bank_cod=params.get("dps_bank_cod", ""),
            noml_dlng_amt=params.get("noml_dlng_amt", ""),
            dlng_imp_amt=params.get("dlng_imp_amt", ""),
            ptil_dlng_cnt=params.get("ptil_dlng_cnt", ""),
            ptil_dlng_num=params.get("ptil_dlng_num", ""),
            othr_bank_tlgrm_num=params.get("othr_bank_tlgrm_num", ""),
            dps_imp_ntc_amt=params.get("dps_imp_ntc_amt", ""),
            err_cod=params.get("err_cod", ""),
            dps_bank_cod_3=params.get("dps_bank_cod_3", ""),
            resv2=params.get("resv2", ""),
        )
        return header.to_raw() + common.to_raw() + biz.to_raw()

    def _build_banking_0600_400(self, params: dict) -> str:
        header = self._make_header(params)
        common = self._make_common_body(params)
        biz = Banking0600400Body(
            trs_ymd=params.get("trs_ymd", ""),
            bank_cod2=params.get("bank_cod2", ""),
            actnum=params.get("actnum", ""),
            act_nm=params.get("act_nm", ""),
            rrn=params.get("rrn", ""),
            res_reg_no_chk_yn=params.get("res_reg_no_chk_yn", ""),
            socact_nm=params.get("socact_nm", ""),
            bank_cod_3=params.get("bank_cod_3", ""),
            resv2=params.get("resv2", ""),
            co_use_inf=params.get("co_use_inf", ""),
            hngl_use_inf=params.get("hngl_use_inf", ""),
            conn_bank_resv=params.get("conn_bank_resv", ""),
        )
        return header.to_raw() + common.to_raw() + biz.to_raw()

    def _build_card_nit_0200(self, params: dict) -> str:
        header = self._make_header(params)
        card_common = CardNit0200CommonBody(
            tlgrm_len=params.get("tlgrm_len", ""),
            tlgrm_txt=params.get("tlgrm_txt", "NIT"),
            tid=params.get("tid", ""),
            tlgrm_gbn=params.get("tlgrm_gbn", "0200"),
            trs_sctn=params.get("trs_sctn", "12"),
            ter_gbn=params.get("ter_gbn", "H1"),
            ter_num=params.get("ter_num", "NULL      "),
            br_num=params.get("br_num", "9716010001"),
        )
        biz = CardNit0200BizBody(
            wcc=params.get("wcc", "@"),
            track=params.get("track", ""),
            inst_mtcnt=params.get("inst_mtcnt", "00"),
            srvc_fee=params.get("srvc_fee", "NULL     "),
            tex=params.get("tex", "NULL     "),
            trs_amt=params.get("trs_amt", ""),
            org_apv_num=params.get("org_apv_num", "NULL    "),
            trs_apvdt=params.get("trs_apvdt", "NULL  "),
            org_num=params.get("org_num", "NULL        "),
            bbk_pwd=params.get("bbk_pwd", "NULL      "),
            rrn=params.get("rrn", ""),
            pin_num=params.get("pin_num", "NULL            "),
            domain=params.get("domain", "NULL                          "),
            ip_adr=params.get("ip_adr", "NULL                "),
        )
        return header.to_raw() + card_common.to_raw() + biz.to_raw()
