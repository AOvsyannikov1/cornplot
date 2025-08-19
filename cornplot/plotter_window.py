from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QWidget


class PlotterWindow(QWidget):
    def __init__(self):
        super().__init__()
        # self.tmr = QTimer(self)
        # self.tmr.timeout.connect(self.update)
        # self.tmr.start(30)

    def set_plot_event(self, event: callable):
        self.__plot_event = event

    def open(self):
        self.show()
    