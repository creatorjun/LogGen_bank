# presentation/widgets/stats_panel.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QFormLayout, QLabel
from PyQt6.QtCore import Qt


class StatsPanel(QWidget):
    STATE_IDLE: str = "IDLE"
    STATE_RUNNING: str = "RUNNING"
    STATE_PAUSED: str = "PAUSED"

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        grp = QGroupBox("전송 통계")
        form = QFormLayout(grp)
        form.setSpacing(8)

        self._lbl_person = QLabel("-")
        self._lbl_type = QLabel("-")
        self._lbl_total = QLabel("0")
        self._lbl_failed = QLabel("0")
        self._lbl_state = QLabel(self.STATE_IDLE)
        self._lbl_state.setObjectName("lbl_state_idle")

        form.addRow("Person", self._lbl_person)
        form.addRow("전문 타입", self._lbl_type)
        form.addRow("전송 건수", self._lbl_total)
        form.addRow("실패 건수", self._lbl_failed)
        form.addRow("상태", self._lbl_state)

        root.addWidget(grp)
        root.addStretch()

    def update_stats(
        self,
        person: str,
        telegram_type: str,
        total: int,
        failed: int,
        state: str,
    ) -> None:
        self._lbl_person.setText(person or "-")
        self._lbl_type.setText(telegram_type or "-")
        self._lbl_total.setText(str(total))
        self._lbl_failed.setText(str(failed))
        self._lbl_state.setText(state)

        obj_name_map = {
            self.STATE_RUNNING: "lbl_state_running",
            self.STATE_PAUSED: "lbl_state_paused",
            self.STATE_IDLE: "lbl_state_idle",
        }
        self._lbl_state.setObjectName(obj_name_map.get(state, "lbl_state_idle"))
        self._lbl_state.style().unpolish(self._lbl_state)
        self._lbl_state.style().polish(self._lbl_state)
