from math import log10, floor, ceil
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QTimer, Qt, pyqtSlot as Slot, QLineF, QRectF
from PyQt6.QtGui import QPainter, QPen, QColor, QFont, QFontMetrics

from .color_generator import ColorGenerator
from .bar_data import BarData
from .utils import *
from .array_utils import *

class BarChart(QWidget):
    def __init__(self, widget: QWidget, x: int, y: int, w: int, h: int):
        super().__init__(widget)

        self.__color_generator = ColorGenerator()
        self.__data = BarData()

        self._MIN_X = 40
        self._MAX_X = w - 40
        self._MIN_Y = 20
        self._MAX_Y = h - 40

        self.__draw_ticks = False
        self.__ystart = 0.0
        self.__ystop = 1.0
        self.__real_height = 1.0
        self.__step_grid_y = 0.25
        self.__y_label = "Y"
        self.__label_height = 10
        self.__label_width = 10
        self.__font = QFont("Bahnschrift, Arial", 11)
        self.__pen_major = QPen(QColor(145, 145, 145), 0.5)
        self.__pen_major.setStyle(Qt.PenStyle.SolidLine)
        self.__legend = True
        self.__legend_loc = 'left'
        self.__dark = False

        self.setGeometry(x, y, w, h)

        self.__qp = QPainter()
        self.__redraw_required = True
        self.__tmr = QTimer(self)
        self.__tmr.timeout.connect(self.__timeout_event)
        self.__tmr.start(50)

    def setGeometry(self, x, y, w, h):
        self.__x = x
        self.__y = y
        self.__w = w
        self.__h = h
        self._MIN_X = 40
        self._MAX_X = self._MIN_X + w
        self._MIN_Y = 20
        self._MAX_Y = self._MIN_Y + h
        super().setGeometry(x - self._MIN_X, y - self._MIN_Y, w + self._MIN_X, h + 2 * self._MIN_Y)
        self.__update_step_y()
        self.__recalculate_window_coords()

    @Slot()
    def __timeout_event(self):
        if self.__redraw_required:
            self.update()
            self.__redraw_required = False

    def add_bar_chart(self, categories: list[str], values, value_names: list[str] | None = None, y_label="Y", value_colors=None, draw_legend=True, legend_loc='left'):
        self.__data.categories = categories
        self.__data.values = values
        if value_colors and len(value_colors) == len(categories):
            self.__data.colors = value_colors
        else:
            self.__data.colors = [self.__color_generator.get_color() for _ in range(len(categories))]

        self.__data.value_names = value_names

        if hasattr(values[0], "__iter__"):
            max_y = max(max(y for y in val) for val in values)
            min_y = min(min(y for y in val) for val in values)
            self.__data.n_values = len(values[0])
        else:
            max_y = max(values)
            min_y = min(values)
            self.__data.n_values = 1
        
        height = max_y - min_y
        self.__ystop = max_y + height * 0.05
        if min_y >= 0:
            self.__ystart = 0.0
        else:
            self.__ystart = min_y - height * 0.05
        self.__real_height = self.__ystop - self.__ystart

        self.__y_label = y_label
        self.__legend = draw_legend
        self.__legend_loc = legend_loc if legend_loc == 'right' else 'left'
        self.__recalculate_window_coords()
        self.__update_step_y()
        self.__redraw_required = True

    def paintEvent(self, a0):
        self.__qp.begin(self)
        self.__qp.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        self.__draw_axes()
        self.__draw_value_rects()
        self.__draw_legend()

        self.__qp.end()

    def __draw_axes(self):
        self.__qp.setPen(QColor(0, 0, 0, 0))
        self.__qp.setBrush(QColor(0xFFFFFF))

        self.__qp.drawRect(self._MIN_X, self._MIN_Y, self.__w, self.__h)
        self.__draw_grid_y()

    def __draw_grid_y(self):
        font = QFont(self.__font)
        font.setBold(True)
        self.__qp.setFont(font)
        self.__label_height = QFontMetrics(font).height()

        txt_pen = QPen(0xD2D2D2) if self.__dark else QPen(0)
        self.__qp.setPen(txt_pen)

        max_y_label_width = QFontMetrics(font).horizontalAdvance(self.__y_label) + 10
        self.__qp.drawText(self._MIN_X - max_y_label_width - 10, self._MIN_Y, max_y_label_width, self.__label_height,
                        Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, self.__y_label)  # имя оси У
        
        font.setBold(False)
        self.__qp.setFont(font)

        y0 = round_custom(self.__ystart, self.__step_grid_y)
        y_metki_coords = arange(y0, self.__ystop + self.__step_grid_y, self.__step_grid_y)

        divised_step = self.__step_grid_y
        digit_count = max(get_digit_count_after_dot(round(y, 10)) for y in y_metki_coords)
        digit_count = max(get_digit_count_after_dot(divised_step), digit_count)
        if divised_step < 0.5:
            digit_count = max(2, digit_count)

        for y in y_metki_coords:
            y_w = self.__real_to_window_y(y)

            if (self._MIN_Y < y_w < self._MAX_Y) or y == 0:
                if (y != 0 and self.__draw_ticks) or (y == 0 and self.__ystart < 0):
                    self.__qp.setPen(self.__pen_major)
                    self.__qp.drawLine(QLineF(self._MIN_X, y_w, self._MAX_X, y_w))
                self.__qp.setPen(txt_pen)
                tmp_str = self.__get_rounded_tick(y, divised_step, digit_count)

                tmp_str_width = QFontMetrics(font).horizontalAdvance(tmp_str) + 10
                max_y_label_width = max(max_y_label_width, tmp_str_width)

                if y_w > self._MIN_Y + self.__label_height + 15:
                    self.__qp.drawText(QRectF(self._MIN_X - 110, y_w - 10, 100, 20),
                                        Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, tmp_str)
        
        if self.__label_width != max_y_label_width:
            self.__label_width = max_y_label_width
            self.__resize_frame()

    def __resize_frame(self):
        self._MIN_X = self.__label_width
        self._MAX_X = self._MIN_X + self.__w
        super().setGeometry(self.__x - self._MIN_X, self.__y - self._MIN_Y, self.__w + self._MIN_X, self.__h + 2 * self._MIN_Y)
        self.__recalculate_window_coords()
        self.update()

    def __draw_value_rects(self):
        val_font = QFont("Consolas, Courier New", 10)
        metrics = QFontMetrics(val_font)
        val_height = metrics.height()

        for i, rects_val in enumerate(self.__data.rects):
            self.__qp.setPen(QColor(0, 0, 0, 0))
            self.__qp.setBrush(QColor(self.__data.colors[i]))
            self.__qp.drawRects(rects_val)
            self.__qp.setPen(QColor(0))
            for j, name in enumerate(self.__data.categories):
                if i == 0:
                    self.__qp.setFont(self.__font)
                    self.__qp.drawText(QRectF(rects_val[j].x(), self._MAX_Y + 2, rects_val[j].width() * self.__data.n_values, 15),
                                    Qt.AlignmentFlag.AlignCenter, name)
                    
                    # self.__qp.setPen(QPen(QColor(0), 0.25))
                    # self.__qp.drawLine(QLineF(rects_val[j].x(), self._MIN_Y, rects_val[j].x(), self._MAX_Y))

                tmp_str = f"{self.__data.values[j][i]}"
                val_width = metrics.horizontalAdvance(tmp_str)
                rect_x = rects_val[j].x() + (rects_val[j].width() - val_width) / 2
                rect_y = (rects_val[j].y() - 17) if self.__data.values[j][i] >= 0 else (rects_val[j].y() + 2)

                self.__qp.setFont(val_font)
                self.__qp.drawText(QRectF(rect_x, rect_y, val_width, val_height),
                                Qt.AlignmentFlag.AlignCenter, tmp_str)

    def __draw_legend(self):
        if not self.__legend:
            return
        w = 20
        if self.__legend_loc == 'left':
            x0 = self._MIN_X + 5
        else:
            x0 = self._MAX_X - 5
        y0 = self._MIN_Y + 5
        self.__qp.setFont(self.__font)
        metrics = QFontMetrics(self.__font)
        h = metrics.height()
        if self.__data.value_names:
            for i, name in enumerate(self.__data.value_names):
                text_width = metrics.horizontalAdvance(name)
                self.__qp.setPen(QColor(0))

                if self.__legend_loc == 'left':
                    text_x0 = x0 + w + 5
                else:
                    text_x0 = x0 - text_width
                self.__qp.drawText(QRectF(text_x0, y0, text_width, metrics.height()), Qt.AlignmentFlag.AlignCenter, name)
            
                self.__qp.setPen(QColor(0, 0, 0, 0))
                self.__qp.setBrush(QColor(self.__data.colors[i]))
                if self.__legend_loc == 'left':
                    self.__qp.drawRect(x0, y0, w, h)
                    x0 += w + 5 + text_width + 10
                else:
                    self.__qp.drawRect(x0 - text_width - w - 5, y0, w, h)
                    x0 -= w + 5 + text_width + 10

    def __recalculate_window_coords(self):
        try:
            step_x = self.__w / (len(self.__data.categories))
        except ZeroDivisionError:
            return
        gap = 0.15
        width_for_all_rects = step_x * (1 - 2 * gap)
        width = width_for_all_rects / self.__data.n_values
        
        y0 = self.__real_to_window_y(0)
        self.__data.rects = list()
        if self.__data.n_values > 1:
            for i_val in range(self.__data.n_values):
                self.__data.rects.append(list())
                for i_cat in range(len(self.__data.categories)):
                    x0 = self._MIN_X + step_x * (i_cat + gap) + width * i_val
                    y = self.__real_to_window_y(self.__data.values[i_cat][i_val])
                    self.__data.rects[-1].append(QRectF(x0, y, width, y0 - y))
        else:
            self.__data.rects.append(list())
            for i_cat in range(len(self.__data.categories)):
                x0 = self._MIN_X + step_x * (i_cat + gap)
                y = self.__real_to_window_y(self.__data.values[i_cat])
                self.__data.rects[-1].append(QRectF(x0, y, width, y0 - y))
    
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

    def __update_step_y(self) -> float:
        """Вычисление шага по оси У"""
        if self.__ystart == self.__ystop:
            self.__ystart -= 0.5
            self.__ystop += 0.5
            self.__real_height = 1

        try:
            self.__step_grid_y = 10 ** (round(log10(self.__real_height)) - 1)
        except ValueError:
            self.__step_grid_y = 1.0
        n = 0

        if self.__real_height / self.__step_grid_y >= 10:
            n = 3
            while self.__real_height / self.__step_grid_y >= 10:
                n += 1
                self.__step_grid_y *= self.__get_factor(n)

        elif self.__real_height / self.__step_grid_y < 8:
            while self.__real_height / self.__step_grid_y <= 10:
                n += 1
                self.__step_grid_y /= self.__get_factor(n)

        while self.__step_grid_y / self.__real_height * self.__h < 25:  # высота не менее 30 пикселей
            n += 1
            self.__step_grid_y *= self.__get_factor(n)

        if self.__step_grid_y / self.__real_height * self.__h > 100:
            self.__step_grid_y /= self.__get_factor(n)

        return self.__step_grid_y

    def __get_factor(self, n):
        return 2.5 if n % 4 == 0 else 2
    
    def __real_to_window_y(self, y: float) -> float:
        """Перевод реальных координат оси у в оконные"""
        return c_real_to_window_y(y, self._MIN_Y, self.__h, self.__real_height, self.__ystop)
