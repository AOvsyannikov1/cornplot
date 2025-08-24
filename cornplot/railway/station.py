from PyQt5.QtGui import QPainter, QColor, QPolygonF, QFont, QFontMetrics
from PyQt5.QtCore import QRectF, Qt


class Station:
    def __init__(self, coord, length, name, dark=False):
        self.__x = coord
        self.__l = length
        self.__name = name
        self.dark: bool = dark
        self.h = 5

        self.polygon = QPolygonF()
        self.y0_real = 0
        self.yk_real = 0

    @property
    def x(self):
        return self.__x

    @property
    def l(self):
        return self.__l

    def draw(self, qp: QPainter, up_txt=True):
        qp.setPen(QColor(0, 0, 0, 0))
        if self.dark:
            qp.setBrush(QColor(200, 200, 200))
        else:
            qp.setBrush(QColor(100, 100, 100))
        qp.drawPolygon(self.polygon)

        font = QFont("Bahnschrift, Arial", 10)
        qp.setFont(font)

        metrics = QFontMetrics(font)
        w = metrics.horizontalAdvance(self.__name)

        if self.dark:
            qp.setPen(QColor(200, 200, 200))
        else:
            qp.setPen(QColor(0, 0, 0))
        if up_txt:
            y = self.polygon[0].y() - 40 - self.h
        else:
            y = self.polygon[0].y() + 20
        qp.drawText(QRectF(self.polygon[0].x(), y, w, 15), Qt.AlignmentFlag.AlignHCenter, self.__name)
