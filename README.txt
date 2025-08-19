Пример использования:


from PyQt6 import QtCore, QtWidgets, QtGui
import cornplot as cp
import numpy as np
import time


class Window(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.plt1 = cp.Dashboard(self, 100, 50, 1000, 300)
        self.plt2 = cp.Dashboard(self, 100, 400, 1000, 300)

        # self.plt1.set_dark(True)
        # self.plt2.set_dark(True)

        X = np.arange(0, 20, 0.001)
        Y1 = np.sin(X)
        Y2 = np.random.beta(0.5, 0.6, len(X))
        Y3 = np.sin(2*X + 0.1) + np.sin(0.68*X - 0.2)
        # X = [1, 2, 3, 4, 5]
        # Y1 = np.random.normal(loc=0, scale=2, size=len(X))

        self.plt1.add_plot(X, Y1, name="SIN")
        self.plt1.add_plot(X, Y3, name="Косинус")
        self.plt2.add_animated_plot(name="Plot1", x_size=30)
        self.plt2.add_animated_plot(name="Plot2", x_size=30)

        self.plt1.move_to_group("1")
        # self.plt2.move_to_group("1")

        # self.plt2.set_visible(True)

        self.tmr = QtCore.QTimer(self)
        self.tmr.timeout.connect(self.update)
        self.tmr.start(25)

    def paintEvent(self, a0):
        t = time.monotonic()
        self.plt2.add_point_to_animated_plot("Plot1", t, np.random.normal(loc=0, scale=0.1))
        self.plt2.add_point_to_animated_plot("Plot2", t, np.sin(t / 1.5) + 0.9 * np.cos(3 * t) + 0.4 * np.cos(6 * t))

        self.plt1.redraw()
        self.plt2.redraw()

    def resizeEvent(self, a0):
        self.plt1.set_geometry(100, 50, self.width() - 200, self.height() // 3)
        self.plt2.set_geometry(100, self.height() // 2, self.width() - 200, self.height() // 3)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Window()
    ui.show()
    sys.exit(app.exec())
