from math import sin, cos, floor, ceil, log10, radians, pi, degrees, sqrt

import numpy as np
from PyQt6.QtCore import Qt, QRectF, QLineF, QTimer, pyqtSlot as Slot, QPointF
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QFontMetrics, QPen, QFont, QPainter, QPainterPath

from .axles import Axles
from .array_utils import *
from .utils import *


class PolarAxles(QWidget):

    def __init__(self, widget, x, y, size):
        super().__init__(widget)
        self.__offset_x = 10
        self.__offset_y = 10

        self.__w = size
        self.__h = size

        self._MIN_X = self.__offset_x
        self._MAX_X = self.__w + self.__offset_x
        self._MIN_Y = self.__offset_y
        self._MAX_Y = self.__offset_y + self.__h

        self._start_value = -5
        self._stop_value = 5
        self._min_value = -5
        self._max_value = 5
        self._real_size = 10
        self.__step_grid = 1
        self._digits_count = -1

        self.__redraw_required = True

        self.__font = QFont("Bahnschrift, Arial", 11)

        self.setGeometry(x, y, size)

        self._qp = QPainter()
        self.__tmr = QTimer(self)
        self.__tmr.timeout.connect(self.__tmr_callback)
        self.__tmr.start(25)

    def paintEvent(self, a0):
        self._redraw()

    @Slot()
    def __tmr_callback(self):
        if self.__redraw_required:
            self.update()

    def _redraw(self):
        self._qp.begin(self)
        self._qp.setRenderHint(QPainter.RenderHint.Antialiasing)
        self._draw_grid()
        self._qp.end()

    def setGeometry(self, x, y, size):
        self.__w = size
        self.__h = size
        super().setGeometry(x - self.__offset_x, y - self.__offset_y, size + 2 * self.__offset_x, size + 2 * self.__offset_y)
        self._MIN_X = self.__offset_x
        self._MAX_X = self.__w + self.__offset_x
        self._MIN_Y = self.__offset_y
        self._MAX_Y = self.__offset_y + self.__h

    def _real_to_window_x(self, r: float, angle: float):
        x = r * cos(angle)
        return c_real_to_window_x(x, self._MIN_X, self.__w, self._real_size, self._start_value)
    
    def _real_to_window_y(self, r: float, angle: float):
        y = r * sin(angle)
        return c_real_to_window_y(y, self._MIN_Y, self.__h, self._real_size, self._stop_value)
    
    def _draw_grid(self):
        self.__draw_grid_circles()
        self.__draw_grid_angles()
    
    def __draw_grid_circles(self):
        x0 = self.__step_grid
        xk = min(self._max_value, self._stop_value) + self.__step_grid
        radiuses = arange(x0, xk, self.__step_grid)
        
        center = QPointF(self.width() / 2, self.height() / 2)
        self._qp.setPen(QColor(0, 0, 0, 0))
        self._qp.setBrush(QColor(0xFFFFFF))
        self._qp.drawEllipse(center, self.width() // 2, self.height() // 2)

        divised_step = self.__step_grid
        digit_count = max(get_digit_count_after_dot(x) for x in radiuses)
        digit_count = max(get_digit_count_after_dot(divised_step), digit_count)
        if divised_step < 0.5:
            digit_count = max(2, digit_count)

        metrics = QFontMetrics(self.__font)

        for i, r in enumerate(radiuses):
            x_win = self._real_to_window_x(r, 0)
            r_win = x_win - self._real_to_window_x(0, 0)

            self._qp.setPen(QPen(QColor(0), 0.5, Qt.PenStyle.SolidLine))
            self._qp.setBrush(QColor(0, 0, 0, 0))
            self._qp.drawEllipse(center, r_win, r_win)

            if i < len(radiuses) - 1:
                self._qp.setFont(self.__font)
                y_win = self.height() / 2 + 5
                tmp_str = self.__get_rounded_tick(r, divised_step, digit_count if self._digits_count < 0 else self._digits_count)
                w = metrics.horizontalAdvance(tmp_str)
                h = metrics.height()

                self._qp.setPen(QColor(0, 0, 0, 0))
                self._qp.setBrush(QColor(0xFFFFFF))
                self._qp.drawRect(QRectF(x_win - w / 2, y_win, w, h))

                self._qp.setPen(QColor(0))
                self._qp.drawText(QRectF(x_win - w / 2, y_win, w, h), Qt.AlignmentFlag.AlignCenter, tmp_str)

                x_win = self._real_to_window_x(-r, 0)
                tmp_str = self.__get_rounded_tick(-r, divised_step, digit_count if self._digits_count < 0 else self._digits_count)
                w = metrics.horizontalAdvance(tmp_str)
                h = metrics.height()

                self._qp.setPen(QColor(0, 0, 0, 0))
                self._qp.setBrush(QColor(0xFFFFFF))
                self._qp.drawRect(QRectF(x_win - w / 2, y_win, w, h))

                self._qp.setPen(QColor(0))
                self._qp.drawText(QRectF(x_win - w / 2, y_win, w, h), Qt.AlignmentFlag.AlignCenter, tmp_str)

    def __draw_grid_angles(self):
        angle_step_degrees = 30
        angles = arange(0, pi, radians(angle_step_degrees))

        metrics = QFontMetrics(self.__font)
        for angle in angles:
            self._qp.setPen(QPen(QColor(0), 0.5, Qt.PenStyle.SolidLine))
            self._qp.setBrush(QColor(0, 0, 0, 0))

            p0 = QPointF(self._real_to_window_x(self._min_value, angle), self._real_to_window_y(self._min_value, angle))
            p1 = QPointF(self._real_to_window_x(self._max_value, angle), self._real_to_window_y(self._max_value, angle))
            self._qp.drawLine(p0, p1)

            x_win = self._real_to_window_x(self._stop_value, 0)
            r_win = x_win - self._real_to_window_x(0, 0)
            max_radius = r_win
            self._qp.setPen(QColor(0))

            text = str(round(degrees(angle))) + "°"
            self.__draw_angle_text(text, metrics, max_radius, angle)
            text = str(round(degrees(angle) + 180)) + "°"
            self.__draw_angle_text(text, metrics, max_radius, angle + pi)

    def __draw_angle_text(self, text: str, metrics: QFontMetrics, max_radius: float, angle_radians: float):
        text_w = metrics.horizontalAdvance(text)
        h = metrics.height()
        r = sqrt(0.5 * text_w ** 2 + (0.5 * h) ** 2)
        r_center = max_radius - r
        x_win_center = r_center * cos(angle_radians) + self.width() / 2
        y_win_center = r_center * sin(-angle_radians) + self.height() / 2
        rect = QRectF(x_win_center - text_w / 2, y_win_center - h / 2, text_w, h)

        self._qp.setPen(QColor(0, 0, 0, 0))
        self._qp.setBrush(QColor(0xFFFFFF))
        self._qp.drawRect(rect)
        self._qp.setPen(QColor(0, 0, 0))
        self._qp.drawText(rect, Qt.AlignmentFlag.AlignCenter, text)
            
    def __get_rounded_tick(self, val, step, digit_count):
        if abs(val) < 1e-15:
            val = 0.0
        val = round(val, 10)
        step = round(step, 10)
        tmp_str = round_value(val, digit_count)
        if step > 5 and 'e' not in tmp_str and 'E' not in tmp_str:
            int_part, frac_part = tmp_str.split('.')
            if step >= 10 and all(dig == '0' for dig in frac_part):
                tmp_str = str(int_part)
        return tmp_str
