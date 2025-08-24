from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5.QtGui import QKeyEvent, QIcon
from .eq_gui import Ui_Form

from .utils import LOWER_INDEXES
from math import exp, sqrt, sin, cos, tan, sinh, cosh, tanh, asin, acos, atan, asinh, acosh, atanh, log
from math import log10, log2, pi, e
from .utils import arange, get_image_path


class EquationWindow(Ui_Form, QWidget):

    def __init__(self, dashboard):
        super(EquationWindow, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(get_image_path("mathIcon.png")))

        self.__dashhboard = dashboard

        self.label_3.setText(f"X{LOWER_INDEXES[0]}:")
        self.label_4.setText(f"X{LOWER_INDEXES[1]}:")

        self.xMin.setValue(self.__dashhboard.x_axis_min)
        self.xMax.setValue(self.__dashhboard.x_axis_max)

        self.button.clicked.connect(self.calculate_plot)

    def keyPressEvent(self, a0: QKeyEvent | None):
        if a0 is None:
            return
        if a0.key() == Qt.Key.Key_Return or a0.key() == Qt.Key.Key_Enter:
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
            self.__dashhboard.add_plot(X, Y, name=(eq if self.eqName.text() == "" else self.eqName.text()))
            self.close()
        except Exception as e:
            msg = QMessageBox()
            msg.setWindowIcon(QIcon(get_image_path("mathIcon.png")))
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setText("Ошибка в формуле!")
            msg.setWindowTitle("Упс...")
            msg.exec()
