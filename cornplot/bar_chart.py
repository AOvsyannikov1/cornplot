from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QTimer, Qt, pyqtSlot as Slot
from PyQt6.QtGui import QPainter, QPen, QColor

from .color_generator import ColorGenerator
from .bar_data import BarData

class BarChart(QWidget):
    def __init__(self, widget: QWidget, x: int, y: int, w: int, h: int):
        super().__init__(widget)

        self.__color_generator = ColorGenerator()
        self.__data = BarData()

        self._MIN_X = 40
        self._MAX_X = w - 40
        self._MIN_Y = 20
        self._MAX_Y = h - 40

        self.__dark = False

        self.setGeometry(x, y, w, h)

        self.__qp = QPainter()
        self.__redraw_required = True
        self.__tmr = QTimer(self)
        self.__tmr.timeout.connect(self.__timeout_event)
        self.__tmr.start(50)

    def setGeometry(self, x, y, w, h):
        self.__w = w
        self.__h = h
        super().setGeometry(x - self._MIN_X, y - self._MIN_Y, w + self._MIN_X, h + 2 * self._MIN_Y)

    @Slot()
    def __timeout_event(self):
        if self.__redraw_required:
            self.update()
            self.__redraw_required = False

    def add_bar_chart(self, categories: list[str], values, value_colors=None):
        self.__data.categories = categories
        self.__data.values = values
        if value_colors and len(value_colors) == len(categories):
            self.__data.colors = value_colors
        else:
            self.__data.colors = [self.__color_generator.get_color() for _ in range(len(categories))]

        self.__redraw_required = True

    def paintEvent(self, a0):
        self.__qp.begin(self)
        self.__qp.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.__draw_axes()

        self.__qp.end()

    def __draw_axes(self):
        self.__qp.setPen(QColor(0, 0, 0, 0))
        self.__qp.setBrush(QColor(0xFFFFFF))

        self.__qp.drawRect(self._MIN_X, self._MIN_Y, self.__w, self.__h)
