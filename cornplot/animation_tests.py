import time

from PyQt6.QtCore import pyqtSlot as Slot, QTimer
from PyQt6.QtWidgets import QWidget, QApplication

from .dashboard import Dashboard
import numpy as np


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(50, 50, 1800, 950)
        self.setMinimumSize(500, 500)

        self.dash = Dashboard(self, 100, 30, 400, 1000)
        self.dash1 = Dashboard(self, 100, 470, 400, 1000)

        self.dash.move_to_group("animated_test")
        self.dash1.move_to_group("animated_test")

        self.dash.add_animated_plot("Dataset 1", x_size=15)
        self.dash.add_animated_plot("Dataset 2", x_size=15)
        self.dash.add_animated_plot("Dataset 3", x_size=15)
        self.dash1.add_animated_plot("Dataset 1", x_size=15)
        self.dash1.add_animated_plot("Dataset 2", x_size=15)

        self.tmr = QTimer(self)
        self.tmr.timeout.connect(self.__add_points)
        self.tmr.start(25)

    @Slot()
    def __add_points(self) -> None:
        t = time.time()
        self.dash.add_point_to_animated_plot("Dataset 1", t, np.exp(np.cos(t)) - 2 * np.cos(4 * t) + np.sin(t / 12) ** 5)
        self.dash.add_point_to_animated_plot("Dataset 2", t, np.cos(t) + np.sin(t))
        self.dash.add_point_to_animated_plot("Dataset 3", t, np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t))

        self.dash1.add_point_to_animated_plot("Dataset 1", t, -2 ** (np.sin(4 * t) + np.cos(2*t)))
        self.dash1.add_point_to_animated_plot("Dataset 2", t, 2 ** (np.sin(4 * t) + np.cos(2*t)))

    def resizeEvent(self, a0) -> None:
        self.dash.set_geometry(90, 30, self.width() - 180, self.height() // 2 - 70)
        self.dash1.set_geometry(90, 60 + self.height() // 2 - 35, self.width() - 180, self.height() // 2 - 70)


def start_animation():
    import sys
    app = QApplication(sys.argv)
    ui = Window()
    ui.show()
    sys.exit(app.exec())
