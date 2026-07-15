# presentation/styles/fluent.py

FLUENT_STYLESHEET: str = """
QWidget {
    font-family: "Segoe UI", Arial, sans-serif;
    font-size: 13px;
    color: #1A1A1A;
    background-color: #F3F3F3;
}

QMainWindow {
    background-color: #F3F3F3;
}

QGroupBox {
    background-color: #FFFFFF;
    border: 1px solid #E0E0E0;
    border-radius: 6px;
    margin-top: 8px;
    padding: 8px 10px 10px 10px;
    font-weight: 600;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 6px;
    color: #0078D4;
    font-size: 12px;
}

QLineEdit, QSpinBox, QDoubleSpinBox {
    background-color: #FFFFFF;
    border: 1px solid #D0D0D0;
    border-radius: 4px;
    padding: 4px 8px;
    selection-background-color: #0078D4;
    selection-color: #FFFFFF;
}

QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus {
    border: 1.5px solid #0078D4;
}

QLineEdit:disabled, QSpinBox:disabled {
    background-color: #F0F0F0;
    color: #A0A0A0;
}

QPushButton {
    background-color: #FFFFFF;
    border: 1px solid #D0D0D0;
    border-radius: 4px;
    padding: 5px 16px;
    min-height: 28px;
    font-size: 13px;
}

QPushButton:hover {
    background-color: #F0F6FF;
    border-color: #0078D4;
    color: #0078D4;
}

QPushButton:pressed {
    background-color: #D9EDFF;
}

QPushButton:disabled {
    color: #AAAAAA;
    border-color: #E0E0E0;
    background-color: #F5F5F5;
}

QPushButton#btn_start {
    background-color: #0078D4;
    color: #FFFFFF;
    border: none;
    font-weight: 600;
}

QPushButton#btn_start:hover {
    background-color: #006CC0;
    color: #FFFFFF;
}

QPushButton#btn_start:pressed {
    background-color: #005DA3;
    color: #FFFFFF;
}

QPushButton#btn_stop {
    background-color: #D13438;
    color: #FFFFFF;
    border: none;
    font-weight: 600;
}

QPushButton#btn_stop:hover {
    background-color: #B52E32;
    color: #FFFFFF;
}

QTextEdit {
    background-color: #FAFAFA;
    border: 1px solid #E0E0E0;
    border-radius: 4px;
    font-family: "Consolas", "D2Coding", monospace;
    font-size: 12px;
    color: #1A1A1A;
    selection-background-color: #0078D4;
}

QLabel {
    background-color: transparent;
    color: #1A1A1A;
}

QLabel#lbl_state_running {
    color: #107C10;
    font-weight: 700;
}

QLabel#lbl_state_paused {
    color: #FF8C00;
    font-weight: 700;
}

QLabel#lbl_state_idle {
    color: #767676;
    font-weight: 700;
}

QStatusBar {
    background-color: #FFFFFF;
    border-top: 1px solid #E0E0E0;
    font-size: 12px;
}

QSplitter::handle {
    background-color: #E0E0E0;
    width: 1px;
    height: 1px;
}

QScrollBar:vertical {
    background: #F3F3F3;
    width: 8px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background: #C0C0C0;
    border-radius: 4px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background: #0078D4;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}

QDialog {
    background-color: #F3F3F3;
}
"""
