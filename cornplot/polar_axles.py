from math import sin, cos, log10, radians, pi, degrees, sqrt, atan2, hypot
import os

from PyQt6.QtCore import Qt, QRectF, QTimer, pyqtSlot as Slot, QPointF
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QFontMetrics, QPen, QFont, QPainter

from .array_utils import *
from .utils import *


class PolarAxles(QWidget):

    def __init__(self, widget, x, y, size):
        super().__init__(widget)
        self.setMouseTracking(True)
        self.__offset_x = 10
        self.__offset_y = 10

        self.__w = size
        self.__h = size

        self._MIN_X = self.__offset_x
        self._MAX_X = self.__w + self.__offset_x
        self._MIN_Y = self.__offset_y
        self._MAX_Y = self.__offset_y + self.__h

        self.__x_met_width = 10

        self._start_value = -5
        self._stop_value = 5
        self._min_value = -5
        self._max_value = 5
        self._real_size = 10
        self._step_grid = 1
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

    def _get_width(self):
        return self.__w
    
    def _get_heignt(self):
        return self.__h

    def _update_step_x(self) -> float:
        """Вычисление шага по оси Х"""
        try:
            new_step = 10 ** (round(log10(self._real_size)) - 1)
        except ValueError:
            new_step = 1.0

        ticks_count = self._real_size / new_step
        if ticks_count > 10:
            n = 3
            while (ticks_count := self._real_size / new_step) > 10:
                n += 1
                new_step *= self.__get_factor(n)
        else:
            n = 0
            while (ticks_count := self._real_size / new_step) < 10:
                n += 1
                new_step /= self.__get_factor(n)
        tick_width_px = new_step / self._real_size * self.__w
        while (tick_width_px := new_step / self._real_size * self.__w) < self.__x_met_width + 15:
            new_step *= self.__get_factor(n)
            n += 1

        if 150 < tick_width_px:
            new_step /= self.__get_factor(n)

        if new_step == 0:
            new_step = self._real_size / 1

        self._step_grid = new_step        
        return new_step
    
    def __get_factor(self, n):
        return 2.5 if n % 4 == 0 else 2

    @Slot()
    def __tmr_callback(self):
        if self.__redraw_required:
            self.update()
            self.__redraw_required = False

    def _force_redraw(self):
        self.__redraw_required = True

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
        self._recalculate_window_coords()
        self._update_step_x()

    def _carthesian_to_polar(self, x: float, y: float) -> tuple[float, float]:
        r = hypot(x, y)
        a = atan2(y, x)
        return r, a
    
    def _window_to_polar(self, x: float, y: float) -> tuple[float, float]:
        x = c_window_to_real_x(x, self._MAX_X - self._MIN_X, self._real_size, self._start_value)
        y = c_window_to_real_y(y, self._MAX_Y - self._MIN_Y, self._real_size, self._stop_value, self._MIN_Y)
        return self._carthesian_to_polar(x, y)

    def _polar_coords_to_x(self, r: float, angle: float) -> float:
        return r * cos(angle)
    
    def _polar_coords_to_y(self, r: float, angle: float) -> float:
        return r * sin(angle)

    def _real_to_window_x(self, x: float):
        return c_real_to_window_x(x, self._MIN_X, self.__w, self._real_size, self._start_value)
    
    def _real_to_window_y(self, y: float):
        return c_real_to_window_y(y, self._MIN_Y, self.__h, self._real_size, self._stop_value)

    def _real_polar_to_window_x(self, r: float, angle: float):
        x = self._polar_coords_to_x(r, angle)
        return c_real_to_window_x(x, self._MIN_X, self.__w, self._real_size, self._start_value)
    
    def _real_polar_to_window_y(self, r: float, angle: float):
        y = self._polar_coords_to_y(r, angle)
        return c_real_to_window_y(y, self._MIN_Y, self.__h, self._real_size, self._stop_value)
    
    def _recalculate_window_coords(self):
        pass

    def _draw_grid(self, white_rect=False):
        self.__draw_grid_circles(white_rect)
        self.__draw_grid_angles()
    
    def __draw_grid_circles(self, white_rect=False):
        x0 = self._step_grid
        xk = min(self._max_value, self._stop_value) + self._step_grid
        radiuses = arange(x0, xk, self._step_grid)
        
        center = QPointF(self.width() / 2, self.height() / 2)
        self._qp.setPen(QColor(0, 0, 0, 0))
        self._qp.setBrush(QColor(0xFFFFFF))
        if white_rect:
            self._qp.drawRect(0, 0, self.width(), self.height())
        else:
            self._qp.drawEllipse(center, self.width() // 2, self.height() // 2)

        divised_step = self._step_grid
        try:
            digit_count = max(get_digit_count_after_dot(x) for x in radiuses)
        except ValueError:
            return
        digit_count = max(get_digit_count_after_dot(divised_step), digit_count)
        if divised_step < 0.5:
            digit_count = max(2, digit_count)

        metrics = QFontMetrics(self.__font)

        old_x_met_width = self.__x_met_width

        for i, r in enumerate(radiuses):
            x_win = self._real_polar_to_window_x(r, 0)
            r_win = x_win - self._real_polar_to_window_x(0, 0)

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

                x_win = self._real_polar_to_window_x(-r, 0)
                tmp_str = self.__get_rounded_tick(-r, divised_step, digit_count if self._digits_count < 0 else self._digits_count)
                w = metrics.horizontalAdvance(tmp_str)
                h = metrics.height()

                if w > self.__x_met_width:
                    self.__x_met_width = w

                self._qp.setPen(QColor(0, 0, 0, 0))
                self._qp.setBrush(QColor(0xFFFFFF))
                self._qp.drawRect(QRectF(x_win - w / 2, y_win, w, h))

                self._qp.setPen(QColor(0))
                self._qp.drawText(QRectF(x_win - w / 2, y_win, w, h), Qt.AlignmentFlag.AlignCenter, tmp_str)

        if old_x_met_width != self.__x_met_width:
            old_step = self._step_grid
            new_step = self._update_step_x()
            old_width_px = new_step / self._real_size * self.__w
            if old_step > new_step:
                if old_width_px <= self.__x_met_width:
                    self._force_redraw()
                    self._step_grid = new_step
                else:
                    self._step_grid = old_step

    def __draw_grid_angles(self):
        angle_step_degrees = 30
        angles = arange(0, pi, radians(angle_step_degrees))

        metrics = QFontMetrics(self.__font)
        for angle in angles:
            self._qp.setPen(QPen(QColor(0), 0.5, Qt.PenStyle.SolidLine))
            self._qp.setBrush(QColor(0, 0, 0, 0))

            p0 = QPointF(self._real_polar_to_window_x(self._min_value, angle), self._real_polar_to_window_y(self._min_value, angle))
            p1 = QPointF(self._real_polar_to_window_x(self._max_value, angle), self._real_polar_to_window_y(self._max_value, angle))
            self._qp.drawLine(p0, p1)

            x_win = self._real_polar_to_window_x(self._stop_value, 0)
            r_win = x_win - self._real_polar_to_window_x(0, 0)
            max_radius = r_win
            self._qp.setPen(QColor(0))

            text = str(round(degrees(angle))) + "°"
            self._draw_angle_text(text, metrics, max_radius, angle)
            text = str(round(degrees(angle) + 180)) + "°"
            self._draw_angle_text(text, metrics, max_radius, angle + pi)

    def _draw_angle_text(self, text: str, metrics: QFontMetrics, max_radius: float, angle_radians: float, draw_rect=False):
        text_w = metrics.horizontalAdvance(text)
        h = metrics.height()
        r = sqrt(0.5 * text_w ** 2 + (0.5 * h) ** 2)
        r_center = max_radius - r
        x_win_center = r_center * cos(angle_radians) + self.width() / 2
        y_win_center = r_center * sin(-angle_radians) + self.height() / 2
        rect = QRectF(x_win_center - text_w / 2, y_win_center - h / 2, text_w, h)

        if draw_rect:
            self._qp.setPen(QColor(0, 0, 0, 0))
            self._qp.setBrush(0x00A2E8)
            outer_rect = QRectF(rect)
            outer_rect.setX(rect.x() - 5)
            outer_rect.setY(rect.y() - 2)
            outer_rect.setWidth(rect.width() + 10)
            outer_rect.setHeight(rect.height() + 4)
            self._qp.drawRoundedRect(outer_rect, 5, 5)

        if not draw_rect:
            self._qp.setPen(QColor(0, 0, 0, 0))
            self._qp.setBrush(QColor(0xFFFFFF))
            self._qp.drawRect(rect)
            self._qp.setPen(QColor(0, 0, 0))
        else:
            self._qp.setPen(QPen(0xFFFFFF))
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
