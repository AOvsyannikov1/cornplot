from enum import Enum
from PyQt6.QtGui import QPen, QColor, QPainter, QFont
from PyQt6.QtCore import QLineF, Qt



class SemaphoreColor(Enum):
    green = QColor(0, 170, 0), QColor(100, 100, 100, 50)
    green_yellow = QColor(0, 170, 0), QColor(255, 208, 47)
    yellow = QColor(255, 208, 47), QColor(100, 100, 100, 50)
    red = QColor(255, 0, 0), QColor(100, 100, 100, 50)
    yellow_blinking = QColor(255, 208, 47), QColor(255, 208, 47)


class Semaphore:

    def __init__(self, widget, coord, name='', dark=False, four_digit=True):
        self.__w = widget
        self.__x = coord
        self.__color = SemaphoreColor.green
        self.__name = name
        self.dark: bool = dark
        self.h = 15
        self.r = 10
        self.four_digit = four_digit

        self.x_win = 0
        self.y_win = 0
        self.y_real = 0

    @property
    def x(self):
        return self.__x

    def mousePressEvent(self, a0):
        if self.__color == SemaphoreColor.green:
            self.__color = SemaphoreColor.green_yellow if self.four_digit else SemaphoreColor.yellow
        elif self.__color == SemaphoreColor.green_yellow:
            self.__color = SemaphoreColor.yellow
        elif self.__color == SemaphoreColor.yellow:
            self.__color = SemaphoreColor.red
        elif self.__color == SemaphoreColor.red:
            self.__color = SemaphoreColor.green

    def draw(self, qp:QPainter, x, y, up=True):
        if self.dark:
            qp.setPen(QPen(QColor(255, 255, 255), 1))
        else:
            qp.setPen(QPen(QColor(0, 0, 0), 1))
        h = self.h
        r = self.r
        if up:
            qp.drawLine(QLineF(x, y, x, y - h))
        else:
            qp.drawLine(QLineF(x, y, x, y + h))
        qp.setPen(QPen(QColor(0, 0, 0, 0), 1))
        qp.setFont(QFont("Bahnschrift, Arial", 9))

        x = round(x - r / 2)
        if up:
            y0 = round(y - h - r)

            qp.setPen(QPen(QColor(self.__color.value[0]), r, cap=Qt.PenCapStyle.RoundCap))
            qp.drawPoint(x + r // 2, y0 + r // 2)
            if self.four_digit:
                qp.setPen(QPen(QColor(self.__color.value[1]), r, cap=Qt.PenCapStyle.RoundCap))
                qp.drawPoint(x + r // 2, y0 - r // 2)

            if self.dark:
                qp.setPen(QPen(QColor(255, 255, 255), 1))
            else:
                qp.setPen(QPen(QColor(0, 0, 0), 1))
            qp.drawText(x + r // 2 - 20, y0 - 2*r - r // 2, 40, 2*r, Qt.AlignmentFlag.AlignHCenter, self.__name)
        else:
            y0 = round(y + h)

            if self.four_digit:
                qp.setPen(QPen(QColor(self.__color.value[1]), r, cap=Qt.PenCapStyle.RoundCap))
                qp.drawPoint(x + r // 2, y0 + r // 2)

            qp.setPen(QPen(QColor(self.__color.value[0]), r, cap=Qt.PenCapStyle.RoundCap))
            qp.drawPoint(x + r // 2, y0 + r + (r if self.four_digit else 0) // 2)

            if self.dark:
                qp.setPen(QPen(QColor(255, 255, 255), 1))
            else:
                qp.setPen(QPen(QColor(0, 0, 0), 1))
            qp.drawText(x + r // 2 - 20, y0 + 2 * r + r // 2, 40, 2*r, Qt.AlignmentFlag.AlignHCenter, self.__name)



    def set_color(self, color: SemaphoreColor):
        self.__color = color
