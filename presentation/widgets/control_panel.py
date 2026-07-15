# presentation/widgets/control_panel.py
from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QGroupBox,
    QLabel, QLineEdit, QComboBox, QPushButton, QFormLayout,
)
from PyQt6.QtCore import pyqtSignal
from domain.entities.telegram_type import TelegramType


class ControlPanel(QWidget):
    generate_requested = pyqtSignal(str, dict)
    send_requested = pyqtSignal(str, int)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self) -> None:
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)

        root_layout.addWidget(self._build_header_group())
        root_layout.addWidget(self._build_network_group())
        root_layout.addWidget(self._build_action_group())

    def _build_header_group(self) -> QGroupBox:
        group = QGroupBox("헤더 / 전문 설정")
        form = QFormLayout(group)

        self._combo_type = QComboBox()
        for t in TelegramType:
            self._combo_type.addItem(t.value, t.value)
        form.addRow(QLabel("전문 타입:"), self._combo_type)

        self._edit_log_pk = QLineEdit("00603REN001    ")
        self._edit_server_id = QLineEdit("211.168.15.3        ")
        self._edit_instance_id = QLineEdit("542EE       ")
        self._edit_sr_type = QLineEdit("MB   ")

        form.addRow(QLabel("Log PK (15):"), self._edit_log_pk)
        form.addRow(QLabel("Server ID (20):"), self._edit_server_id)
        form.addRow(QLabel("Instance ID (12):"), self._edit_instance_id)
        form.addRow(QLabel("SR Type (5):"), self._edit_sr_type)
        return group

    def _build_network_group(self) -> QGroupBox:
        group = QGroupBox("전송 설정")
        layout = QHBoxLayout(group)

        self._edit_host = QLineEdit("127.0.0.1")
        self._edit_port = QLineEdit("9000")

        layout.addWidget(QLabel("Host:"))
        layout.addWidget(self._edit_host)
        layout.addWidget(QLabel("Port:"))
        layout.addWidget(self._edit_port)
        return group

    def _build_action_group(self) -> QGroupBox:
        group = QGroupBox("액션")
        layout = QHBoxLayout(group)

        btn_generate = QPushButton("로그 생성")
        btn_send = QPushButton("로그 전송")
        btn_generate.clicked.connect(self._on_generate_clicked)
        btn_send.clicked.connect(self._on_send_clicked)

        layout.addWidget(btn_generate)
        layout.addWidget(btn_send)
        return group

    def _on_generate_clicked(self) -> None:
        params = {
            "log_pk": self._edit_log_pk.text(),
            "server_id": self._edit_server_id.text(),
            "instance_id": self._edit_instance_id.text(),
            "sr_type": self._edit_sr_type.text(),
        }
        self.generate_requested.emit(self._combo_type.currentData(), params)

    def _on_send_clicked(self) -> None:
        try:
            port = int(self._edit_port.text())
        except ValueError:
            port = 9000
        self.send_requested.emit(self._edit_host.text(), port)
