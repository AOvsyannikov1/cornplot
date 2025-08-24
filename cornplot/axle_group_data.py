from PyQt6.QtCore import QObject, pyqtSignal as Signal
    
from .scanner_lines import VerticalLineList

MAX_SCANNER_LINES = 3

class AxleGroupData(QObject):
    line_move_signal = Signal()
    pause_signal = Signal(bool)
    restart_signal = Signal(object)
    line_clear_signal = Signal(object)

    def __init__(self):
        super().__init__()
        self.scanner_lines = VerticalLineList(MAX_SCANNER_LINES)
        self.scale_lines = VerticalLineList(2)

        self.x_start = 0
        self.x_stop = 0

    def update_x_borders(self, x0, xk):
        self.x_start = x0
        self.x_stop = xk