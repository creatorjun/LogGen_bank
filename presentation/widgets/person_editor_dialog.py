# presentation/widgets/person_editor_dialog.py
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QComboBox,
    QFormLayout, QLineEdit, QPushButton, QDialogButtonBox,
    QGroupBox, QScrollArea, QWidget,
)
from PyQt6.QtCore import pyqtSignal
from domain.entities.person import Person
from infrastructure.data.person_fixture import PERSONS
import copy


class PersonEditorDialog(QDialog):
    persons_updated = pyqtSignal(list)

    FIELD_LABELS: dict[str, str] = {
        "name": "성명",
        "rrn": "주민번호",
        "log_pk": "로그 PK",
        "entr_cod": "업체코드",
        "server_id": "서버 IP",
        "instance_id": "인스턴스 ID",
        "bank_cod": "은행코드(2)",
        "bank_cod_3": "은행코드(3)",
        "bank_resp_cod": "은행응답코드",
        "dfmt_actnum": "출금계좌번호",
        "bbk_pwd": "통장비밀번호",
        "pwd_mrk": "복기부호",
        "dps_act": "입금계좌번호",
        "dps_bank_cod": "입금은행코드(2)",
        "dps_bank_cod_3": "입금은행코드(3)",
        "dpsr_nm": "입금인성명",
        "bank_tlgrm_num": "은행전문번호",
        "card_number": "카드번호",
        "card_expiry": "유효기간",
        "track": "Track-II",
        "tid_prefix": "TID 증권번호",
        "br_num": "가맹점번호",
        "trs_amt": "거래금액",
    }

    def __init__(self, persons: list[Person], parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Person 편집")
        self.setMinimumWidth(480)
        self._persons: list[Person] = [copy.copy(p) for p in persons]
        self._current_idx: int = 0
        self._edits: dict[str, QLineEdit] = {}
        self._build_ui()
        self._load_person(0)

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)

        selector_row = QHBoxLayout()
        selector_row.addWidget(*[__import__('PyQt6.QtWidgets', fromlist=['QLabel']).QLabel("Person")])
        self._combo = QComboBox()
        for p in self._persons:
            self._combo.addItem(p.name)
        self._combo.currentIndexChanged.connect(self._on_person_changed)
        selector_row.addWidget(self._combo, stretch=1)
        root.addLayout(selector_row)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        inner = QWidget()
        form = QFormLayout(inner)
        form.setSpacing(6)
        for field, label in self.FIELD_LABELS.items():
            edit = QLineEdit()
            edit.setObjectName(field)
            form.addRow(label, edit)
            self._edits[field] = edit
        scroll.setWidget(inner)
        root.addWidget(scroll, stretch=1)

        btn_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        btn_reset = QPushButton("기본값으로 복원")
        btn_box.addButton(btn_reset, QDialogButtonBox.ButtonRole.ResetRole)
        btn_box.accepted.connect(self._on_ok)
        btn_box.rejected.connect(self.reject)
        btn_reset.clicked.connect(self._on_reset)
        root.addWidget(btn_box)

    def _load_person(self, idx: int) -> None:
        p = self._persons[idx]
        for field, edit in self._edits.items():
            edit.setText(getattr(p, field, ""))

    def _save_current(self) -> None:
        p = self._persons[self._current_idx]
        for field, edit in self._edits.items():
            setattr(p, field, edit.text())

    def _on_person_changed(self, idx: int) -> None:
        self._save_current()
        self._current_idx = idx
        self._load_person(idx)

    def _on_ok(self) -> None:
        self._save_current()
        self.persons_updated.emit(self._persons)
        self.accept()

    def _on_reset(self) -> None:
        self._persons = [copy.copy(p) for p in PERSONS]
        self._load_person(self._current_idx)
