import pickle, time
from math import log2, floor

from PyQt6.QtCore import QPointF, QLineF, QRectF, pyqtSlot, QRect
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtGui import QPainter, QPen, QColor, QFont, QFontMetrics, QPolygonF, QLinearGradient

from .axles import Axles
from .utils import *
from .color_generator import ColorGenerator
from .plot_data import Plot
from .value_rectangle import ValueRectangle
from .cornplot_window import CornplotWindow
from .point import Point
from .array_utils import *


FULL_VERSION = True
VALUE_FONT = QFont("Consolas, Courier New", 10)
VALUE_FONT.setBold(True)


class Dashboard(Axles):
    __MAX_POINTS = 5000

    def __init__(self, widget, x, y, w, h):
        super().__init__(widget, x, y, w, h)

        self.__plots: list[Plot] = list()

        self.__color_generator = ColorGenerator()
        self.__zero_y_fixed = False
        self.__window: CornplotWindow | None = None

        self._pointsToSelect = 0
        self._selectingPointGraph = -1
        self.__selected_point = SelectedPoint(0, 0, -1)

        self.__points: dict[str, Point] = dict()

        self.__redraw_time = 0

    def hideEvent(self, a0):
        if self.__window and self.__window.isVisible():
            self.__window.close()

    def __get_checkbox_x(self) -> int:
        chb_x = self._MIN_X
        for plt in self.__plots:
            chb_x += plt.get_checkbox_width()
        return chb_x

    def add_plot(self, x_arr, y_arr=None, name='', linewidth=2, linestyle='solid',
                 color='any', accurate=False, initial_ts=0) -> int:
        """Добавить статичный график для отображения"""

        if not hasattr(x_arr, "__iter__"):
            return False
        if y_arr is None:
            y_arr = x_arr
            x_arr = list(range(len(y_arr)))
        elif not hasattr(y_arr, "__iter__"):
            return False
        if len(x_arr) != len(y_arr) or len(x_arr) < 2:
            return False

        # все значения графика в одной точке
        if max(x_arr) - min(x_arr) == 0 and max(y_arr) - min(y_arr) == 0:
            return False
        
        self.set_initial_timestamp(initial_ts)

        x_tmp = list(x_arr)
        y_tmp = list(y_arr)
        if len(name) == 0:
            name = f"График {len(self.__plots) + 1}"
    
        self.__plots.append(Plot(self, x_tmp, y_tmp, self.__get_pen(color, linewidth, linestyle), 
                                 name=name, accurate=accurate, hist=False, checkbox_x=self.__get_checkbox_x()))
        self.__plots[-1].redraw_signal.connect(self.__process_checkbox_press)
        self.__plots[-1].set_dark(self.dark)

        max_x = max(x_tmp)
        min_x = min(x_tmp)
        if min_x < self._x_axis_min or len(self.__plots) == 1:
            if self._x_axle.logarithmic:
                if min_x > 0:
                    self._x_axis_min = min_x
                else:
                    self._x_axis_min = 0.01
            else:
                self._x_axis_min = min_x
        self._set_x_start(self._x_axis_min)

        if max_x >= self._x_axis_max or len(self.__plots) == 1:
            self._x_axis_max = max_x
        self._set_x_stop(self._x_axis_max)

        self._calculate_y_parameters()
        self._recalculate_window_coords()
        self._update_step_y()
        self._update_step_x()
        self._update_x_borders(self._x_axis_min, self._x_axis_max)

        if self.__window:
            self.__window.update_plot_info(self.__plots)

        self._force_redraw()
        return True
    
    def update_plot(self, name: str, x_arr, y_arr=None, rescale_x=False, rescale_y=False):
        if not hasattr(x_arr, "__iter__"):
            return False
        if y_arr is None:
            y_arr = x_arr
            x_arr = list(range(len(y_arr)))
        elif not hasattr(y_arr, "__iter__"):
            return False
        
        for plt in self.__plots:
            if plt.name == name:
                x_tmp = list(x_arr)
                y_tmp = list(y_arr)
                plt.update_x_array(array('d', x_tmp))
                plt.update_y_array(array('d', y_tmp))

                max_x = max(x_tmp)
                min_x = min(x_tmp)
                if min_x < self._x_axis_min or len(self.__plots) == 1:
                    if self._x_axle.logarithmic:
                        if min_x > 0:
                            self._x_axis_min = min_x
                        else:
                            self._x_axis_min = 0.01
                    else:
                        self._x_axis_min = min_x

                if max_x >= self._x_axis_max or len(self.__plots) == 1:
                    self._x_axis_max = max_x

                if len(self.__plots) == 1:
                    self._set_x_start(self._x_axis_min)
                    self._set_x_stop(self._x_axis_max)
                    self._update_x_borders(self._x_axis_min, self._x_axis_max)
                if rescale_y:
                    self._calculate_y_parameters()
                self._recalculate_window_coords()
                self._update_step_y()
                self._update_step_x()
                self._force_redraw()
                break
    
    def add_animated_plot(self, name: str, color='any', x_size=30, linewidth=2, linestyle='solid') -> bool:
        if len(name) == 0:
            return False
        
        if len(self.__plots) == 0 or self._real_width < x_size:
            self._xstop = x_size
            self._x_axis_max = x_size
            self._real_width = x_size
            self._xstart = 0
            self._x_axis_min = 0
            self._update_step_x()
            self._update_x_borders(self._x_axis_min, self._x_axis_max)
        self.__plots.append(Plot(self, list(), list(), self.__get_pen(color, linewidth, linestyle), name=name, checkbox_x=self.__get_checkbox_x(), animated=True, x_size=x_size))
        self.__plots[-1].redraw_signal.connect(self.__process_checkbox_press)
        self.__plots[-1].set_dark(self.dark)
        self._set_animated(True)
        return True
    
    def add_histogram(self, data, interval_count=0, name="", color="any"):
        if interval_count <= 0:
            interval_count = 1 + floor(log2(len(data)))

        x0 = min(data)
        xk = max(data)

        y = [0] * interval_count
        n_bin = 0
        intervals = [x0 + (xk - x0) / interval_count * i for i in range(interval_count + 1)]
        x = [(intervals[i + 1] + intervals[i]) / 2 for i in range(interval_count)]

        for val in np.sort(data):
            while val > intervals[n_bin + 1] and n_bin < interval_count - 1:
                n_bin += 1
            try:
                y[n_bin] += 1
            except IndexError:
                y[n_bin - 1] += 1

        if color == 'any':
            color = self.__color_generator.get_color()
            heatmap = False
        elif color == 'heatmap':
            heatmap = True
            color = self.__color_generator.get_color()
        else:
            color = color
            heatmap = False

        pen = QPen(QColor(color), 2)
        pen.setStyle(Qt.PenStyle.SolidLine)
        if len(name) == 0:
            name = f"Гистограмма {len(self.__plots) + 1}"

        self.__plots.append(Plot(self, x, y, pen, name=name, accurate=True, hist=True, heatmap=heatmap, checkbox_x=self.__get_checkbox_x()))
        self.__plots[-1].redraw_signal.connect(self.__process_checkbox_press)
        self.__plots[-1].set_dark(self.dark)

        if x0 < self._x_axis_min or len(self.__plots) == 1:
            self._x_axis_min = x0
        if xk >= self._x_axis_max or len(self.__plots) == 1:
            self._x_axis_max = xk

        if self._x_axis_min < self._xstart:
            self._xstart = self._x_axis_min
        if self._x_axis_max > self._xstop:
            self._xstop = self._x_axis_max
        self._real_width = self._xstop - self._xstart

        self._calculate_y_parameters()
        self._recalculate_window_coords()
        self._update_step_y()
        self._update_step_x()
        self._update_x_borders(self._x_axis_min, self._x_axis_max)

        if self.__window:
            self.__window.update_plot_info(self.__plots)
        self._force_redraw()

        return True

    def add_point_to_animated_plot(self, name, x: float, y: float) -> bool:
        if self.is_paused():
            return
        for plt in self.__plots:
            if plt.name == name:
                if plt.animated:
                    x, y = plt.add_element(x, y)

                    if x > self._xstop:
                        self._xstop = x
                        self._x_axis_max = x
                        self._xstart = self._xstop - self._real_width
                        self._x_axis_min = self._xstart
                        self._update_x_borders(self._xstart, self._xstop)

                    self._calculate_y_parameters()
                    self._update_step_y()

                    self._recalculate_window_coords()

                    if len(plt.X) > 2 and plt.X[-1] - plt.X[-2] > plt.x_size:
                        self.restart_animation()
                    return True
                else:
                    break

        return False
    
    @pyqtSlot()
    def __process_checkbox_press(self):
        self._calculate_y_parameters()
        self._update_step_y()
        self._recalculate_window_coords()
        self.update()

    def __get_pen(self, color, linewidth: float, linestyle: str) -> QPen:
        if color == 'any':
            color = self.__color_generator.get_color()
        else:
            color = color

        pen = QPen(QColor(color), linewidth)
        if linestyle == 'dash':
            pen.setStyle(Qt.PenStyle.DashLine)
        elif linestyle == 'dot':
            pen.setStyle(Qt.PenStyle.DotLine)
        elif linestyle == 'dash-dot':
            pen.setStyle(Qt.PenStyle.DashDotLine)
        elif linestyle == 'dash-dot-dot':
            pen.setStyle(Qt.PenStyle.DashDotDotLine)
        else:
            pen.setStyle(Qt.PenStyle.SolidLine)
        pen.setCapStyle(Qt.PenCapStyle.SquareCap)
        pen.setWidthF(linewidth)
        return pen

    def delete_all_plots(self) -> None:
        """Удалить все графики"""
        self._xstart = 0
        self._xstop = 10
        self._ystart = 0
        self._ystop = 1

        self._x_axis_min = 0
        self._x_axis_max = 10
        self._y_axis_min = 0
        self._y_axis_max = 1
        self._real_width = self._xstop - self._xstart
        self._real_height = self._ystop - self._ystart
        self.__plots.clear()
        self._force_redraw()
        self._update_step_x()
        self._update_step_y()
        self.__color_generator.reset()
    
    def delete_plot(self, name):
        index = -1
        for i, plt in enumerate(self.__plots):
            if plt.name == name:
                index = i
                break
        if index == -1:
            return

        self.__plots.pop(index)

        self._calculate_x_parameters()
        self._calculate_y_parameters()
        self._update_step_y()
        self._recalculate_window_coords()
        self.__color_generator.one_color_back()

        self.__window.update_plot_info(self.__plots)
        self.__window.display_plot_info()

        w = self._MIN_X
        for plt in self.__plots:
            plt.set_checkbox_x(w)
            w += plt.get_checkbox_width()

        self.update()

    @pyqtSlot(int, int)
    def __begin_point_selection(self, plt_num, n_points=1):
        if plt_num >= len(self.__plots) or self.is_animated() and not self.is_paused():
            return
        self.__plots[plt_num].selectedPoints.clear()
        self._selectingPointGraph = plt_num
        self._pointsToSelect = n_points
    
    def _redraw(self):
        if not self.visible:
            return
        t0 = time.time()
        super()._redraw()

        scanner_coords = self._scanner_coords()
        n_scanners = self._scanner_count()
        value_rects: list[list[ValueRectangle]] = [list() for _ in range(n_scanners)]
        
        self._qp.setClipRect(QRectF(self._MIN_X, self._MIN_Y - 1, self.width(), self.height() - self._OFFSET_Y_UP - self._OFFSET_Y_DOWN + 1))
        for plt in self.__plots:
            if plt.visible:
                self.__redraw_plot(plt)
    
                for i in range(n_scanners):
                    rects = self.__create_value_pointer(scanner_coords[i], plt)
                    if rects:
                        for rect in rects:
                            value_rects[i].append(rect)

        self.__draw_points()
        self._qp.setClipRect(QRectF(0, 0, self.width(), self.height()))
        
        for rects in value_rects:
            for i_fixed in range(len(rects)):
                for i_mobile in range(i_fixed + 1, len(rects)):
                    if not rects[i_mobile].intersects(rects[i_fixed]):
                        continue
                    if rects[i_mobile].move_left:
                        rects[i_mobile].moveLeft(rects[i_fixed].x() - rects[i_mobile].width() - 5)
                    else:
                        rects[i_mobile].moveLeft(rects[i_mobile].x() + rects[i_fixed].width() + 5)
        
        self._draw_scale_lines()
        self._draw_scaling_rect()
        self._draw_scanner_lines(value_rects)
        self.__draw_point_on_graph()
        self._draw_x_slider()
        if not self.is_animated() or self.is_paused():
            self._redraw_required = False
        
        
        self.__redraw_time = time.time() - t0

    def __create_value_pointer(self, xwin, plt: Plot):
        if len(plt.Y) <= 1:
            return None
        x_real = self._window_to_real_x(xwin - self._MIN_X)
        nearest = plt.get_nearest(x_real)

        res = tuple()
        for _, i in nearest:
            y = plt.Y[i]
            ywin = max(self._real_to_window_y(y), self._MIN_Y)
            ywin = min(ywin, self._MAX_Y)

            if len(nearest) > 1 and (y > self._ystop or y < self._ystart):
                continue

            digits_count = get_digit_count_after_dot(self._step_grid_y) + 1
            if self._step_grid_y <= 1.0:
                digits_count = max(3, digits_count)
            y /= self._y_axle.divisor

            tmp_str = round_value(y, digits_count)

            text_width = QFontMetrics(VALUE_FONT).horizontalAdvance(tmp_str)

            yrect = ywin
            wrect = text_width + 10
            if xwin < self.width() / 2:
                xrect = xwin + 10
            else:
                xrect = xwin - wrect - 10
            hrect = 18

            yrect = min(yrect, self._value_rect_max_y)

            res += ValueRectangle(xrect, yrect, wrect, hrect, tmp_str, plt.pen.color(), QPointF(xwin, ywin), xwin > self.width() / 2),
            if len(res) > 4:
                break
        return res

    def _resize_frame(self):
        super()._resize_frame()
        x = self._MIN_X
        for plt in self.__plots:
            plt.set_checkbox_x(x)
            x += plt.get_checkbox_width()

    def _draw_scanner_lines(self, value_rects):
        super()._draw_scanner_lines()
        for rects in value_rects:
            for rect in rects:
                self._qp.setPen(QColor(255, 255, 255, 127))
                self._qp.setBrush(rect.color)
                self._qp.drawRoundedRect(rect, 5, 5)
                self._qp.setPen(QColor(255, 255, 255))
                self._qp.setFont(VALUE_FONT)
                self._qp.drawText(rect, Qt.AlignmentFlag.AlignCenter, rect.text)
                
                self._qp.setPen(QPen(rect.color, 10, Qt.PenStyle.DashLine, Qt.PenCapStyle.RoundCap))
                self._qp.drawPoint(rect.point)

    def __redraw_plot(self, plt: Plot) -> None:
        """Перерисовывание одного графика"""
        if len(plt) == 0:
            return
        
        if plt.animated and not self.is_paused():
            Xwin = c_recalculate_window_x(list(plt.X), self._MIN_X, self._get_width(), self._real_width, self._xstart, plt.index0, plt.index1 + 1, 1)       # type: ignore
            Ywin = c_recalculate_window_y(list(plt.Y), self._MIN_Y, self._get_heignt(), self._real_height, self._ystop, plt.index0, plt.index1 + 1, 1)      # type: ignore
            if plt.draw_line and plt.pen.style() == Qt.PenStyle.SolidLine:
                plt.lines = [QLineF(Xwin[i - 1], Ywin[i - 1], Xwin[i], Ywin[i]) for i in range(1, len(Xwin))]
            if plt.draw_markers or plt.pen.style() != Qt.PenStyle.SolidLine:
                plt.points = [QPointF(x, y) for x, y in zip(Xwin, Ywin)]

            self.__draw_plot_lines_and_points(plt)
        elif plt.is_hist:
            self.__draw_histogram(plt)
        else:
            self.__draw_plot_lines_and_points(plt)

    def paintEvent(self, a0):
        self._qp.begin(self)
        self._qp.setRenderHint(QPainter.RenderHint.Antialiasing)
        self._redraw()
        self._qp.end()

    def __draw_plot_lines_and_points(self, plt: Plot):
        if plt.draw_line:
            if plt.pen.style() == Qt.PenStyle.SolidLine:
                self._qp.setPen(QPen(plt.pen.color(), plt.pen.widthF()))
                self._qp.drawLines(plt.lines)
            else:
                self._qp.setPen(QPen(plt.pen.color(), plt.pen.widthF(), plt.pen.style()))
                self._qp.drawPolyline(plt.points)
        if plt.draw_markers:
            pen = QPen(plt.pen)
            pen.setWidthF(plt.marker_width)
            self._qp.setPen(pen)
            self._qp.drawPoints(plt.points)

    def __draw_histogram(self, plt: Plot):
        if not plt.x_ascending or len(plt) == 0:
            return

        if not plt.heatmap:
            self._qp.setPen(QColor(0, 0, 0))
            self._qp.setBrush(plt.pen.color())
            self._qp.drawRects(plt.rects)
        else:
            gradient = Gradient(QColor(68, 1, 84), QColor(253, 231, 36))
            gradient.set_color_at(0.5, QColor(33, 141, 140))
            max_h = max(rect.height() for rect in plt.rects)
            min_h = min(rect.height() for rect in plt.rects)
            self._qp.setPen(QColor(0, 0, 0))
            for rect in plt.rects:
                h = rect.height()
                self._qp.setBrush(gradient.get_color((h - min_h) / (max_h - min_h)))
                self._qp.drawRect(rect)

            self._qp.setPen(QColor(0, 0, 0, 0))
            x = self._MIN_X + 5
            y = self._MIN_Y + 5
            w = int(self.width() * 0.2)
            h = 20
            gradient = QLinearGradient(x, y, x + w, y + h)
            gradient.setColorAt(0, QColor(68, 1, 84))
            gradient.setColorAt(0.5, QColor(33, 141, 140))
            gradient.setColorAt(1, QColor(253, 231, 36))

            self._qp.setBrush(gradient)
            self._qp.drawRect(x, y, w, h)

            self._qp.setPen(QColor(210, 210, 210) if self.dark else QColor(0, 0, 0))
            self._qp.setFont(QFont("Consolas, Arial", 8))
            self._qp.drawText(x, y + h + 10, str(min(plt.Y)))
            self._qp.drawText(x + w - 15, y + h + 10, str(max(plt.Y)))

    def take_plot_screenshot(self, name: str):
        if self.is_animated():
            self.pause(True)
        for plt in self.__plots:
            if plt.name != name:
                plt.set_checkbox_state(False)
            else:
                plt.set_checkbox_state(True)

        major_enabled = self.major_ticks_enabled
        minor_enabled = self.minor_ticks_enabled
        self.enable_minor_grid(False)
        self.enable_major_grid(False)
        self._set_buttons_visible(False)
        grab = self.grab(QRect(self._MIN_X, self._MIN_Y, self.width() - self._MIN_X, self.height() - 47))

        for plt in self.__plots:
            plt.set_checkbox_state(True)
        self.enable_minor_grid(minor_enabled)
        self.enable_major_grid(major_enabled)
        self._set_buttons_visible(True)
        
        return grab

    def _calculate_x_parameters(self):
        if self.is_animated() and not self.is_paused():
            return
        if len(self.__plots) > 0:
            minimums = [plt.min(0) for plt in self.__plots if plt.visible]
            maximums = [plt.max(0) for plt in self.__plots if plt.visible]
            if len(minimums) > 0:
                min_x = min(minimums)
                max_x = max(maximums)
            else:
                min_x = self._xstart
                max_x = self._xstop
            if min_x == max_x:
                max_x += 10
        else:
            min_x = 0
            max_x = 10
        if self._x_axle.logarithmic:
            self._x_axis_min = min_x if min_x > 0 else 0.01
        else:
            self._x_axis_min = min_x
        self._x_axis_max = max_x
        if self._xstart < self.x_axis_min:
            self._set_x_start(self.x_axis_min)
        if self._xstop > self.x_axis_max:
            self._set_x_stop(self.x_axis_max)

    def _calculate_y_parameters(self) -> None:
        """Пересчёт параметров оси У. Нужен при вертикальном масштабировании
        или если график оказывается выше текущей верхней границы"""

        super()._calculate_y_parameters()

        if len(self.__plots) > 0:
            try:
                self._y_axis_max = max([plt.max(1) for plt in self.__plots if plt.visible])
                self._y_axis_min = min([plt.min(1) for plt in self.__plots if plt.visible])
            except ValueError:
                self._y_axis_max = 1
                self._y_axis_min = 0

            if self._y_axle.logarithmic and self._y_axis_min <= 0:
                self._y_axis_min = 0.01
            if self._y_axle.logarithmic and self._y_axis_max <= self._y_axis_min:
                self._y_axis_max = 0.1
        else:
            self._y_axis_max = 1
            self._y_axis_min = 0 if not self._y_axle.logarithmic else 0.01

        if not self._y_scaled:
            self._set_y_start(0 if not self._y_axle.logarithmic else self._y_axis_min)
            self._set_y_stop(1)
        max_y_list = []
        min_y_list = []
        for plt in self.__plots:
            if not plt.visible or len(plt) == 0:
                continue
            self.__find_indexes(plt)
            max_y_list.append(plt.max(1))
            min_y_list.append(plt.min(1))
        if len(max_y_list) == 0:
            return

        max_y = max(max_y_list)
        min_y = min(min_y_list)
        if max_y == min_y:
            max_y += abs(max_y * 0.1)
            min_y -= abs(min_y * 0.1)

        if self.__zero_y_fixed:
            if min_y > 0:
                min_y = 0
            if max_y < 0:
                max_y = 0
        self._Y_STOP_COEFF = (max_y - min_y) / self._Y_STOP_RATIO

        if not self._y_scaled:
            if self._y_axle.logarithmic:
                self._set_y_start(self._y_axis_min)
                self._set_y_stop(self._y_axis_max)
            else:
                ystart = min_y if self.__zero_y_fixed and min_y == 0 else min_y - self._Y_STOP_COEFF
                ystop = max_y if self.__zero_y_fixed and max_y == 0 else max_y + self._Y_STOP_COEFF
                self._set_y_start(ystart)
                self._set_y_stop(ystop)
        
        if self._y_axis_max == self._y_axis_min:
            self._y_axis_max += 10

    def __draw_point_on_graph(self):
        if self._selectingPointGraph < 0:
            return

        self._qp.setPen(QColor(0, 0, 0, alpha=255))
        # вертикальная линия у текущей выбираемой точки
        self._qp.drawLine(QLineF(self.__selected_point.x, self._MIN_Y, self.__selected_point.x, self._MAX_Y))

        # сама точка
        self._qp.setPen(QColor(0, 0, 0, alpha=0))
        self._qp.setBrush(QColor(103, 103, 52, alpha=200))
        self._qp.drawEllipse(QPointF(self.__selected_point.x, self.__selected_point.y), 5, 5)

        # возня с прямоугольником со значением
        font = QFont("Consolas, Courier New", 10)
        font.setBold(True)
        self._qp.setFont(font)
        qm = QFontMetrics(font)
        tmp_str = f"{self._window_to_real_x(self.__selected_point.x - self._MIN_X):.2f}; " \
                  f"{self._window_to_real_y(self.__selected_point.y - self._MIN_Y + self._OFFSET_Y_UP):.2f}"  # координаты
        text_width = qm.size(0, tmp_str).width()

        self._qp.setBrush(QColor(0, 162, 232, alpha=255))
        rectX = self.__selected_point.x + 10
        if rectX < self._MIN_X:
            rectX = self.__selected_point.x + 10 + self._MIN_X
        rectW = text_width + 10
        rectH = 17
        rectY = self.__selected_point.y

        tmp_str1 = f"Осталось выбрать: {self._pointsToSelect}"
        text_width1 = qm.size(0, tmp_str1).width()
        rectX1 = rectX - 30 - text_width1
        rectW1 = text_width1 + 10
        rectH1 = 17

        if rectX > self._MAX_X - 200 and rectY >= self._MAX_Y - 60:
            rectY -= 50
        if rectX > self._MAX_X - rectW - 10:
            rectX -= rectW + 20
        rectY1 = rectY - 30
        self._qp.drawRoundedRect(QRectF(rectX, rectY, rectW, rectH), 5, 5)
        self._qp.setPen(QColor(255, 255, 255, alpha=255))
        self._qp.drawText(QRectF(rectX, rectY, rectW, rectH), Qt.AlignmentFlag.AlignCenter, tmp_str)
        self._qp.setBrush(QColor(29, 69, 154, alpha=255))
        self._qp.setPen(QColor(0, 0, 0, alpha=0))

        if rectX1 <= self._MIN_X:
            rectX1 += rectW1 + 10

        self._qp.drawRoundedRect(QRectF(rectX1, rectY1, rectW1, rectH1), 5, 5)
        self._qp.setPen(QColor(255, 255, 255, alpha=255))
        self._qp.drawText(QRectF(rectX1, rectY1, rectW1, rectH1), Qt.AlignmentFlag.AlignCenter, tmp_str1)

        points = self.__plots[self._selectingPointGraph].selectedPoints
        graph_x = self.__plots[self._selectingPointGraph].X
        graph_y = self.__plots[self._selectingPointGraph].Y

        # если первая точка уже выбрана, нарисуем линию на её месте
        if len(points) == 1:
            x = self._real_to_window_x(points[0].x)
            self._qp.setPen(QColor(0, 0, 0, alpha=255))
            self._qp.drawLine(QLineF(x, self._MIN_Y, x, self._MAX_Y))
            self._qp.setPen(QColor(0, 0, 0, alpha=0))
            self._qp.setBrush(QColor(103, 103, 52, alpha=40))

            # нарисуем закрашенную область под графиком
            i0 = min(points[0].i, self.__selected_point.i)
            ik = max(points[0].i, self.__selected_point.i) + 1

            x_p = self._real_to_window_x(graph_x[self.__selected_point.i])
            points_list = [QPointF(max(x, x_p), min(self._real_to_window_y(0), self._MAX_Y + 1)) if i == i0 - 2
                           else QPointF(min(x, x_p), min(self._real_to_window_y(0),
                                                               self._MAX_Y + 1)) if i == i0 - 1
                           else QPointF(max(x, x_p), min(self._real_to_window_y(0), self._MAX_Y + 1)) if i == ik
                           else QPointF(self._real_to_window_x(graph_x[i]), self._real_to_window_y(graph_y[i]))
                           for i in range(i0 - 2, ik + 1)]
            self._qp.drawPolygon(QPolygonF(points_list))

    def __find_point_coords(self, x_win):
        x_real = self._window_to_real_x(x_win)
        i = self._selectingPointGraph
        _, indx = self.__plots[i].get_nearest(x_real)[0]
        self.__selected_point.x = self._real_to_window_x(self.__plots[i].X[indx])
        self.__selected_point.y = self._real_to_window_y(self.__plots[i].Y[indx])
        self.__selected_point.i = indx

    def _recalculate_window_coords(self) -> None:
        """Пересчёт массивов оконных координат графиков"""
        super()._recalculate_window_coords()
        for plt in self.__plots:
            self.__recalculate_plot_coords(plt)

    def __recalculate_plot_coords(self, plt: Plot):
        if plt.animated and not self.is_paused():
            return
        self.__find_indexes(plt)
        step = 1 if plt.accurate else max(1, int((1 + plt.index1 - plt.index0) / self.__MAX_POINTS))
        self.__recalculate_window_xy(plt, step)

    def __find_indexes(self, plot: Plot):
        """нахождение индексов начальной и конечной отображаемых точек"""
        if not self.is_animated() and (plot.X[-1] < self._xstart or plot.X[0] > self._xstop):
            return
        plt_len = len(plot)

        if not plot.x_ascending:
            plot.index0 = 0
            plot.index1 = plt_len - 1
            return

        if plt_len < 3:
            return
        try:
            tmp = int(plt_len * (abs(self._xstart - self._x_axis_min) / (self._x_axis_max - self._x_axis_min))) - 1
        except ZeroDivisionError:
            return
        # предположительный индекс начальной точки
        tmp = min(tmp, plt_len - 1)
        while tmp > 0 and plot.X[tmp] > self._xstart:
            tmp -= 1
        if tmp < 0:
            tmp = 0

        plot.index0 = tmp

        tmp = int(plt_len * (abs(self._xstop - self._x_axis_min) /
                                 (self._x_axis_max - self._x_axis_min))) - 1
        # предположительный индекс конечной точки
        while tmp < plt_len - 1 and plot.X[tmp] < self._xstop:
            tmp += 1
        if tmp > plt_len - 1:
            tmp = plt_len - 1
        plot.index1 = tmp

    def __recalculate_window_xy(self, plt: Plot, step):
        Xwin = self.__recalculate_plot_x(plt, step)
        Ywin = self.__recalculate_plot_y(plt, step)
        
        length = plt.index1 - plt.index0
        if length == 0:
            return

        if plt.is_hist:
            width = Xwin[1] - Xwin[0]
            half_width = width * .5
            y_zero = self._real_to_window_y(0)
            plt.rects = [QRectF(x - half_width, y, width, y_zero - y) for x, y in zip(Xwin, Ywin)]
        else:
            if plt.draw_line and plt.pen.style() == Qt.PenStyle.SolidLine:
                plt.lines = [QLineF(Xwin[i - 1], Ywin[i - 1], Xwin[i], Ywin[i]) for i in range(1, len(Xwin))]
            if plt.draw_markers or plt.pen.style() != Qt.PenStyle.SolidLine:
                plt.points = [QPointF(x, y) for x, y in zip(Xwin, Ywin)]

    def __recalculate_plot_x(self, plt: Plot, step):
        if self._x_axle.logarithmic:
            return [self._real_to_window_x(plt.X[i]) for i in range(plt.index0, plt.index1, step)]
        return c_recalculate_window_x(list(plt.X), self._MIN_X, self._get_width(), self._real_width, self._xstart, plt.index0, plt.index1, step)       # type: ignore
    
    def __recalculate_plot_y(self, plt: Plot, step):
        if self._y_axle.logarithmic:
            return [self._real_to_window_y(plt.Y[i]) for i in range(plt.index0, plt.index1, step)]
        return c_recalculate_window_y(list(plt.Y), self._MIN_Y, self._get_heignt(), self._real_height, self._ystop, plt.index0, plt.index1, step)       # type: ignore
    
    def set_plot_linestyle(self, name: str, linestyle: Qt.PenStyle):
        for plt in self.__plots:
            if not plt.draw_line:
                return
            if plt.name == name and linestyle != plt.pen.style():
                plt.pen.setStyle(linestyle)
                self.__recalculate_plot_coords(plt)
                self._force_redraw()

    def set_plot_linewidth(self, name: str, linewidth: float):
        for plt in self.__plots:
            if not plt.draw_line:
                return
            if plt.name == name and linewidth != plt.pen.widthF():
                plt.pen.setWidthF(linewidth)
                self._force_redraw()

    def set_plot_markerwidth(self, name: str, width: float):
        for plt in self.__plots:
            if plt.name == name:
                plt.set_marker_width(width)
                self._force_redraw()

    def set_plot_markerstyle(self, name: str, style: Qt.PenCapStyle):
        for plt in self.__plots:
            if plt.name == name and plt.pen.capStyle() != style:
                plt.pen.setCapStyle(style)
                self._force_redraw()

    def plot_draw_line(self, name: str, draw: bool):
        for plt in self.__plots:
            if plt.name == name and draw != plt.draw_line:
                plt.draw_line = draw
                self._force_redraw()

    def plot_draw_markers(self, name: str, draw: bool):
        for plt in self.__plots:
            if plt.name == name and draw != plt.draw_markers:
                self._recalculate_window_coords()
                plt.draw_markers = draw
                self._force_redraw()
    
    def __update_extended_window(self):
        self.__window.update_plot_info(self.__plots)
        if self.__window.isVisible():
            self.__window.display_plot_info()

    def _show_extended_window(self):
        if self.__window is None:
            self.__window = CornplotWindow(self)
            self.__window.point_selection_signal.connect(self.__begin_point_selection)
        self.__window.update_plot_info(self.__plots)
        self.__window.display_plot_info()
        self.__window.show()

    def mouseMoveEvent(self, a0):
        super().mouseMoveEvent(a0)

        if self._selectingPointGraph >= 0:
            self.__find_point_coords(a0.pos().x() - self._MIN_X)
            self._force_redraw()

    def mousePressEvent(self, a0):
        super().mousePressEvent(a0)

        if a0.button() == Qt.MouseButton.LeftButton:
            if self._selectingPointGraph >= 0:     # выделение точки на графике
                self.__plots[self._selectingPointGraph].selectedPoints.append(
                    SelectedPoint(
                        self._window_to_real_x(self.__selected_point.x - self._MIN_X),
                        self._window_to_real_y(self.__selected_point.y + self._OFFSET_Y_UP),
                        self.__selected_point.i
                    )
                )
                self._point_added = True
                self._pointsToSelect -= 1
                if self._pointsToSelect == 0:
                    self.__window.set_selected_points(self.__plots[self._selectingPointGraph].selectedPoints)
                    self._selectingPointGraph = -1
                    self.__window.show()                    
                return

    def export_to_file(self, path):
        data = dict()
        data["background_color"] = self.background_color.name()
        data["plots"] = dict()
        for plt in self.__plots:
            data["plots"][plt.name] = dict()
            tmp = data["plots"][plt.name]
            tmp["color"] = plt.pen.color().name()
            tmp["linewidth"] = plt.pen.widthF()
            tmp["x"] = plt.X.tolist()
            tmp["y"] = plt.Y.tolist()
        with open(path, "wb") as f:
            pickle.dump(data, f)

    def import_from_file(self, path):
        if self.is_animated() and not self.__paused:
            return

        if len(self.__plots) > 0:
            self.__msgBox = QMessageBox()
            self.__msgBox.setIcon(QMessageBox.Icon.Question)
            self.__msgBox.setText("Все текущие графики будут удалены. Продолжить?")
            self.__msgBox.setWindowTitle("Импорт графиков")
            self.__msgBox.setStandardButtons(QMessageBox.StandardButton.Yes |
                                             QMessageBox.StandardButton.No)
            self.__msgBox.button(QMessageBox.StandardButton.Yes).setText("Да")
            self.__msgBox.button(QMessageBox.StandardButton.No).setText("Нет")

            button = self.__msgBox.exec()
            if button == QMessageBox.StandardButton.No:
                self.__msgBox.deleteLater()
                return

        try:
            with open(path, 'rb') as f:
                data: dict[str] = pickle.load(f)
        except FileNotFoundError:
            return
        
        self.delete_all_plots()
        for name in data["plots"]:
            plt = data["plots"][name]
            self.add_plot(plt["x"], plt["y"], linewidth=plt["linewidth"], name=name, color=plt["color"])
        self.set_background_color(QColor(data["background_color"]))
        if self.__msgBox:
            self.__msgBox.deleteLater()
        self.update()

    def pause(self, pause: bool):
        super().pause(pause)
        if not self.is_animated():
            return
        if pause:
            self._recalculate_window_coords()
            self._x_axis_min = self._xstart
            self._x_axis_max = self._xstop
        x_size = 10
        for plt in self.__plots:
            if plt.animated:
                x_size = plt.x_size
        if self._real_width < x_size:
            self._real_width = x_size
            self._update_step_x()

    @pyqtSlot()
    def restart_animation(self, **kwargs) -> None:
        super().restart_animation(**kwargs)
        x_size = 10

        for plt in self.__plots:
            x_size = plt.x_size
            plt.remove_all()
        self._xstart = 0
        self._real_width = x_size
        self._xstop = self._xstart + self._real_width
        self._x_axis_min = 0
        self._x_axis_max = self._real_width
        self._update_step_x()
        self._update_x_borders(self._xstart, self._xstop)

        self.pause(False)

    def set_plot_accurate(self, name: str, accurate: bool):
        for plot in self.__plots:
            if plot.name == name and plot.accurate != accurate:
                plot.accurate = accurate
                self._recalculate_window_coords()
                self._force_redraw()
                return
            
    def set_dark(self, dark: bool):
        super().set_dark(dark)
        for plt in self.__plots:
            plt.set_dark(dark)

    def create_point(self, name: str, color: QColor | str | int, size=5.0, shape="round"):
        self.__points[name] = Point(name, QColor(color), size, shape)

    def delete_point(self, name: str):
        try:
            self.__points.pop(name)
        except KeyError:
            pass

    def delete_all_points(self):
        self.__points.clear()

    def draw_point(self, name: str, x: float, y: float, text=""):
        if name in self.__points:
            self.__points[name].setX(x)
            self.__points[name].setY(y)
            self.__points[name].text = text
            self._force_redraw()

    def __draw_points(self):
        font = QFont("Consolas, Courier New", 12)
        self._qp.setFont(font)
        metr = QFontMetrics(font)

        for point in self.__points.values():
            self._qp.setPen(point.pen)
            xwin, ywin = self._real_to_window_x(point.x()), self._real_to_window_y(point.y())
            self._qp.drawPoint(QPointF(xwin, ywin))
            text_width = metr.size(0, point.text).width()
            text_height = metr.size(0, point.text).height()
            self._qp.drawText(QRectF(xwin - text_width / 2, ywin - text_height * 3 / 2, text_width, text_height),
                                Qt.AlignmentFlag.AlignCenter, point.text)

    @property
    def redraw_time(self) -> float:
        return self.__redraw_time
