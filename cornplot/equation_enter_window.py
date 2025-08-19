from PyQt6 import QtGui, QtWidgets, QtCore
from .utils import LOWER_INDEXES
from .eq_gui import Ui_Form
from math import exp, sqrt, sin, cos, tan, sinh, cosh, tanh, asin, acos, atan, asinh, acosh, atanh, log
from math import log10, log2, pi, e
from .utils import arange


class EquationWindow(Ui_Form, QtWidgets.QWidget):

    def __init__(self, dashboard):
        super(EquationWindow, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon("cornplot/images/mathIcon.png"))

        self.dashhboard = dashboard

        self.label_3.setText(f"X{LOWER_INDEXES[0]}:")
        self.label_4.setText(f"X{LOWER_INDEXES[1]}:")

        self.xMin.setValue(self.dashhboard.x_axis_min)
        self.xMax.setValue(self.dashhboard.x_axis_max)

        self.button.clicked.connect(self.calculate_plot)

    def keyPressEvent(self, a0: QtGui.QKeyEvent):
        if a0.key() == QtCore.Qt.Key.Key_Return or a0.key() == QtCore.Qt.Key.Key_Enter:
            self.calculate_plot()

    def calculate_plot(self):
        try:
            x0 = min(self.xMin.value(), self.xMax.value())
            x1 = max(self.xMin.value(), self.xMax.value())
            X = arange(x0, x1 + self.xStep.value(), self.xStep.value())
            eq = self.eqLine.text()
            if "sqr" in eq:
                eq = eq.replace("sqr", "sqrt")
            Y = [eval(eq) for x in X]
            self.dashhboard.add_plot(X, Y, name=(eq if self.eqName.text() == "" else self.eqName.text()))
            self.close()
        except:
            msg = QtWidgets.QMessageBox()
            msg.setWindowIcon(QtGui.QIcon("cornplot/images/mathIcon.png"))
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Ошибка в формуле!")
            msg.setWindowTitle("Упс...")
            msg.exec_()
