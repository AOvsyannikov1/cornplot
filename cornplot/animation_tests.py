try:
    from PyQt6 import QtCore, QtWidgets, QtGui
except ImportError:
    from PyQt5 import QtCore, QtWidgets, QtGui

from .dashboard import Dashboard
import numpy as np
import time
from .plotter import Plotter


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(50, 50, 1800, 950)
        self.setMinimumSize(500, 500)

        self.dash = Dashboard(self, 100, 30, 400, 1000, y_name="Y", animated=True, draw_x=True)
        self.dash1 = Dashboard(self, 100, 470, 400, 1000, y_name="Y", draw_x=True, master=self.dash)

        self.dash.add_dataset("Dataset 1", x_size=15)
        self.dash.add_dataset("Dataset 2", x_size=15)
        self.dash.add_dataset("Dataset 3", x_size=15)
        self.dash1.add_dataset("Dataset 1", x_size=15)
        self.dash1.add_dataset("Dataset 2", x_size=15)

        self.plotter = Plotter(self, self.plot_event)
        self.plotter.start()

    def plot_event(self):
        return True# self.dash.needs_redrawing() or self.dash1.needs_redrawing()

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        t = time.time()
        self.dash.add_point_to_dataset("Dataset 1", t, np.exp(np.cos(t)) - 2 * np.cos(4 * t) + np.sin(t / 12) ** 5)
        self.dash.add_point_to_dataset("Dataset 2", t, np.cos(t) + np.sin(t))
        self.dash.add_point_to_dataset("Dataset 3", t, np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t))

        self.dash1.add_point_to_dataset("Dataset 1", t, -2 ** (np.sin(4 * t) + np.cos(2*t)))
        self.dash1.add_point_to_dataset("Dataset 2", t, 2 ** (np.sin(4 * t) + np.cos(2*t)))
        self.dash.redraw_plots()
        self.dash1.redraw_plots()

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        self.dash.set_geometry(90, 30, self.width() - 180, self.height() // 2 - 70)
        self.dash1.set_geometry(90, 60 + self.height() // 2 - 35, self.width() - 180, self.height() // 2 - 70)


def start_animation():
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = Window()
    ui.show()
    sys.exit(app.exec())
