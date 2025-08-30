from math import pi

from PyQt6.QtGui import QPainter, QPainterPath, QPen
from PyQt6.QtCore import QPointF, QLineF

from .polar_axles import PolarAxles

from .utils import *


class DashboardPolar(PolarAxles):

    def __init__(self, widget, x, y, size):
        super().__init__(widget, x, y, size)

    def _redraw(self):
        self._qp.begin(self)
        self._qp.setRenderHint(QPainter.RenderHint.Antialiasing)
        self._draw_grid()

        A = arange(0, 2 * pi, 0.01)
        R = [a for a in A]

        path = QPainterPath(QPointF(self.x() + self.__offset_x, self.y() + self.height() / 2))
        path.addEllipse(QPointF(self.width() / 2, self.height() / 2), self.width() // 2, self.height() // 2)
        self._qp.setClipPath(path)
        self._qp.setPen(QPen(QColor("red"), 2.0))
        for i, (a, r) in enumerate(zip(A, R)):
            if i == 0:
                continue
            
            x0 = self._real_to_window_x(R[i - 1], A[i - 1])
            y0 = self._real_to_window_y(R[i - 1], A[i - 1])
            x1 = self._real_to_window_x(r, a)
            y1 = self._real_to_window_y(r, a)

            self._qp.drawLine(QLineF(x0, y0, x1, y1))
        self._qp.end()
