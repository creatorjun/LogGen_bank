# presentation/view_models/main_view_model.py
from PyQt6.QtCore import QObject, pyqtSignal
from application.services.transmission_loop import TransmissionStats


class MainViewModel(QObject):
    log_appended = pyqtSignal(str, bool)
    stats_updated = pyqtSignal(TransmissionStats)
    state_changed = pyqtSignal(str)
    send_result = pyqtSignal(bool, str)
