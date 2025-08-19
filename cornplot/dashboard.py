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

from .array_utils import *
from array import array

FULL_VERSION = True
VALUE_FONT = QFont("consolas", 10)
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
        self.__selected_point = SelectedPoint(0, 0, -1)

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
            if self._x_logarithmic:
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
    
    def add_histogram(self, data, intervals=0, name="", color="any"):
        if intervals <= 0:
            intervals = 1 + floor(log2(len(data)))

        x0 = min(data)
        xk = max(data)

        y = [0] * intervals
        n_bin = 0
        intervals = [x0 + (xk - x0) / intervals * i for i in range(intervals + 1)]
        x = [(intervals[i + 1] + intervals[i]) / 2 for i in range(intervals)]

        for val in np.sort(data):
            while val > intervals[n_bin + 1] and n_bin < intervals - 1:
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
                    value_rects[i].append(self.__create_value_pointer(scanner_coords[i], plt))
        self._qp.setClipRect(QRectF(0, 0, self.width(), self.height()))
        
        
        for rects in value_rects:
            for i in range(len(rects)):
                for j in range(i + 1, len(rects)):
                    if rects[i] in rects[j]:
                        w = rects[j].width()
                        rects[j].setX(rects[i].x() - rects[i].width() - 5)
                        rects[j].setWidth(w)
        
        self._draw_scale_lines()
        self._draw_scaling_rect()
        self._draw_scanner_lines(value_rects)
        self.__draw_point_on_graph()
        self._redraw_required = self.is_animated() and not self.is_paused()
        
        self.__redraw_time = time.time() - t0

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
            lines = list()

            buffered_x = plt.X[0]
            buffered_x_win = self.real_to_window_x(buffered_x)
            buffered_y = plt.Y[0]
            buffered_y_win = self.real_to_window_y(buffered_y)

            for j, x in enumerate(plt.X):
                if j == 0:
                    if x > self._xstart:
                        self._xstart = x
                        self._x_axis_min = x
                    continue
                x0 = plt.X[j - 1]
                x1 = plt.X[j]
                y0 = plt.Y[j - 1]
                y1 = plt.Y[j]
                if y0 == y1:
                    # если значение У не изменилось
                    if buffered_y != y0:
                        # сохраняем значение в память, если ещё этого не сделали
                        buffered_y = y0
                        buffered_x_win = self.real_to_window_x(x0)
                        buffered_y_win = self.real_to_window_y(y0)
                else:
                    buffered_y = y0
                    buffered_x_win = self.real_to_window_x(x0)
                    buffered_y_win = self.real_to_window_y(y0)

                if self._xstart < x1 < self._xstop and self._ystart <= y1 <= self._ystop and x0 > self._xstart:
                    x = self.real_to_window_x(x1)
                    y = self.real_to_window_y(y1)
                    if plt.draw_line:
                        lines.append(QLineF(max(buffered_x_win, self._MIN_X), buffered_y_win, x, y))

                    if plt.draw_markers:
                        pen = QPen(plt.pen)
                        pen.setWidthF(plt.marker_width)
                        self._qp.setPen(pen)
                        self._qp.drawPoint(QPointF(x, y))

            self._qp.setPen(plt.pen)
            self._qp.drawLines(lines)
        elif plt.is_hist:
            self.__draw_histogram(plt)
        else:
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

    def paintEvent(self, a0):
        self._qp.begin(self)
        self._qp.setRenderHint(QPainter.RenderHint.Antialiasing)
        self._redraw()
        self._qp.end()

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
            self._qp.setFont(QFont("bahnschrift", 8))
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
        if self._x_logarithmic:
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
            self._y_axis_max = max([plt.max(1) for plt in self.__plots if plt.visible])
            self._y_axis_min = min([plt.min(1) for plt in self.__plots if plt.visible])

            if self._y_logarithmic and self._y_axis_min <= 0:
                self._y_axis_min = 0.01
            if self._y_logarithmic and self._y_axis_max <= self._y_axis_min:
                self._y_axis_max = 0.1
        else:
            self._y_axis_max = 1
            self._y_axis_min = 0 if not self._y_logarithmic else 0.01

        if not self._y_scaled:
            self._set_y_start(0 if not self._y_logarithmic else self._y_axis_min)
            self._set_y_stop(1)
        max_y_list = []
        min_y_list = []
        for plt in self.__plots:
            if not plt.visible or plt.length == 0:
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
        self.__Y_STOP_COEFF = (max_y - min_y) / self._Y_STOP_RATIO

        if not self._y_scaled:
            if self._y_logarithmic:
                self._set_y_start(self._y_axis_min)
                self._set_y_stop(self._y_axis_max)
            else:
                ystart = min_y if self.__zero_y_fixed and min_y == 0 else min_y - self.__Y_STOP_COEFF
                ystop = max_y if self.__zero_y_fixed and max_y == 0 else max_y + self.__Y_STOP_COEFF
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
        font = QFont("consolas", 10)
        font.setBold(True)
        self._qp.setFont(font)
        qm = QFontMetrics(font)
        tmp_str = f"{self.window_to_real_x(self.__selected_point.x - self._MIN_X):.2f}; " \
                  f"{self.window_to_real_y(self.__selected_point.y - self._MIN_Y + self._OFFSET_Y_UP):.2f}"  # координаты
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
            x = self.real_to_window_x(points[0].x)
            self._qp.setPen(QColor(0, 0, 0, alpha=255))
            self._qp.drawLine(QLineF(x, self._MIN_Y, x, self._MAX_Y))
            self._qp.setPen(QColor(0, 0, 0, alpha=0))
            self._qp.setBrush(QColor(103, 103, 52, alpha=40))

            # нарисуем закрашенную область под графиком
            i0 = min(points[0].i, self.__selected_point.i)
            ik = max(points[0].i, self.__selected_point.i) + 1

            x_p = self.real_to_window_x(graph_x[self.__selected_point.i])
            points_list = [QPointF(max(x, x_p), min(self.real_to_window_y(0), self._MAX_Y + 1)) if i == i0 - 2
                           else QPointF(min(x, x_p), min(self.real_to_window_y(0),
                                                               self._MAX_Y + 1)) if i == i0 - 1
                           else QPointF(max(x, x_p), min(self.real_to_window_y(0), self._MAX_Y + 1)) if i == ik
                           else QPointF(self.real_to_window_x(graph_x[i]), self.real_to_window_y(graph_y[i]))
                           for i in range(i0 - 2, ik + 1)]
            self._qp.drawPolygon(QPolygonF(points_list))

    def __find_point_coords(self, x_win):
        x_real = self.window_to_real_x(x_win)
        i = self._selectingPointGraph
        _, indx = self.__plots[i].get_nearest(x_real)[0]
        self.__selected_point.x = self.real_to_window_x(self.__plots[i].X[indx])
        self.__selected_point.y = self.real_to_window_y(self.__plots[i].Y[indx])
        self.__selected_point.i = indx

    def __recalculate_window_xy(self, plt: Plot, step):
        Xwin = [self.real_to_window_x(plt.X[i]) for i in range(plt.index0, plt.index1 + 1, step)]
        Ywin = [self.real_to_window_y(plt.Y[i]) for i in range(plt.index0, plt.index1 + 1, step)]

        length = plt.index1 - plt.index0
        if length == 0:
            return
        
        if plt.is_hist:
            width = Xwin[1] - Xwin[0]
            half_width = width * .5
            y_zero = self.real_to_window_y(0)
            plt.rects = [QRectF(x - half_width, y, width, y_zero - y) for x, y in zip(Xwin, Ywin)]
        else:
            plt.lines = [QLineF(Xwin[i - 1], Ywin[i - 1], Xwin[i], Ywin[i]) for i in range(1, len(Xwin))]
            if plt.draw_markers or plt.pen.style != Qt.PenStyle.SolidLine:
                plt.points = [QPointF(x, y) for x, y in zip(Xwin, Ywin)]

    def _recalculate_window_coords(self) -> None:
        """Пересчёт массивов оконных координат графиков.
        Делается при изменении масштаба, передвижениях осей"""

        super()._recalculate_window_coords()
        for plt in self.__plots:
            if plt.animated and not self.is_paused():
                continue
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

    def __create_value_pointer(self, xwin, plt: Plot):
        x_real = self.window_to_real_x(xwin)
        _, i = plt.get_nearest(x_real)[0]
        y = plt.Y[i]
        ywin = max(self.real_to_window_y(y), self._MIN_Y)
        ywin = min(ywin, self._MAX_Y)

        if y == 0:
            tmp_str = "0.00"
        elif abs(y) < 0.001:
            tmp_str = f"{y:.3e}"
        elif abs(y) < 0.01:
            tmp_str = f"{y:.3f}"
        elif abs(y) > 9999:
            tmp_str = f"{y:.2E}"
        else:
            tmp_str = f"{y:4.2f}"

        text_width = QFontMetrics(VALUE_FONT).horizontalAdvance(tmp_str)

        yrect = ywin
        wrect = text_width + 10
        xrect = xwin - wrect - 10 + self._MIN_X
        hrect = 18

        yrect = min(yrect, self._value_rect_max_y)

        # self._qp.setPen(QPen(plt.pen.color(), 10, Qt.PenStyle.DashLine, Qt.PenCapStyle.RoundCap))
        # self._qp.drawPoint(QPointF(xwin + self._MIN_X, ywin))

        return ValueRectangle(xrect, yrect, wrect, hrect, tmp_str, plt.pen.color(), QPointF(xwin + self._MIN_X, ywin))
    
    def set_plot_linestyle(self, name: str, linestyle: Qt.PenStyle):
        for plt in self.__plots:
            if not plt.draw_line:
                return
            if plt.name == name and linestyle != plt.pen.style():
                plt.pen.setStyle(linestyle)
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
                        self.window_to_real_x(self.__selected_point.x - self._MIN_X),
                        self.window_to_real_y(self.__selected_point.y + self._OFFSET_Y_UP),
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

        for plt in self.__plots:
            data[plt.name] = dict()
            tmp = data[plt.name]
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
                plots: dict[str] = pickle.load(f)
        except FileNotFoundError:
            return
        
        self.delete_all_plots()
        for name in plots:
            plt = plots[name]
            self.add_plot(plt["x"], plt["y"], linewidth=plt["linewidth"], name=name, color=plt["color"], graph_type=plt["type"])
        if self.__msgBox:
            self.__msgBox.deleteLater()

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

    @property
    def redraw_time(self) -> float:
        return self.__redraw_time

# class __Dashboard:

#     __MAX_VAL_LINES = 3
#     __OFFSET_Y = 20             # смещение по У для размещения шапки
#     __MAX_POINTS = 5000
#     _Y_STOP_RATIO = 20

#     def __init__(self, widget, x, y, h, w, xmin=0, xmax=10, ymin=0, ymax=1,
#                  x_name='Т, с', y_name='', relay_type=False, draw_x=True, convert_to_hhmmss=False, master=None,
#                  animated=False, draw_origin=False, maximum_x_width=-1, initial_timestamp=0, dark=False):

#         self.__x = int(x)
#         self._y = int(y)
#         self.__h = int(h)
#         self.__w = int(w)
#         self.__relay_type = relay_type                  # для отображения релейных сигналов

#         self.__MAXIMUM_X_WIDTH = maximum_x_width        # максимальная видимая ширина графика
#         self.__initial_timestamp = initial_timestamp

#         self.__MIN_X = self.__x
#         self.__MAX_X = self.__x + self.__w
#         self.__MIN_Y = self._y
#         self.__MAX_Y = self._y + self.__h

#         self._plots = list()

#         self.__x_name = x_name
#         self.__y_name = y_name  # имя оси У
#         self.__Y_STOP_COEFF = 1  # увеличение максимума У

#         self.__master = master
#         """Ссылка на график - "мастер". По нему будут рисоваться все вспомогательные
#         вертикальные линии и осуществляться масштабирование. Если не указывать, значит
#         экземпляр сам является мастером"""

#         self.__x_label_width = 100
#         self.__x_met_width = 50
#         self.__y_label_high = 20

#         if self.__master is None:
#             self.slave_restart_flags = list()
#         else:
#             self.__my_index = len(self.__master.slave_restart_flags)
#             self.__master.slave_restart_flags.append(False)

#         self.xstart = xmin
#         self.xstop = xmax
#         self.x_axis_min = xmin
#         self.x_axis_max = xmax
#         self._real_width = self.xstop - self.xstart  # длина оси Х в реальных единицах
#         self.__step_grid_x = self._real_width / 2

#         self._ystart = ymin if not self.__relay_type else 0
#         self._ystop = ymax if not self.__relay_type else 2.1
#         self._y_axis_min = ymin if not self.__relay_type else 0
#         self._y_axis_max = ymax if not self.__relay_type else 2.1
#         self._real_height = self._ystop - self._ystart  # длина оси У в реальных единицах
#         self.__step_grid_y = self._real_height / 2

#         if master is not None:
#             self.VertLines = self.__master.VertLines
#             self.VertLineSelected = self.__master.VertLineSelected
#             self.ValueLines = self.__master.ValueLines
#             self.ValueLineSelected = self.__master.ValueLineSelected
#         else:
#             self.VertLines = list()
#             self.VertLineSelected = [False] * 2
#             self.ValueLines = list()
#             self.ValueLineSelected = [False] * self.__MAX_VAL_LINES
#             self.LastValueLine = 0

#         self.__nearest_value_line = -1      # координата ближайшей к курсору линии-сканера
#         self.__nearest_vert_line = -1       # координата ближайшей к курсору вертикальной линии для масштабирования

#         self._widget = widget              # родительский виджет
#         self.__checkboxes = list()

#         self.__rectX0 = 0
#         self.__rectY0 = 0
#         self.__rectX1 = 0
#         self.__rectY1 = 0

#         self.points = list()

#         # флаги
#         self.__convert_to_hhmmss = convert_to_hhmmss    # конвертировать ли значения Х в ЧЧ:ММ:СС
#         self.__animated = animated if master is None else master.is_animated()
#         self.__x_auto_scale = True
#         self.__y_auto_scale = True
#         self._visible = True
#         self.__draw_major_grid = True
#         self.__draw_minor_grid = False
#         self.__draw_x = draw_x                  # отображать ли подписи оси Х
#         self.__draw_y = True
#         self.__draw_origin = False
#         self.__y_scaled = False
#         self.__right_button_pressed = False
#         self.__left_button_pressed = False
#         self.__scaling_rect_drawing = False
#         self.__redraw_flag = True               # в графике что-то поменялось, нужно перерисовать
#         self.__redraw_flag = False
#         self.__point_added = False
#         self.__paused = False
#         self.__zero_y_fixed = False              # ноль по Х всегда виден
#         self.__zoom_active = False
#         self.__ctrl_pressed = False
#         self.__alt_pressed = False
#         self._dark = dark

#         # ручки
#         self.__pen_grid = QPen(QColor(145, 145, 145), 1)
#         self.__pen_grid.setStyle(Qt.PenStyle.DotLine)
#         self.__pen_grid_minor = QPen(QColor(145, 145, 145), 1)
#         self.__pen_grid_minor.setStyle(Qt.PenStyle.DotLine)
#         self.__origin_pen = QPen(QColor(0, 0, 0), 0.75)

#         self.__minor_step_ratio = 5     # доля от шага основных линий - шаг дополнительных линий

#         self.__msgBox = None

#         self.__mouse_on_slider = False
#         self.__slider_x = -1
#         self.__slider_y = -1
#         self.__slider_w = -1
#         self.__slider_h = -1
#         self.__slider_pressed = False
#         self.__slider_x0 = -1
#         self.__slider_length = 0.2

#         self.__touch_x = 0
#         self.__touch_y = 0

#         self.__initial_x = 0
#         self.__initial_y = 0

#         self._qp = QPainter()

#         self._selectingPointGraph = -1
#         self.__pointsToSelect = 0
#         self.__pointCoords = [0, 0, -1]

#         self.__values_from_slider = [list() for _ in range(self.__MAX_VAL_LINES)]

#         self.__color_generator = ColorGenerator()
#         self.__saveDialog = QFileDialog()
#         self.__action_buffer = ActionBuffer()
#         self.__ext_window = ExtendedWindow(self)

#         # рамка для обработки мыши (невидимая)
#         self.__frame = QtWidgets.QFrame(widget)
#         self.__frame.setGeometry(self.__x, self._y - self.__OFFSET_Y, self.__w, self.__h + self.__OFFSET_Y)
#         self.__frame.setMouseTracking(True)
#         self.__frame.mouseMoveEvent = self.mouse_move_event
#         self.__frame.mousePressEvent = self.mouse_press_event
#         self.__frame.mouseReleaseEvent = self.mouse_release_event
#         self.__frame.mouseDoubleClickEvent = self.mouse_double_click_event
#         self.__frame.keyPressEvent = self.key_press_event
#         self.__frame.keyReleaseEvent = self.key_release_event
#         self.__frame.show()

#         if self.__animated:
#             if self.__master is None:
#                 self.__pause_button = QtWidgets.QPushButton(self.__frame)
#                 self.__pause_button.setGeometry(self.__w - 56, 22, 25, 25)
#                 self.__pause_button.setFont(QFont('consolas', 10))
#                 self.__pause_button.setText("||")
#                 self.__pause_button.clicked.connect(lambda: self.pause(not self.__paused))
#                 self.__pause_button.setToolTip("Пауза / Старт")
#                 self.__pause_button.setStyleSheet(button_style(dark))
#                 self.__pause_button.show()

#                 self.__restart_button = QtWidgets.QPushButton(self.__frame)
#                 self.__restart_button.setGeometry(self.__w - 28, 22, 25, 25)
#                 self.__restart_button.setFont(QFont('arial', 16))
#                 self.__restart_button.setText("\u21e4")
#                 self.__restart_button.clicked.connect(self.restart_animation)
#                 self.__restart_button.setToolTip("Перезапуск анимации")
#                 self.__restart_button.setStyleSheet(button_style(dark))
#                 self.__restart_button.show()

#         x0_b = self.__w - 28
#         step_b = 28
#         y0_b = self.__h - 7

#         self.__button_tmr = time.time()
#         self.__button_flag = False

#         if self.__master is None:
#             self.__clear_button = QtWidgets.QPushButton(self.__frame)
#             self.__clear_button.setGeometry(x0_b - step_b * 5, y0_b, 25, 25)
#             self.__clear_button.setFont(QFont("arial", 12))
#             self.__clear_button.setText("\u2718")
#             self.__clear_button.clicked.connect(self.clear_graph)
#             self.__clear_button.show()
#             self.__clear_button.setToolTip("Очистить график от вспомогательных линий")
#             self.__clear_button.setStyleSheet(button_style(dark))

#             self.__add_vert_button = QtWidgets.QPushButton(self.__frame)
#             self.__add_vert_button.setGeometry(x0_b - step_b * 4, y0_b, 25, 25)
#             self.__add_vert_button.setFont(QFont('arial', 12))
#             self.__add_vert_button.setText("\u2195")
#             self.__add_vert_button.clicked.connect(lambda: self.add_value_line())
#             self.__add_vert_button.show()
#             self.__add_vert_button.setToolTip("Добавить линию-сканер")
#             self.__add_vert_button.setStyleSheet(button_style(dark))

#         self.__fix_button = QtWidgets.QPushButton(self.__frame)
#         if self.__master:
#             self.__fix_button.setGeometry(x0_b - step_b * 3, y0_b, 25, 25)
#         else:
#             self.__fix_button.setGeometry(x0_b - step_b * 6, y0_b, 25, 25)
#         self.__fix_button.setFont(QFont("arial", 12))
#         self.__fix_button.setText("\u2693")
#         self.__fix_button.clicked.connect(lambda: self.fix_y_zero(not self.__zero_y_fixed))
#         self.__fix_button.show()
#         self.__fix_button.setToolTip("Закрепить нуль Y")
#         self.__fix_button.setStyleSheet(button_style(dark))

#         self.__more_button = QtWidgets.QPushButton(self.__frame)
#         self.__more_button.setGeometry(x0_b, y0_b, 25, 25)
#         self.__more_button.setFont(QFont('arial', 11))
#         self.__more_button.setText("\u2699")
#         self.__more_button.clicked.connect(self.__show_extended_window)
#         self.__more_button.show()
#         self.__more_button.setToolTip("Настройки и анализ графиков")
#         self.__more_button.setStyleSheet(button_style(dark))
#         self.__more_button.setEnabled(FULL_VERSION)

#         self.__arrow_button = QtWidgets.QPushButton(self.__frame)
#         self.__arrow_button.setGeometry(x0_b, y0_b, 25, 25)
#         self.__arrow_button.setFont(QFont('arial', 11))
#         self.__arrow_button.setText("🢐")
#         self.__arrow_button.clicked.connect(self.__arrow_btn_proc)
#         self.__arrow_button.show()
#         self.__arrow_button.setStyleSheet(button_style(dark))
#         self.__arrow_button.setEnabled(FULL_VERSION)

#         self.__back_button = QtWidgets.QPushButton(self.__frame)
#         self.__back_button.setGeometry(x0_b - step_b * 2, y0_b, 25, 25)
#         self.__back_button.setFont(QFont("arial", 14))
#         self.__back_button.setText("\u21ba")
#         self.__back_button.clicked.connect(self.cancel_scaling)
#         self.__back_button.show()
#         self.__back_button.setToolTip("Отменить масштабирование")
#         self.__back_button.setStyleSheet(button_style(dark))

#         self.__save_button = QtWidgets.QPushButton(self.__frame)
#         self.__save_button.setGeometry(x0_b - step_b, y0_b, 25, 25)
#         self.__save_button.setFont(QFont('arial', 16))
#         self.__save_button.setText("\u270d")
#         self.__save_button.clicked.connect(self.save_picture)
#         self.__save_button.setToolTip("Сохранить изображение")
#         self.__save_button.setStyleSheet(button_style(dark))
#         self.__save_button.show()
#         self.__save_button.setEnabled(FULL_VERSION)

#         self.__zoom_button = QtWidgets.QPushButton(self.__frame)
#         self.__zoom_button.setGeometry(x0_b - step_b * 3, y0_b, 25, 25)
#         self.__zoom_button.setFont(QFont('arial', 12))
#         self.__zoom_button.setText("🔍")
#         self.__zoom_button.clicked.connect(self.__zoom)
#         self.__zoom_button.setToolTip("Масштабировать")
#         self.__zoom_button.setStyleSheet(button_style(dark))
#         self.__zoom_button.show()
#         self.__zoom_button.setEnabled(True)

#         self.update_step_x()
#         self.update_step_y()

#         set_default_cursor()

#         self.draw_origin(draw_origin)

#     def __arrow_btn_proc(self):
#         self.__button_tmr = time.time()

#     def set_theme(self, dark: bool):
#         self._dark = dark

#     def stop(self):
#         self.__update_checkboxes()
#         self.__ext_window.deleteLater()
#         self.__save_button.deleteLater()
#         self.__back_button.deleteLater()
#         self.__more_button.deleteLater()
#         self.__fix_button.deleteLater()
#         self.__frame.deleteLater()
#         self.__saveDialog.deleteLater()
#         self.__arrow_button.deleteLater()

#     def fix_y_zero(self, fix: bool) -> None:
#         if fix != self.__zero_y_fixed:
#             self.__zero_y_fixed = fix
#             self.calculate_y_parameters()
#             self.update_step_y()
#             self.recalculate_window_coords()
#             self.force_redraw()

#     def get_parent_widget(self):
#         return self.__frame

#     def get_slider_value(self, slider_index, plot_index):
#         if slider_index >= len(self.__values_from_slider):
#             return 0
#         if plot_index >= len(self.__values_from_slider[slider_index]):
#             return 0
#         return self.__values_from_slider[slider_index][plot_index]

#     def set_initial_timestamp(self, ts: int) -> None:
#         self.__initial_timestamp = ts

#     def get_initial_timestamp(self):
#         return self.__initial_timestamp

#     def __zoom(self):
#         if len(self.VertLines) < 2:
#             self.__zoom_active = not self.__zoom_active
#             if self.__zoom_active:
#                 set_crossed_cursor()
#             else:
#                 set_default_cursor()
#             return
#         if self.__animated and not self.__paused:
#             return
#         # увеличиваем график между двуми вертикальными линиями
#         if len(self._plots) == 0:
#             return

#         x0 = min(self.VertLines)
#         x1 = max(self.VertLines)
#         min_len_index = np.argmin(np.array([graph.length for graph in self._plots]))
#         max_x_step = self._plots[min_len_index].X[2] - self._plots[min_len_index].X[1]
#         if x1 - x0 > 4 * max_x_step:
#             self.__action_buffer.add_action(self.xstart, self.xstop, self._ystart, self._ystop)
#             self.set_x_start(x0)
#             self.set_x_stop(x1)
#             self.update_step_x()
#             self.calculate_y_parameters()
#             self.update_step_y()
#             self.recalculate_window_coords()
#             if self.__master is not None:
#                 # передаём данные мастеру
#                 self.__master.set_x_start(x0)
#                 self.__master.set_x_stop(x1)
#                 self.__master.update_step_x()
#                 self.__master.recalculate_window_coords()
#         self.VertLines.clear()
#         self.VertLineSelected[0] = False
#         self.ValueLineSelected[1] = False
#         set_default_cursor()
#         self.force_redraw()

#     def is_paused(self) -> bool:
#         return self.__paused

#     def is_animated(self) -> bool:
#         return self.__animated

#     def needs_redrawing(self) -> bool:
#         return self.__redraw_flag

#     def force_redraw(self) -> None:
#         self.__redraw_flag = True

#     def save_to_json(self, path):
#         buf = dict()
#         for plot in self.plots():
#             buf[plot.name] = dict()
#             buf[plot.name]["x"] = [x for x in plot.X]
#             buf[plot.name]["y"] = plot.Y.tolist()
#             buf[plot.name]["color"] = plot.pen.color().name()
#             buf[plot.name]["linewidth"] = plot.pen.width()

#         with open(path, "w") as f:
#             f.write(json.dumps(buf))

#     def load_from_json(self, path):
#         if self.__animated and not self.__paused:
#             return
#         try:
#             with open(path, 'r') as f:
#                 dash_data = json.load(f)
#         except FileNotFoundError:
#             return

#         if len(self._plots) > 0:
#             self.__msgBox = QtWidgets.QMessageBox()
#             self.__msgBox.setIcon(QtWidgets.QMessageBox.Icon.Question)
#             self.__msgBox.setText("Все текущие графики будут удалены. Продолжить?")
#             self.__msgBox.setWindowTitle("Импорт графиков")
#             self.__msgBox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes |
#                                              QtWidgets.QMessageBox.StandardButton.No)
#             self.__msgBox.button(QtWidgets.QMessageBox.StandardButton.Yes).setText("Да")
#             self.__msgBox.button(QtWidgets.QMessageBox.StandardButton.No).setText("Нет")

#             button = self.__msgBox.exec()
#             if button == QtWidgets.QMessageBox.StandardButton.No:
#                 self.__msgBox.deleteLater()
#                 return
#         self.delete_all_plots()
#         for name, data in dash_data.items():
#             self.add_plot(data["x"], data["y"], thickness=data["linewidth"], name=name, color=data["color"],
#                           graph_type=data["type"])
#         if self.__msgBox:
#             self.__msgBox.deleteLater()

#     def add_point(self, color, shape="round"):
#         d = dict()
#         d["x"] = 0
#         d["y"] = 0
#         d["size"] = 5
#         d["color"] = color
#         if shape == "square":
#             d["shape"] = Qt.PenCapStyle.SquareCap
#         else:
#             d["shape"] = Qt.PenCapStyle.RoundCap
#         d["text"] = ""
#         self.points.append(d)

#     def clear_points(self):
#         self.points = list()

#     def draw_point(self, x, y, size, point_num=0, text=""):
#         self.points[point_num]["x"] = x
#         self.points[point_num]["y"] = y
#         self.points[point_num]["size"] = size
#         self.points[point_num]["text"] = text
#         self.__redraw_flag = True

#     def get_y_axis(self):
#         if len(self._plots) == 0:
#             return list()
#         for plot in self._plots:
#             yield plot.Y

#     def cancel_scaling(self):
#         action = self.__action_buffer.get_last_action()
#         if action is False:
#             return
#         xstart, xstop, ystart, ystop = action
#         self.set_x_start(xstart)
#         self.set_x_stop(xstop)
#         self.set_y_start(ystart)
#         self.set_y_stop(ystop)
#         self.calculate_y_parameters()
#         self.recalculate_window_coords()
#         self.update_step_x()
#         self.update_step_y()
#         self.force_redraw()

#         if self.__master:
#             self.__master.set_x_start(xstart)
#             self.__master.set_x_stop(xstop)
#             self.__master.recalculate_window_coords()
#             self.__master.update_step_x()

#     def save_picture(self):
#         if self.__animated:
#             self.pause(True)
#         self.set_control_elements_visible(False)
#         grab = self._widget.grab(QRect(self.__x - 50, self._y - self.__OFFSET_Y, self.__w + 55,
#                                               self.__h + self.__OFFSET_Y + self.__y_label_high + 1))
#         fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self._widget, "Сохранить картинку", "",
#                                                             "PNG Files (*.png)")

#         grab.save(fileName, 'png')
#         self.set_control_elements_visible(True)
#         os.startfile(fileName)
#         if self.__animated:
#             self.pause(False)

#     def set_enabled(self, enabled: bool) -> None:
#         self.set_control_elements_visible(enabled)

#     def set_visible(self, visible: bool) -> None:
#         self._visible = visible
#         self.set_control_elements_visible(visible)

#     def __update_checkboxes(self):
#         for chb in self.__checkboxes:
#             chb.deleteLater()
#         self.__checkboxes.clear()

#     def __resize_buttons(self):
#         x0_b = self.__w - 28
#         step_b = 28
#         y0_b = self.__h - 7
#         size = 24
#         self.__frame.setGeometry(self.__MIN_X, self.__MIN_Y - self.__OFFSET_Y, self.__w, self.__h + self.__OFFSET_Y)
#         self.__arrow_button.setGeometry(x0_b + size // 2, y0_b, size // 2, size)
#         x0_b = self.__w - size // 2 - step_b - 5
#         self.__more_button.setGeometry(x0_b, y0_b, size, size)
#         self.__save_button.setGeometry(x0_b - step_b, y0_b, size, size)
#         self.__back_button.setGeometry(x0_b - step_b * 2, y0_b, size, size)
#         self.__zoom_button.setGeometry(x0_b - step_b * 3, y0_b, size, size)
#         if self.__master:
#             self.__fix_button.setGeometry(x0_b - step_b * 4, y0_b, size, size)
#         else:
#             self.__fix_button.setGeometry(x0_b - step_b * 6, y0_b, size, size)
#         if self.__master is None:
#             self.__add_vert_button.setGeometry(x0_b - step_b * 4, y0_b, size, size)
#             self.__clear_button.setGeometry(x0_b - step_b * 5, y0_b, size, size)
#             if self.__animated:
#                 self.__pause_button.setGeometry(x0_b - step_b, 22, size, size)
#                 self.__restart_button.setGeometry(x0_b, 22, size, size)

#     def set_geometry(self, x: int, y: int, w: int, h: int) -> None:
#         if x == self.__x and y == self._y and w == self.__w and h == self.__h:
#             return
#         if x >= 0:
#             self.__x = x
#         if y >= 0:
#             self._y = y
#         if w > 30:
#             self.__w = w
#         if h > 10:
#             self.__h = h
#         self.__x = x
#         self.__MAX_X = self.__x + self.__w
#         self.__MIN_X = self.__x
#         self.__MAX_Y = self._y + self.__h
#         self.__MIN_Y = self._y
#         self.recalculate_window_coords()
#         self.__resize_buttons()
#         self.__update_checkboxes()
#         self.update_step_x()
#         self.update_step_y()

#     def begin_point_selection(self, graph_num, n_points=1):
#         if graph_num >= len(self._plots) or self.__animated and not self.__paused:
#             return False
#         self._plots[graph_num].selectedPoint.clear()
#         self._selectingPointGraph = graph_num
#         self.__pointsToSelect = n_points
#         return True

#     def plots(self):
#         for graph in self._plots:
#             yield graph

#     def change_time_format(self, hhmmss=False):
#         self.__convert_to_hhmmss = hhmmss

#     def is_human_time(self):
#         return self.__convert_to_hhmmss

#     def get_x_name(self) -> str:
#         return self.__x_name

#     def get_y_name(self) -> str:
#         return self.__y_name

#     def set_x_name(self, name: str) -> None:
#         self.__x_name = name

#     def set_y_name(self, name: str) -> None:
#         self.__y_name = name

#     def enable_x_ticks(self, enable: bool) -> None:
#         self.__draw_x = enable

#     def enable_y_ticks(self, enable: bool) -> None:
#         self.__draw_y = enable

#     def x_ticks_enabled(self) -> bool:
#         return self.__draw_x

#     def y_ticks_enabled(self) -> bool:
#         return self.__draw_y

#     def get_step_x(self):
#         return self.__step_grid_x

#     def get_step_y(self):
#         return self.__step_grid_y

#     def get_x_start(self):
#         return self.xstart

#     def get_x_stop(self):
#         return self.xstop

#     def get_x_min(self):
#         return self.x_axis_min

#     def get_x_max(self):
#         return self.x_axis_max

#     def get_y_start(self):
#         return self._ystart

#     def get_y_stop(self):
#         return self._ystop

#     def get_y_min(self):
#         return self._y_axis_min

#     def get_y_max(self):
#         return self._y_axis_max

#     def set_step_x(self, step: float):
#         if step <= 0 or self.__x_auto_scale:
#             return
#         self.__step_grid_x = step

#     def set_step_y(self, step: float):
#         if step <= 0 or self.__y_auto_scale:
#             return
#         self.__step_grid_y = step

#     def set_autoscale_x(self, auto: bool):
#         if self.__animated and not self.__paused:
#             return
#         self.__x_auto_scale = auto
#         if auto:
#             self.update_step_x()

#     def set_autoscale_y(self, auto: bool):
#         self.__y_auto_scale = auto
#         if auto:
#             self.update_step_y()

#     def set_x_borders(self, xmin: float, xmax: float):
#         if self.__x_auto_scale or xmin >= xmax or self.__animated and not self.__paused:
#             return
#         self.set_x_start(xmin)
#         self.set_x_stop(xmax)
#         self.recalculate_window_coords()

#     def set_y_borders(self, ymin: float, ymax: float):
#         if self.__y_auto_scale or ymin >= ymax:
#             return
#         self.set_y_start(ymin)
#         self.set_y_stop(ymax)
#         self.recalculate_window_coords()

#     def draw_major_ticks(self, draw: bool):
#         self.__draw_major_grid = draw

#     def draw_minor_ticks(self, draw: bool):
#         self.__draw_minor_grid = draw

#     def major_ticks(self) -> bool:
#         return self.__draw_major_grid

#     def minor_ticks(self) -> bool:
#         return self.__draw_minor_grid

#     def plot_names(self):
#         for graph in self._plots:
#             yield graph.name

#     def is_relay_type(self) -> bool:
#         return self.__relay_type

#     def set_major_grid_style(self, style="dot", width=1.0):
#         match style:
#             case "dot":
#                 self.__pen_grid.setStyle(Qt.PenStyle.DotLine)
#             case "dash":
#                 self.__pen_grid.setStyle(Qt.PenStyle.DashLine)
#             case "solid":
#                 self.__pen_grid.setStyle(Qt.PenStyle.SolidLine)
#         self.__pen_grid.setWidthF(width)

#     def set_minor_grid_style(self, style="dot", width=1.0, step_ratio=5):
#         match style:
#             case "dot":
#                 self.__pen_grid_minor.setStyle(Qt.PenStyle.DotLine)
#             case "dash":
#                 self.__pen_grid_minor.setStyle(Qt.PenStyle.DashLine)
#             case "solid":
#                 self.__pen_grid_minor.setStyle(Qt.PenStyle.SolidLine)
#         self.__pen_grid_minor.setWidthF(width)
#         if step_ratio > 0:
#             self.__minor_step_ratio = step_ratio

#     def y(self):
#         return self._y

#     def x(self):
#         return self.__x

#     def h(self):
#         return self.__h

#     def w(self):
#         return self.__w

#     def draw_origin(self, draw: bool, width=1.0):
#         self.__draw_origin = draw
#         if 0.25 <= width <= 4:
#             self.__origin_pen.setWidthF(width)

#     def is_origin_drawing(self):
#         return self.__draw_origin

#     def set_graph_accurate(self, name: str, accurate: bool):
#         for i, graph_name in enumerate(self.plot_names()):
#             if graph_name == name and self._plots[i].accurate != accurate:
#                 self._plots[i].accurate = accurate
#                 self.recalculate_window_coords()
#                 self.force_redraw()

#     def update_extended_window(self):
#         self.__ext_window.update_plot_info(self._plots)
#         if self.__ext_window.isVisible():
#             self.__ext_window.display_plot_info()

#     def __show_extended_window(self):
#         self.__ext_window.update_plot_info(self._plots)
#         self.__ext_window.display_plot_info()
#         self.__ext_window.show()

#     def set_control_elements_visible(self, visible: bool, hide_checkboxes=True) -> None:
#         """Показ/скрытие управляющих элементов графика:
#         кнопок, чекбоксов. Применятся, если нужно скрыть график,
#         например при использовании tab widget"""
#         if hide_checkboxes:
#             self.__frame.setVisible(visible)
#         self.__fix_button.setVisible(visible and self.__button_flag)
#         self.__more_button.setVisible(visible and self.__button_flag)
#         self.__save_button.setVisible(visible and self.__button_flag)
#         self.__back_button.setVisible(visible and self.__button_flag)
#         self.__zoom_button.setVisible(visible and self.__button_flag)
#         self.__arrow_button.setVisible(visible)
#         if self.__master is not None:
#             return
#         if self.__animated:
#             self.__pause_button.setVisible(visible)
#             self.__restart_button.setVisible(visible)
#         self.__clear_button.setVisible(visible and self.__button_flag)
#         self.__add_vert_button.setVisible(visible and self.__button_flag)

#     def pause(self, pause: bool) -> None:
#         """Обработка нажатия кнопки старт/пауза"""
#         if not self.__animated:
#             return
#         self.__paused = pause
#         if pause:
#             self.__pause_button.setFont(QFont('consolas', 14))
#             self.__pause_button.setText("\u23f5")
#             self.recalculate_window_coords()
#             self.x_axis_min = self.xstart
#             self.x_axis_max = self.xstop
#         else:
#             self.__pause_button.setFont(QFont('consolas', 10))
#             self.__pause_button.setText("||")
#         x_size = 10
#         for dataset in self._plots:
#             x_size = dataset.x_size
#         if self._real_width < x_size:
#             self._real_width = x_size
#             self.update_step_x()

#     def check_graph_visibility(self) -> None:
#         """Проверка видимости графика (стоит ли галочка в соответствующем чекбоксе)
#         Если видимость изменилась, происходит изменение масштаба по оси У, если необходимо,
#         чтобы оставшиеся графики были лучше видны"""
#         for chb, graph in zip(self.__checkboxes, self._plots):
#             if chb.isChecked() is not graph.visible:
#                 graph.visible = chb.isChecked()
#                 self.calculate_x_parameters()
#                 self.calculate_y_parameters()
#                 self.recalculate_window_coords()
#                 self.update_step_x()
#                 self.update_step_y()
#                 self.force_redraw()

#     def recalculate_window_xy(self, plt: Plot, step):
#         plt.Xwin = array("d", [self.real_to_window_x(plt.X[i]) for i in range(plt.index0, plt.index1 + 1, step)])
#         plt.Ywin = array("d", [self.real_to_window_y(plt.Y[i]) for i in range(plt.index0, plt.index1 + 1, step)])

#     def recalculate_window_coords(self) -> None:
#         """Пересчёт массивов оконных координат графиков.
#         Делается при изменении масштаба, передвижениях осей"""

#         if self.__animated and not self.__paused:
#             return

#         for i in range(len(self._plots)):
#             self.find_indexes(i)
#             step = (1 if self._plots[i].accurate
#                     else max(1, int((1 + self._plots[i].index1 - self._plots[i].index0) / self.__MAX_POINTS)))
#             self.recalculate_window_xy(self._plots[i], step)
#         self.__recalculate_slider_coords()

#     def real_to_window_x(self, x: float) -> int:
#         """Перевод реальных координат оси х в оконные"""
#         return c_real_to_window_x(x, self.__MIN_X, self.__w, self._real_width, self.xstart)     # type: ignore

#     def real_to_window_y(self, y: float) -> int:
#         """Перевод реальных координат оси у в оконные"""
#         return c_real_to_window_y(y, self.__MIN_Y, self.__h, self._real_height, self._ystop)    # type: ignore

#     def window_to_real_x(self, x: float) -> float:
#         """Перевод оконных координат оси х в реальные"""
#         return c_window_to_real_x(x, self.__w, self._real_width, self.xstart)   # type: ignore

#     def window_to_real_y(self, y: float) -> float:
#         return c_window_to_real_y(y, self.__h, self._real_height, self._ystop, self.__OFFSET_Y) # type: ignore

#     def update_step_x(self) -> None:
#         """Установка шага оси Х. Происходит с таким расчётом,
#         чтобы на оси было не более 10 меток"""
#         if not self.__x_auto_scale:
#             return
#         try:
#             self.__step_grid_x = 10 ** round(log10(self._real_width)) / 10
#         except ValueError:
#             self.__step_grid_x = 1.0

#         if self._real_width / self.__step_grid_x > 10:
#             n = 3
#             while self._real_width / self.__step_grid_x > 10:
#                 n += 1
#                 self.__step_grid_x *= (2.5 if n % 4 == 0 else 2)
#         else:
#             n = 0
#             while self._real_width / self.__step_grid_x < 10:
#                 n += 1
#                 self.__step_grid_x /= (2.5 if n % 4 == 0 else 2)

#         while self.__step_grid_x / self._real_width * self.__w < self.__x_met_width:
#             self.__step_grid_x *= (2.5 if n % 4 == 0 else 2)
#             n += 1

#         if self.__step_grid_x / self._real_width * self.__w > 150:
#             self.__step_grid_x /= (2.5 if n % 4 == 0 else 2)

#         if self.__step_grid_x == 0:
#             self.__step_grid_x = self._real_width / 1

#         # if

#     def update_step_y(self) -> None:
#         """См. ось Х"""
#         if self.__relay_type:
#             self.__step_grid_y = 1
#             return
#         if not self.__y_auto_scale:
#             return

#         if self._ystart == self._ystop:
#             self._ystart -= 0.5
#             self._ystop += 0.5
#             self._real_height = 1

#         self.__step_grid_y = 10 ** round(log10(self._real_height)) / 10
#         n = 0

#         if self._real_height / self.__step_grid_y >= 10:
#             n = 3
#             while self._real_height / self.__step_grid_y >= 10:
#                 n += 1
#                 self.__step_grid_y *= (2.5 if n % 4 == 0 else 2)

#         elif self._real_height / self.__step_grid_y < 8:
#             while self._real_height / self.__step_grid_y <= 10:
#                 n += 1
#                 self.__step_grid_y /= (2.5 if n % 4 == 0 else 2)

#         while self.__step_grid_y / self._real_height * self.__h < 25:  # высота не менее 30 пикселей
#             n += 1
#             self.__step_grid_y *= (2.5 if n % 4 == 0 else 2)

#         if self.__step_grid_y / self._real_height * self.__h > 100:
#             self.__step_grid_y /= (2.5 if n % 4 == 0 else 2)

#     def set_dataset_size(self, name, size):
#         for plt in self._plots:
#             if plt.name == name:
#                 plt.set_x_size(size)
#                 self.set_x_start(0)
#                 self.set_x_stop(size)
#                 self.update_step_x()
#                 return

#     def add_dataset(self, name: str, x_size=10, thickness=2, linestyle='solid', color='any',
#                     graph_type='ordinary') -> None:
#         """Добавление нового графика на анимированные оси."""
#         if not self.__animated:
#             return
#         if name == "" or name in self.plot_names():
#             return
#         if color == 'any':
#             color = self.__color_generator.get_color()
#         else:
#             color = color
#         pen = QPen(QColor(color), thickness)
#         if linestyle == 'dash':
#             pen.setStyle(Qt.PenStyle.DashLine)
#         elif linestyle == 'dot':
#             pen.setStyle(Qt.PenStyle.DotLine)
#         elif linestyle == 'dash-dot':
#             pen.setStyle(Qt.PenStyle.DashDotLine)
#         elif linestyle == 'dash-dot-dot':
#             pen.setStyle(Qt.PenStyle.DashDotDotLine)
#         else:
#             pen.setStyle(Qt.PenStyle.SolidLine)
#         pen.setCapStyle(Qt.PenCapStyle.RoundCap)
#         if graph_type == 'approx' or graph_type == 'derivative':
#             x_size = self._plots[0].width
#         self._plots.append(Plot([], [], pen, name=name, x_size=x_size,
#                                 graph_type=graph_type, animated=True))

#         if graph_type == 'ordinary':
#             self._real_width = x_size
#             self.xstop = x_size
#             self.x_axis_max = x_size
#             self.update_step_x()
#         self.__update_checkboxes()

#         for i in range(self.__MAX_VAL_LINES):
#             self.__values_from_slider[i].append(0)

#     def add_point_to_dataset(self, name: str, x: float, y: float) -> None:
#         """Добавление новой точки к анимированному графику"""
#         if name not in self.plot_names():
#             return
#         plt = self._plots[0]
#         for plot in self._plots:
#             if plot.name == name:
#                 plt = plot
#                 break
#         if self.__animated and not self.__paused:
#             self.force_redraw()
#             x, y = plt.add_element(x, y)

#             if self.__master is None:
#                 if x > self.xstop:
#                     self.xstop = x
#                     self.x_axis_max = x
#                     self.xstart = self.xstop - self._real_width
#                     self.x_axis_min = self.xstart
#             else:
#                 self.xstart = self.__master.xstart
#                 self.xstop = self.__master.xstop
#                 self.x_axis_min = self.__master.xstart
#                 self.x_axis_max = self.xstop

#     def restart_animation(self) -> None:
#         """Обработка нажатия кнопки Заново"""
#         x_size = 10
#         keys_to_pop = []
#         for plt in self._plots:
#             keys_to_pop.append(plt.name)

#         for key in keys_to_pop:
#             for i in range(len(self._plots)):
#                 if self._plots[i].name == key:
#                     self._plots.pop(i)
#                     break

#         for plt in self._plots:
#             x_size = plt.x_size
#             plt.remove_all()
#         self.xstart = 0
#         self._real_width = x_size
#         self.xstop = self.xstart + self._real_width
#         self.x_axis_min = 0
#         self.x_axis_max = self._real_width
#         self.update_step_x()

#         if self.__master is None:
#             for j in range(len(self.slave_restart_flags)):
#                 self.slave_restart_flags[j] = True
#         else:
#             self.__master.slave_restart_flags[self.__my_index] = False
#         self.__update_checkboxes()

#     def clear_graph(self) -> None:
#         """Очистка осей от всех дополнительных линий"""
#         self.ValueLines.clear()
#         self.VertLines.clear()
#         self.__deselect_all()
#         self.force_redraw()
#         if self.__animated:
#             y_maximum = 1
#             y_minimum = 0
#             for plt in self._plots:
#                 for y in plt.Y:
#                     if y > y_maximum * self.__Y_STOP_COEFF:
#                         y_maximum = y
#                     if y < y_minimum:
#                         y_minimum = y
#             self.set_y_stop(self.__Y_STOP_COEFF * y_maximum)
#             self._y_axis_max = y_maximum
#         set_default_cursor()

#     def add_hist(self, data, categories=None, bins=0, name="", color="any"):
#         if self.__animated:
#             return -1

#         if bins <= 0:
#             bins = 10

#         x0 = min(data)
#         xk = max(data)

#         y = [0] * bins
#         n_bin = 0
#         data_sorted = np.sort(data)
#         intervals = [x0 + (xk - x0) / bins * i for i in range(bins + 1)]
#         x = [(intervals[i + 1] + intervals[i]) / 2 for i in range(bins)]

#         for val in data_sorted:
#             while val > intervals[n_bin + 1] and n_bin < bins - 1:
#                 n_bin += 1
#             try:
#                 y[n_bin] += 1
#             except IndexError:
#                 y[n_bin - 1] += 1

#         if color == 'any':
#             color = self.__color_generator.get_color()
#             heatmap = False
#         elif color == 'heatmap':
#             heatmap = True
#             color = self.__color_generator.get_color()
#         else:
#             color = color
#             heatmap = False

#         pen = QPen(QColor(color), 2)
#         pen.setStyle(Qt.PenStyle.SolidLine)
#         if name == '':
#             name = f"Гистограмма {len(self._plots) + 1}"

#         self._plots.append(Plot(x, y, pen, name=name, graph_type='ordinary', accurate=True, bar=True,
#                                 heatmap=heatmap))

#         max_x = xk
#         min_x = x0
#         if min_x < self.x_axis_min or len(self._plots) == 1:
#             self.x_axis_min = min_x
#         self.set_x_start(self.x_axis_min)

#         if max_x >= self.x_axis_max or len(self._plots) == 1:
#             self.x_axis_max = max_x
#         self.set_x_stop(self.x_axis_max)
#         self.calculate_y_parameters()
#         self.recalculate_window_coords()
#         self.update_step_y()
#         self.update_step_x()

#         self.__ext_window.update_plot_info(self._plots)
#         self.__update_checkboxes()
#         self.force_redraw()

#         for i in range(self.__MAX_VAL_LINES):
#             self.__values_from_slider[i].append(0)

#         return 0

#     def add_plot(self, x_arr, y_arr=None, thickness=2, linestyle='solid', name='',
#                  color='any', graph_type='ordinary', accurate=False, initial_ts=0) -> int:
#         """Добавить статичный график для отображения"""

#         if not hasattr(x_arr, "__iter__"):
#             return False
#         if y_arr is None:
#             y_arr = x_arr
#             x_arr = list(range(len(y_arr)))
#         elif not hasattr(y_arr, "__iter__"):
#             return False
#         if len(x_arr) != len(y_arr) or len(x_arr) < 2:
#             return False

#         # все значения графика в одной точке
#         if max(x_arr) - min(x_arr) == 0 and max(y_arr) - min(y_arr) == 0:
#             return False

#         if color == 'any':
#             color = self.__color_generator.get_color()
#         else:
#             color = color

#         self.__initial_timestamp = initial_ts

#         pen = QPen(QColor(color), thickness)
#         if linestyle == 'dash':
#             pen.setStyle(Qt.PenStyle.DashLine)
#         elif linestyle == 'dot':
#             pen.setStyle(Qt.PenStyle.DotLine)
#         elif linestyle == 'dash-dot':
#             pen.setStyle(Qt.PenStyle.DashDotLine)
#         elif linestyle == 'dash-dot-dot':
#             pen.setStyle(Qt.PenStyle.DashDotDotLine)
#         else:
#             pen.setStyle(Qt.PenStyle.SolidLine)
#         x_tmp = list(x_arr)
#         y_tmp = list(y_arr)
#         if name == '':
#             name = f"График {len(self._plots) + 1}"
#         self._plots.append(Plot(x_tmp, y_tmp, pen, name=name, graph_type=graph_type, accurate=accurate, bar=False))
#         if graph_type == 'ordinary':
#             max_x = max(x_tmp)
#             min_x = min(x_tmp)
#             if min_x < self.x_axis_min or len(self._plots) == 1:
#                 self.x_axis_min = min_x
#             self.set_x_start(self.x_axis_min)

#             if max_x >= self.x_axis_max or len(self._plots) == 1:
#                 self.x_axis_max = max_x
#             self.set_x_stop(self.x_axis_max)

#         self.calculate_y_parameters()
#         self.recalculate_window_coords()
#         self.update_step_y()
#         self.update_step_x()

#         self.__ext_window.update_plot_info(self._plots)
#         self.__update_checkboxes()

#         for i in range(self.__MAX_VAL_LINES):
#             self.__values_from_slider[i].append(0)

#         self.force_redraw()
#         return True

#     def calculate_y_parameters(self) -> None:
#         """Пересчёт параметров оси У. Нужен при вертикальном масштабировании
#         или если график оказывается выше текущей верхней границы"""

#         if len(self._plots) > 0:
#             self._y_axis_max = max([plt.max(1) for plt in self._plots])
#             self._y_axis_min = min([plt.min(1) for plt in self._plots])
#         else:
#             self._y_axis_max = 1
#             self._y_axis_min = 0
#         if not self.__y_scaled:
#             self.set_y_start(0)
#             self.set_y_stop(1)
#         max_y_list = []
#         min_y_list = []
#         for i, graph in enumerate(self._plots):
#             if not graph.visible or graph.length == 0:
#                 continue
#             self.find_indexes(i)
#             max_y_list.append(graph.max(1))
#             min_y_list.append(graph.min(1))
#         if len(max_y_list) == 0:
#             return

#         max_y = max(max_y_list)
#         min_y = min(min_y_list)
#         if max_y == min_y:
#             max_y += abs(max_y * 0.1)
#             min_y -= abs(min_y * 0.1)

#         if self.__zero_y_fixed:
#             if min_y > 0:
#                 min_y = 0
#             if max_y < 0:
#                 max_y = 0
#         self.__Y_STOP_COEFF = (max_y - min_y) / self._Y_STOP_RATIO

#         if not self.__relay_type:
#             if not self.__y_scaled:
#                 ystart = min_y if self.__zero_y_fixed and min_y == 0 else min_y - self.__Y_STOP_COEFF
#                 ystop = max_y if self.__zero_y_fixed and max_y == 0 else max_y + self.__Y_STOP_COEFF
#                 self.set_y_start(ystart)
#                 self.set_y_stop(ystop)
#         else:
#             self.set_y_start(0)
#             self.set_y_stop(max_y * 1.01 if max_y != 0 else 1)
#             self._y_axis_min = 0
#             self._y_axis_max = max_y
#             self.__step_grid_y = 1
#         if self._y_axis_max == self._y_axis_min:
#             self._y_axis_max += 10

#     def calculate_x_parameters(self):
#         if self.__animated and not self.__paused:
#             return
#         if len(self._plots) > 0:
#             minimums = [plt.min(0) for plt in self._plots if plt.visible]
#             maximums = [plt.max(0) for plt in self._plots if plt.visible]
#             if len(minimums) > 0:
#                 min_x = min(minimums)
#                 max_x = max(maximums)
#             else:
#                 min_x = self.xstart
#                 max_x = self.xstop
#             if min_x == max_x:
#                 max_x += 10
#         else:
#             min_x = 0
#             max_x = 10
#         self.x_axis_min = min_x
#         self.x_axis_max = max_x
#         if self.xstart < self.x_axis_min:
#             self.set_x_start(self.x_axis_min)
#         if self.xstop > self.x_axis_max:
#             self.set_x_stop(self.x_axis_max)

#     def delete_plot(self, name):
#         index = -1
#         for i, plot_name in enumerate(self.plot_names()):
#             if plot_name == name:
#                 index = i
#         if index == -1:
#             return

#         self._plots.pop(index)
#         self.__update_checkboxes()

#         self.calculate_x_parameters()
#         self.calculate_y_parameters()
#         self.update_step_y()
#         self.recalculate_window_coords()
#         self.__color_generator.one_color_back()

#         self.__ext_window.update_plot_info(self._plots)
#         self.__ext_window.display_plot_info()

#         for i in range(self.__MAX_VAL_LINES):
#             self.__values_from_slider[i].pop(-1)
#         self.force_redraw()

#     def delete_all_plots(self) -> None:
#         """Удалить все графики"""
#         self.xstart = 0
#         self.xstop = 10
#         self._ystart = 0
#         self._ystop = 1

#         self.x_axis_min = 0
#         self.x_axis_max = 10
#         self._y_axis_min = 0
#         self._y_axis_max = 1
#         self._real_width = self.xstop - self.xstart
#         self._real_height = self._ystop - self._ystart
#         self._plots.clear()
#         self.force_redraw()
#         self.update_step_x()
#         self.update_step_y()
#         self.__update_checkboxes()
#         self.__color_generator.reset()
#         for i in range(self.__MAX_VAL_LINES):
#             self.__values_from_slider[i].clear()

#     def delete_animation_dataset(self, name):
#         self.delete_plot(name)

#     def set_x_stop(self, xmax: float) -> None:
#         """Установка максимального отображаемого значения Х"""
#         if self.__MAXIMUM_X_WIDTH == -1 or xmax - self.xstart <= self.__MAXIMUM_X_WIDTH:
#             self.xstop = xmax
#             self._real_width = self.xstop - self.xstart
#         else:
#             self.xstop = self.xstart + self.__MAXIMUM_X_WIDTH
#             self._real_width = self.__MAXIMUM_X_WIDTH

#     def set_x_start(self, xmin: float) -> None:
#         """Установка минимального отображаемого значения Х"""
#         self.xstart = xmin
#         self._real_width = self.xstop - self.xstart

#     def set_y_stop(self, ymax: float) -> None:
#         """Установка максимального отображаемого значения У"""
#         self._ystop = ymax
#         self._real_height = self._ystop - self._ystart

#     def set_y_start(self, ymin: float) -> None:
#         """Установка минимального отображаемого значения У"""
#         self._ystart = ymin
#         self._real_height = self._ystop - self._ystart

#     def reset_y_axle(self) -> None:
#         self._ystart = self._y_axis_min
#         self._ystop = self._y_axis_max
#         self._real_height = abs(self._ystop - self._ystart)

#     def __recalculate_slider_coords(self):
#         if self.__slider_pressed:
#             return

#         x0 = self.__x + int((1 - self.__slider_length - 0.01) * self.__w)

#         x_axis_length = self.x_axis_max - self.x_axis_min
#         if x_axis_length == 0:
#             return
#         x01 = x0 + int(self.__w * self.__slider_length * (self.xstart - self.x_axis_min) / x_axis_length)
#         x11 = x0 + int(self.__w * self.__slider_length * (self.xstop - self.x_axis_min) / x_axis_length)
#         self.__slider_x = x01
#         self.__slider_y = self._y + 10
#         self.__slider_w = max(4, x11 - x01)
#         self.__slider_h = 12

#     def __draw_x_slider(self) -> None:
#         """Рисование указателя положения окна просмотра относительно
#         всей имеющейся оси Х. Только для статичных графиков"""
#         if len(self._plots) == 0 or self.__master:  # если на графике ничего нет, не рисуем
#             return
#         if self.xstart == self.x_axis_min and self.xstop == self.x_axis_max:
#             return

#         self._qp.setPen(QPen(QColor(100, 100, 100, 0), 1))
#         self._qp.setBrush(QColor(230, 230, 230, 100))

#         x0 = self.__x + round((1 - self.__slider_length - 0.01) * self.__w)
#         x1 = x0 + round(self.__w * self.__slider_length)
#         R = 5
#         self._qp.drawRoundedRect(x0, self.__slider_y - self.__slider_h // 2, x1 - x0, self.__slider_h, R, R)

#         if self.__slider_pressed:
#             color = QColor(112, 146, 190, 150)
#         elif self.__mouse_on_slider:
#             color = QColor(190, 190, 190, 150)
#         else:
#             color = QColor(150, 150, 150, 150)

#         self._qp.setBrush(color)
#         self._qp.drawRoundedRect(self.__slider_x, self.__slider_y - self.__slider_h // 2, self.__slider_w,
#                                  self.__slider_h, R, R)

#     def _draw_axes(self) -> None:
#         """Отрисовка осей и сетки"""
#         if self._dark:
#             self._qp.setPen(QColor(40, 47, 60))
#             self._qp.setBrush(QColor(40, 47, 60))
#         else:
#             self._qp.setPen(QColor(255, 255, 255))
#             self._qp.setBrush(QColor(255, 255, 255))
#         self._qp.drawRect(self.__x, self._y, self.__w, self.__h)  # белое поле графика

#         font = QFont('bahnschrift', 11)
#         font.setBold(True)
#         if self._dark:
#             self._qp.setPen(QPen(QColor(230, 230, 230)))
#             font.setBold(False)
#         else:
#             self._qp.setPen(QPen(QColor(0, 0, 0)))
#         self._qp.setFont(font)
#         self._qp.drawText(self.__x - 110, self._y, 100, self.__y_label_high,
#                           Qt.AlignmentFlag.AlignRight, self.__y_name)  # имя оси У

#         self.__x_label_width = QFontMetrics(font).horizontalAdvance(self.__x_name)
#         self.__y_label_high = QFontMetrics(font).height()

#         if self.__draw_x:
#             self._qp.drawText(self.__MAX_X - 500, self.__MAX_Y + 1, 500, 20,
#                               Qt.AlignmentFlag.AlignRight, self.__x_name)  # имя оси Х
#         font.setBold(False)
#         self._qp.setFont(font)
#         # оси координат по необходимости
#         if self.__draw_origin:
#             self._qp.setPen(self.__origin_pen)
#             x = self.real_to_window_x(0)
#             y = self.real_to_window_y(0)
#             if self.__MIN_Y <= y <= self.__MAX_Y:
#                 self._qp.drawLine(QLineF(self.__MIN_X, y, self.__MAX_X, y))
#             if self.__MIN_X <= x <= self.__MAX_X:
#                 self._qp.drawLine(QLineF(x, self.__MIN_Y, x, self.__MAX_Y))

#         if self.__master is not None and self.__x_auto_scale:
#             self.__step_grid_x = self.__master.get_step_x()

#         # формируем метки по оси Х
#         x0 = round_custom(self.xstart, self.__step_grid_x)
#         xk = min(self.x_axis_max, self.xstop)
#         x_met = np.arange(x0, xk, self.__step_grid_x)
#         tmp_x_met = self.__x_met_width
#         self.__x_met_width = 0
#         for x in x_met:
#             x_w = self.real_to_window_x(x)  # оконная координата метки
#             if self.__MIN_X < x_w < self.__MAX_X:
#                 if not (x == 0 and self.__draw_origin) and self.__draw_major_grid:
#                     self._qp.setPen(self.__pen_grid)
#                     self._qp.drawLine(QLineF(x_w, self.__MAX_Y, x_w, self.__MIN_Y))  # линии сетки

#                 if self.__draw_x:
#                     # подписи осей
#                     if self._dark:
#                         self._qp.setPen(QPen(QColor(210, 210, 210)))
#                     else:
#                         self._qp.setPen(QPen(QColor(0, 0, 0)))
#                     if self.__convert_to_hhmmss and self.x_axis_min >= 0:
#                         tmp_str = convert_timestamp_to_human_time(x + self.__initial_timestamp, self.__step_grid_x < 1)
#                     else:
#                         step_div = self.__step_grid_x
#                         if step_div < 0.001:
#                             tmp_str = f"{x:.3e}"
#                         elif step_div < 0.01:
#                             tmp_str = f"{x:.4f}"
#                             if tmp_str[-1] == '0':
#                                 tmp_str = tmp_str[:-1]
#                         elif step_div < 2.5:
#                             tmp_str = f"{x:.2f}"
#                         elif step_div < 25:
#                             tmp_str = f"{x:.1f}"
#                         elif step_div > 9999:
#                             tmp_str = f"{x:.2E}"
#                         else:
#                             tmp_str = f"{round(x)}"

#                     tmp_str_width = QFontMetrics(font).horizontalAdvance(tmp_str)
#                     if tmp_str_width > self.__x_met_width:
#                         self.__x_met_width = tmp_str_width

#                     if self.__MIN_X + 30 < x_w < self.__MAX_X - self.__x_label_width - tmp_str_width:
#                         self._qp.drawText(QRectF(x_w - 40, self.__MAX_Y + 1, 80, 20),
#                                           Qt.AlignmentFlag.AlignCenter, tmp_str)

#             if self.__draw_minor_grid:  # побочная сетка
#                 x_min = np.arange(x + self.__step_grid_x / self.__minor_step_ratio, x + self.__step_grid_x,
#                                   self.__step_grid_x / self.__minor_step_ratio)
#                 x_minor = [self.real_to_window_x(x_m) for x_m in x_min]
#                 for x_m in x_minor:
#                     if self.__MIN_X < x_m < self.__MAX_X:
#                         self._qp.setPen(self.__pen_grid_minor)
#                         self._qp.drawLine(QLineF(x_m, self.__MAX_Y, x_m, self.__MIN_Y))
#         if tmp_x_met != self.__x_met_width:
#             self.update_step_x()

#         y_met_upper = np.arange(0, self._ystop + 1e-10, self.__step_grid_y)
#         y_met_lower = np.arange(-self.__step_grid_y, self._ystart - self.__step_grid_y, -self.__step_grid_y)
#         y_met = np.concatenate([y_met_lower, y_met_upper])

#         for y in y_met:
#             y_w = self.real_to_window_y(y)

#             if self.__MIN_Y < y_w < self.__MAX_Y:
#                 if not (y == 0 and self.__draw_origin) and self.__draw_major_grid:
#                     self._qp.setPen(self.__pen_grid)
#                     self._qp.drawLine(QLineF(self.__MIN_X, y_w, self.__MAX_X, y_w))
#                 if self.__draw_y:
#                     if self._dark:
#                         self._qp.setPen(QPen(QColor(210, 210, 210)))
#                     else:
#                         self._qp.setPen(QPen(QColor(0, 0, 0)))

#                     if self.__relay_type:
#                         tmp_str = f"{int(y)}"
#                     else:
#                         if self.__step_grid_y < 0.001:
#                             tmp_str = f"{y:.3e}"
#                         elif self.__step_grid_y < 0.01:
#                             tmp_str = f"{y:.3f}"
#                         elif self.__step_grid_y < 5:
#                             tmp_str = f"{y:.2f}"
#                         elif self.__step_grid_y > 9999:
#                             tmp_str = f"{y:.2E}"
#                         else:
#                             tmp_str = f"{int(y)}"

#                     if y_w > self._y + self.__y_label_high + 15:
#                         self._qp.drawText(QRectF(self.__MIN_X - 110, y_w - 10, 100, 20),
#                                           Qt.AlignmentFlag.AlignRight, tmp_str)

#             if self.__draw_minor_grid:  # побочная сетка
#                 y_min = np.arange(y + self.__step_grid_y / self.__minor_step_ratio, y + self.__step_grid_y,
#                                   self.__step_grid_y / self.__minor_step_ratio)
#                 y_minor = [self.real_to_window_y(y_m) for y_m in y_min]
#                 for y_m in y_minor:
#                     if self.__MIN_Y <= y_m <= self.__MAX_Y:
#                         self._qp.setPen(self.__pen_grid_minor)
#                         self._qp.drawLine(QLineF(self.__MIN_X, y_m, self.__MAX_X, y_m))

#     def __find_point_coords(self, x_win):
#         x_real = self.window_to_real_x(x_win)
#         i = self._selectingPointGraph
#         _, indx = self._plots[i].get_nearest(x_real)[0]
#         self.__pointCoords[0] = self.real_to_window_x(self._plots[i].X[indx])
#         self.__pointCoords[1] = self.real_to_window_y(self._plots[i].Y[indx])
#         self.__pointCoords[2] = indx

#     def __draw_point_on_graph(self):
#         if self._selectingPointGraph < 0:
#             return

#         self._qp.setPen(QColor(0, 0, 0, alpha=255))
#         # вертикальная линия у текущей выбираемой точки
#         self._qp.drawLine(QLineF(self.__pointCoords[0], self.__MIN_Y, self.__pointCoords[0], self.__MAX_Y))

#         # сама точка
#         self._qp.setPen(QColor(0, 0, 0, alpha=0))
#         self._qp.setBrush(QColor(103, 103, 52, alpha=200))
#         self._qp.drawEllipse(QPointF(self.__pointCoords[0], self.__pointCoords[1]), 5, 5)

#         # возня с прямоугольником со значением
#         font = QFont("consolas", 10)
#         font.setBold(True)
#         self._qp.setFont(font)
#         qm = QFontMetrics(font)
#         tmp_str = f"{self.window_to_real_x(self.__pointCoords[0] - self.__x):.2f}; " \
#                   f"{self.window_to_real_y(self.__pointCoords[1] - self._y + self.__OFFSET_Y):.2f}"  # координаты
#         text_width = qm.size(0, tmp_str).width()

#         self._qp.setBrush(QColor(0, 162, 232, alpha=255))
#         rectX = self.__pointCoords[0] + 10
#         if rectX < self.__MIN_X:
#             rectX = self.__pointCoords[0] + 10 + self.__MIN_X
#         rectW = text_width + 10
#         rectH = 17
#         rectY = self.__pointCoords[1]

#         tmp_str1 = f"Осталось выбрать: {self.__pointsToSelect}"
#         text_width1 = qm.size(0, tmp_str1).width()
#         rectX1 = rectX - 30 - text_width1
#         rectW1 = text_width1 + 10
#         rectH1 = 17

#         if rectX > self.__MAX_X - 200 and rectY >= self.__MAX_Y - 60:
#             rectY -= 50
#         if rectX > self.__MAX_X - rectW - 10:
#             rectX -= rectW + 20
#         rectY1 = rectY - 30
#         self._qp.drawRoundedRect(QRectF(rectX, rectY, rectW, rectH), 5, 5)
#         self._qp.setPen(QColor(255, 255, 255, alpha=255))
#         self._qp.drawText(QRectF(rectX, rectY, rectW, rectH), Qt.AlignmentFlag.AlignCenter, tmp_str)
#         self._qp.setBrush(QColor(29, 69, 154, alpha=255))
#         self._qp.setPen(QColor(0, 0, 0, alpha=0))

#         if rectX1 <= self.__MIN_X:
#             rectX1 += rectW1 + 10

#         self._qp.drawRoundedRect(QRectF(rectX1, rectY1, rectW1, rectH1), 5, 5)
#         self._qp.setPen(QColor(255, 255, 255, alpha=255))
#         self._qp.drawText(QRectF(rectX1, rectY1, rectW1, rectH1), Qt.AlignmentFlag.AlignCenter, tmp_str1)

#         point = self._plots[self._selectingPointGraph].selectedPoint
#         graph_x = self._plots[self._selectingPointGraph].X
#         graph_y = self._plots[self._selectingPointGraph].Y

#         # если первая точка уже выбрана, нарисуем линию на её месте
#         if len(point) == 1:
#             x = self.real_to_window_x(point[0][0])
#             self._qp.setPen(QColor(0, 0, 0, alpha=255))
#             self._qp.drawLine(QLineF(x, self.__MIN_Y, x, self.__MAX_Y))
#             self._qp.setPen(QColor(0, 0, 0, alpha=0))
#             self._qp.setBrush(QColor(103, 103, 52, alpha=40))

#             # нарисуем закрашенную область под графиком
#             i0 = min(point[0][2], self.__pointCoords[2])
#             ik = max(point[0][2], self.__pointCoords[2]) + 1

#             x_p = self.real_to_window_x(graph_x[self.__pointCoords[2]])
#             points_list = [QPointF(max(x, x_p), min(self.real_to_window_y(0), self.__MAX_Y + 1)) if i == i0 - 2
#                            else QPointF(min(x, x_p), min(self.real_to_window_y(0),
#                                                                self.__MAX_Y + 1)) if i == i0 - 1
#                            else QPointF(max(x, x_p), min(self.real_to_window_y(0), self.__MAX_Y + 1)) if i == ik
#                            else QPointF(self.real_to_window_x(graph_x[i]), self.real_to_window_y(graph_y[i]))
#                            for i in range(i0 - 2, ik + 1)]
#             self._qp.drawPolygon(QPolygonF(points_list))

#     def move_slider(self, mouse_x):
#         self.__slider_x += (mouse_x - self.__slider_x0)

#         x0 = self.__x + int((1 - self.__slider_length - 0.01) * self.__w)
#         x1 = x0 + int(self.__w * self.__slider_length)

#         if self.__slider_x < x0:
#             self.__slider_x = x0
#         if self.__slider_x + self.__slider_w > x1:
#             self.__slider_x = x1 - self.__slider_w

#         self.__slider_x0 = mouse_x

#         x_len = self.x_axis_max - self.x_axis_min
#         x_start = x_len * (self.__slider_x - x0) / (self.__w * self.__slider_length) + self.x_axis_min
#         x_stop = x_len * (self.__slider_x - x0 + self.__slider_w) / (self.__w * self.__slider_length) + self.x_axis_min

#         self.set_x_start(x_start)
#         self.set_x_stop(x_stop)
#         self.recalculate_window_coords()

#     def kick_master(self):
#         if self.__master:
#             # пинаем мастера
#             self.__master.xstart = self.xstart
#             self.__master.xstop = self.xstart + self._real_width
#             self.__master.recalculate_window_coords()

#     def mouse_move_event(self, event: QMouseEvent):
#         set_default_cursor()
#         if event.pos().y() < self.__OFFSET_Y and not self.__zoom_active:
#             set_default_cursor()
#             self.__slider_pressed = False
#             return

#         # обработка слайдера
#         if self.__master is None:
#             if self.xstart != self.x_axis_min or self.xstop != self.x_axis_max:
#                 tmp_y = self.__slider_y - self._y
#                 tmp = (self.__slider_x < (event.pos().x() + self.__x) < self.__slider_x + self.__slider_w and
#                        tmp_y - self.__slider_h / 2 < event.pos().y() - self.__OFFSET_Y < tmp_y + self.__slider_h / 2)
#                 if tmp != self.__mouse_on_slider:
#                     self.force_redraw()
#                     self.__mouse_on_slider = tmp
#                 if self.__mouse_on_slider:
#                     self.__deselect_all()

#                 if self.__slider_pressed:
#                     self.move_slider(event.pos().x() + self.__x)
#                     self.force_redraw()

#         if self._selectingPointGraph >= 0:
#             self.__find_point_coords(event.pos().x())
#             self.force_redraw()

#         if (not self.__left_button_pressed and not self.__slider_pressed and
#                 not self.__mouse_on_slider and not self.__zoom_active):
#             for i, val_line in enumerate(self.ValueLines):
#                 val_line = self.__get_value_line_coord(val_line)
#                 old_val = self.ValueLineSelected[i]
#                 self.ValueLineSelected[i] = abs(event.pos().x() - val_line) < 15
#                 if old_val != self.ValueLineSelected[i]:
#                     self.force_redraw()

#             if any(self.ValueLineSelected):
#                 self.VertLineSelected[0] = False
#                 self.VertLineSelected[1] = False
#             else:
#                 for i, vert_line in enumerate(self.VertLines):
#                     coord = self.real_to_window_x(vert_line)
#                     old_val = self.VertLineSelected[i]
#                     self.VertLineSelected[i] = abs(event.pos().x() + self.__MIN_X - coord) < 15
#                     if old_val != self.VertLineSelected[i]:
#                         self.force_redraw()

#         if self.__frame.underMouse() and self.__right_button_pressed:
#             # при нажатой ПКМ двигаем график
#             if self.__animated and not self.__paused:
#                 return
#             set_grab_cursor()
#             tmpX = self.window_to_real_x(self.__initial_x) - self.window_to_real_x(event.pos().x())
#             self.xstart = max(min(tmpX, self.x_axis_max - self._real_width), self.x_axis_min)
#             self.xstop = self.xstart + self._real_width

#             if not self.__relay_type:
#                 tmpY = self.__initial_y - self.window_to_real_y(event.pos().y())
#                 self._ystart += tmpY
#                 min_possible_y = (0 if self.__zero_y_fixed and self._y_axis_min >= 0
#                                   else self._y_axis_min - self.__Y_STOP_COEFF)
#                 max_possible_y = self._y_axis_max + (0 if (self.__zero_y_fixed and self._y_axis_max <= 0)
#                                                       else self.__Y_STOP_COEFF)
#                 if self._ystart < min_possible_y:
#                     self._ystart = min_possible_y
#                 if self._ystart + self._real_height > max_possible_y:
#                     self._ystart = max_possible_y - self._real_height
#                 self._ystop = self._ystart + self._real_height
#             self.recalculate_window_coords()
#             self.kick_master()
#             self.force_redraw()

#         if self.__left_button_pressed:
#             # при нажатой ЛКМ двигаем вертикальную линию - сканер
#             if self.__nearest_value_line != -1:
#                 self.ValueLines[self.__nearest_value_line] = (min(max(event.pos().x(), 2), self.__w - 1) / self.__w)
#                 self.LastValueLine = self.__nearest_value_line

#             if self.__nearest_vert_line != -1 and self.__nearest_value_line == -1:
#                 x_vert = min(max(event.pos().x(), 1), self.__w - 1)
#                 self.VertLines[self.__nearest_vert_line] = self.window_to_real_x(x_vert)
#             self.force_redraw()

#         if self.__scaling_rect_drawing:
#             if self.__animated and not self.__paused:
#                 return
#             self.__rectX1 = min(max(event.pos().x(), 0), self.__w)  # координаты второго угла прямоугольника
#             self.__rectY1 = min(max(event.pos().y(), self.__OFFSET_Y), self.__h + self.__OFFSET_Y)
#             self.force_redraw()

#         if self.__zoom_active:
#             set_crossed_cursor()

#     def key_release_event(self, event: QKeyEvent):
#         key = event.key()
#         if key == Qt.Key.Key_Control:
#             self.__ctrl_pressed = False
#         if key == key == Qt.Key.Key_Alt:
#             self.__alt_pressed = False

#     def key_press_event(self, event: QKeyEvent):
#         key = event.key()
#         match key:
#             case Qt.Key.Key_Control:
#                 self.__ctrl_pressed = True
#             case Qt.Key.Key_Alt:
#                 self.__alt_pressed = True
#             case Qt.Key.Key_Plus:
#                 self.__zoom()
#             case Qt.Key.Key_Minus:
#                 self.__zoom_out()
#             case Qt.Key.Key_3 | Qt.Key.Key_6 | Qt.Key.Key_9:
#                 speed = 0.005 if key == Qt.Key.Key_6 else (0.01 if key == Qt.Key.Key_9 else 0.001)
#                 if self.__ctrl_pressed:
#                     speed *= 10
#                 if self.__alt_pressed:
#                     speed /= 10
#                 if len(self.ValueLines):
#                     self.ValueLines[self.LastValueLine] += speed
#                     if self.ValueLines[self.LastValueLine] > 0.995:
#                         self.ValueLines[self.LastValueLine] = 0.995
#                         dx = self._real_width * speed
#                         if self.xstop + dx <= self.x_axis_max:
#                             self.set_x_stop(self.xstop + dx)
#                             self.set_x_start(self.xstart + dx)
#                             self.recalculate_window_coords()
#                             self.kick_master()
#                     self.force_redraw()
#             case Qt.Key.Key_1 | Qt.Key.Key_4 | Qt.Key.Key_7:
#                 speed = 0.005 if key == Qt.Key.Key_4 else (0.01 if key == Qt.Key.Key_7 else 0.001)
#                 if self.__ctrl_pressed:
#                     speed *= 10
#                 if self.__alt_pressed:
#                     speed /= 10
#                 if len(self.ValueLines):
#                     self.ValueLines[self.LastValueLine] -= speed
#                     if self.ValueLines[self.LastValueLine] < 0.005:
#                         self.ValueLines[self.LastValueLine] = 0.005
#                         dx = self._real_width * speed
#                         if self.xstart - dx >= self.x_axis_min:
#                             self.set_x_start(self.xstart - dx)
#                             self.set_x_stop(self.xstop - dx)
#                             self.recalculate_window_coords()
#                             self.kick_master()
#                     self.force_redraw()

#     def mouse_press_event(self, event: QMouseEvent):
#         if event.pos().y() < self.__OFFSET_Y:
#             return
#         self.__initial_x = event.pos().x() + self.__MIN_X - self.real_to_window_x(0)
#         # расстояние от точки касания до осей в пикселях
#         self.__initial_y = self.window_to_real_y(event.pos().y())

#         self.__touch_x = event.pos().x()
#         self.__touch_y = event.pos().y()

#         self.__right_button_pressed = (event.button() == Qt.MouseButton.RightButton)
#         match event.button():
#             case Qt.MouseButton.RightButton:
#                 set_grab_cursor()
#             case Qt.MouseButton.LeftButton:
#                 if not any(self.ValueLineSelected) and not any(self.VertLineSelected):
#                     if self.__animated and not self.__paused:
#                         return
#                     if self.__mouse_on_slider:
#                         self.__slider_pressed = True
#                         self.__slider_x0 = event.pos().x() + self.__x
#                         self.force_redraw()
#                         return

#                     if self._selectingPointGraph >= 0:     # выделение точки на графике
#                         self._plots[self._selectingPointGraph].selectedPoint.append(
#                             [self.window_to_real_x(self.__pointCoords[0] - self.__MIN_X),
#                              self.window_to_real_y(self.__pointCoords[1] + self.__OFFSET_Y),
#                              self.__pointCoords[2]])
#                         self.__point_added = True
#                         self.__pointsToSelect -= 1
#                         if self.__pointsToSelect == 0:
#                             self._selectingPointGraph = -1
#                             self.__ext_window.show()
#                             self.__ext_window.math_window.show()
#                         self.__rectX0 = 0
#                         self.__rectX1 = 0
#                         self.__rectY0 = 0
#                         self.__rectY1 = 0
#                         return
#                     if self.__zoom_active:
#                         self.__rectX0 = event.pos().x()
#                         self.__rectY0 = event.pos().y()
#                         self.__rectX1 = event.pos().x()
#                         self.__rectY1 = event.pos().y()
#                         self.__scaling_rect_drawing = True
#                 else:
#                     for i, x in enumerate(self.ValueLines):
#                         if self.ValueLineSelected[i]:
#                             self.__nearest_value_line = i
#                             break
#                     for i, x in enumerate(self.VertLines):
#                         if self.VertLineSelected[i]:
#                             self.__nearest_vert_line = i
#                             break
#                     self.__left_button_pressed = True
#                     self.force_redraw()
#             case Qt.MouseButton.XButton1:
#                 self.cancel_scaling()

#     def mouse_release_event(self, event: QMouseEvent):
#         if event.pos().y() < self.__OFFSET_Y and not self.__zoom_active:
#             return

#         match event.button():
#             case Qt.MouseButton.RightButton:
#                 self.__right_button_pressed = False
#                 set_default_cursor()
#             case Qt.MouseButton.LeftButton:
#                 self.__left_button_pressed = False

#                 if self.__slider_pressed:
#                     self.__slider_pressed = False
#                     self.force_redraw()
#                     return

#                 if self.__point_added:
#                     self.__point_added = False
#                     return

#                 self.__nearest_value_line = -1
#                 self.__nearest_vert_line = -1
#                 if self.__animated and not self.__paused or any(self.ValueLineSelected) or any(self.VertLineSelected):
#                     self.__scaling_rect_drawing = False
#                     return
#                 else:
#                     if self.__rectX0 == self.__rectX1 and self.__rectY0 == self.__rectY1 and not self.__zoom_active:
#                         if self.__touch_x == event.pos().x() and self.__touch_y == event.pos().y() and self.__pointsToSelect == 0:
#                             self.add_zoom_line(self.window_to_real_x(event.pos().x()))
#                     else:
#                         if abs(self.__rectX0 - self.__rectX1) < 10 or abs(self.__rectY0 - self.__rectY1) < 10:
#                             self.__scaling_rect_drawing = False
#                             self.force_redraw()
#                             return
#                         x0 = self.window_to_real_x(min(self.__rectX0, self.__rectX1))
#                         x1 = self.window_to_real_x(max(self.__rectX0, self.__rectX1))
#                         y0 = self.window_to_real_y(max(self.__rectY0, self.__rectY1))
#                         y1 = self.window_to_real_y(min(self.__rectY0, self.__rectY1))
#                         self.__action_buffer.add_action(self.xstart, self.xstop, self._ystart, self._ystop)
#                         self.set_x_start(x0)
#                         self.set_x_stop(x1)
#                         self.set_y_start(y0)
#                         self.set_y_stop(y1)
#                         self.update_step_y()
#                         self.update_step_x()
#                         self.recalculate_window_coords()
#                         self.__y_scaled = True
#                         if self.__master is not None:
#                             self.__master.set_x_start(x0)
#                             self.__master.set_x_stop(x1)
#                             self.__master.update_step_x()
#                             self.__master.recalculate_window_coords()
#                 self.__zoom_active = False
#                 set_default_cursor()
#                 self.__rectX0 = 0
#                 self.__rectX1 = 0
#                 self.__rectY0 = 0
#                 self.__rectY1 = 0
#                 self.__scaling_rect_drawing = False
#                 self.force_redraw()

#     def __zoom_out(self):
#         x_center = self.window_to_real_x(round(self.__MAX_X / 2))
#         self.__action_buffer.add_action(self.xstart, self.xstop, self._ystart, self._ystop)
#         if self.__MAXIMUM_X_WIDTH == -1:
#             self.set_x_start(self.x_axis_min)
#             self.set_x_stop(self.x_axis_max)
#         else:
#             self.set_x_start(max(self.x_axis_min, round(x_center - self.__MAXIMUM_X_WIDTH / 2)))
#             self.set_x_stop(min(self.x_axis_max, round(x_center + self.__MAXIMUM_X_WIDTH / 2)))
#         self.update_step_x()
#         self.__y_scaled = False
#         self.calculate_y_parameters()
#         self.update_step_y()
#         self.recalculate_window_coords()
#         self.VertLines.clear()
#         self.VertLineSelected[0] = False
#         self.VertLineSelected[1] = False

#         if self.__master:
#             # передаём данные мастеру
#             if self.__MAXIMUM_X_WIDTH == -1:
#                 self.__master.set_x_start(self.x_axis_min)
#                 self.__master.set_x_stop(self.x_axis_max)
#             else:
#                 self.__master.set_x_start(max(self.x_axis_min, round(x_center - self.__MAXIMUM_X_WIDTH / 2)))
#                 self.__master.set_x_stop(min(self.x_axis_max, round(x_center + self.__MAXIMUM_X_WIDTH / 2)))
#             self.__master.update_step_x()
#             self.__master.reset_y_axle()
#             self.__master.calculate_y_parameters()
#             self.__master.update_step_y()
#             self.__master.recalculate_window_coords()

#         self.force_redraw()

#     def mouse_double_click_event(self, event):
#         set_default_cursor()
#         if event.pos().y() < self.__OFFSET_Y or self.__slider_pressed:
#             return
#         match event.button():
#             case Qt.MouseButton.RightButton:
#                 if event.pos().y() < self.__OFFSET_Y or (self.__animated and not self.__paused):
#                     return
#                 # возвращаем исходный масштаб
#                 self.__zoom_out()

#             case Qt.MouseButton.MiddleButton:
#                 # удаляем линии-сканеры
#                 self.__deselect_all()
#                 self.ValueLines.clear()
#                 self.force_redraw()

#     def __deselect_all(self):
#         for i in range(self.__MAX_VAL_LINES):
#             self.ValueLineSelected[i] = False
#             if i < 2:
#                 self.VertLineSelected[i] = False

#     def find_indexes(self, i):
#         """нахождение индексов начальной и конечной отображаемых точек"""
#         plot = self._plots[i]
#         if not self.__animated and (plot.X[-1] < self.xstart or plot.X[0] > self.xstop):
#             return
#         plt_len = len(plot)

#         if not plot.x_ascending:
#             plot.index0 = 0
#             plot.index1 = plt_len - 1
#             return

#         if plt_len < 3:
#             return
#         try:
#             tmp = int(plt_len * (abs(self.xstart - self.x_axis_min) / (self.x_axis_max - self.x_axis_min))) - 1
#         except ZeroDivisionError:
#             return
#         # предположительный индекс начальной точки
#         tmp = min(tmp, plt_len - 1)
#         while tmp > 0 and plot.X[tmp] > self.xstart:
#             tmp -= 1
#         if tmp < 0:
#             tmp = 0

#         plot.index0 = tmp

#         tmp = int(plt_len * (abs(self.xstop - self.x_axis_min) /
#                                  (self.x_axis_max - self.x_axis_min))) - 1
#         # предположительный индекс конечной точки
#         while tmp < plt_len - 1 and plot.X[tmp] < self.xstop:
#             tmp += 1
#         if tmp > plt_len - 1:
#             tmp = plt_len - 1
#         plot.index1 = tmp

#     def add_zoom_line(self, x):
#         if len(self.VertLines) < 2:
#             self.VertLines.append(x)
#         self.force_redraw()

#     def add_value_line(self):
#         if len(self.ValueLines) < self.__MAX_VAL_LINES:
#             self.ValueLines.append(0.3 * len(self.ValueLines) + 0.2)
#             if self.__master is not None:
#                 self.__master.add_value_line()
#             self.force_redraw()

#     def __draw_hist(self, x_win, y_win, x_ascending, pen, origin_ax='x', heatmap=False):
#         if not x_ascending or len(x_win) == 0:
#             return

#         zero = self.real_to_window_y(0) if origin_ax == 'x' else self.real_to_window_x(0)
#         self._qp.setPen(QColor(0, 0, 0, 0))
#         self._qp.setBrush(pen.color())

#         gradient = Gradient(QColor(68, 1, 84), QColor(253, 231, 36))
#         gradient.set_color_at(0.5, QColor(33, 141, 140))

#         max_h = max([self.__MAX_Y - y_win[i] for i in range(len(y_win))])
#         min_h = min([self.__MAX_Y - y_win[i] for i in range(len(y_win))])

#         prev_xk = 0
#         for i in range(len(x_win)):
#             if i == 0:
#                 rect_width = (x_win[i + 1] - x_win[i]) if len(x_win) > 1 else self._real_width // 4
#                 prev_xk = x_win[i] + rect_width / 2
#             else:
#                 rect_width = (x_win[i] - x_win[i - 1])
#                 if x_win[i] - rect_width / 2 - prev_xk > 0:
#                     rect_width += 1
#                 prev_xk = x_win[i] + rect_width / 2

#             if x_win[i] + rect_width / 2 < self.__x:
#                 continue
#             if x_win[i] - rect_width / 2 > self.__MAX_X:
#                 break

#             rect_y = max(min(zero, self.__MAX_Y), self.__MIN_Y) + 1
#             rect_x = max(self.__x, x_win[i] - rect_width / 2)

#             rect_w = rect_width if rect_x > self.__x else rect_width - abs(self.__x - (x_win[i] - rect_width / 2))
#             rect_w = min(rect_w, abs(rect_x - self.__MAX_X))
#             rect_h = max(min(y_win[i], self.__MAX_Y), self.__MIN_Y) - rect_y

#             if heatmap:
#                 h = self.__MAX_Y - y_win[i]
#                 self._qp.setBrush(gradient.get_color((h - min_h) / (max_h - min_h)))
#             self._qp.drawRect(QRectF(rect_x, rect_y, rect_w, rect_h))

#     def __draw_static_plot(self, x_win, y_win, x_ascending=True):
#         if len(x_win) == 0:
#             return
#         buffered_x = x_win[0]
#         buffered_y = y_win[0]
#         bufferizations = 0
#         x_end = False
#         for i in range(len(x_win)):
#             if i == 0 or x_win[i] < self.__MIN_X:
#                 continue

#             x0 = x_win[i - 1]
#             x1 = x_win[i]
#             y0 = y_win[i - 1]
#             y1 = y_win[i]

#             if (y0 < self.__MIN_Y and y1 < self.__MIN_Y) or (y0 > self.__MAX_Y and y1 > self.__MAX_Y):
#                 bufferizations = 0
#                 buffered_x = x0
#                 buffered_y = y0
#                 continue

#             # ограничим значения пределами окна
#             if x0 < self.__MIN_X:
#                 y0 = round(interpolate(self.__MIN_X, [x0, x1], [y0, y1]))
#                 x0 = self.__MIN_X
#             if x1 > self.__MAX_X:
#                 y1 = round(interpolate(self.__MAX_X, [x0, x1], [y0, y1]))
#                 x1 = self.__MAX_X
#                 x_end = x_ascending

#             if y0 < self.__MIN_Y:
#                 x0 = round(interpolate(self.__MIN_Y, [y0, y1], [x0, x1]))
#                 y0 = self.__MIN_Y
#             if y1 < self.__MIN_Y:
#                 x1 = round(interpolate(self.__MIN_Y, [y0, y1], [x0, x1]))
#                 y1 = self.__MIN_Y

#             if y0 > self.__MAX_Y:
#                 x0 = round(interpolate(self.__MAX_Y, [y1, y0], [x1, x0]))
#                 y0 = self.__MAX_Y
#             if y1 > self.__MAX_Y:
#                 x1 = round(interpolate(self.__MAX_Y, [y0, y1], [x0, x1]))
#                 y1 = self.__MAX_Y

#             if i == len(x_win) - 1:
#                 x_end = True

#             if x_ascending:
#                 if y0 == y1 and not x_end:
#                     # если значение У не изменилось и мы не на последней точке...
#                     if buffered_y != y0:
#                         # сохраняем значение в память, если ещё этого не сделали
#                         buffered_x = x0
#                         buffered_y = y0
#                     bufferizations += 1
#                     # и ничего не рисуем
#                     continue
#                 if bufferizations > 0 and (buffered_y != y1 or x_end):  # значение Y изменилось или точка последняя
#                     if buffered_x < self.__MIN_X:
#                         buffered_y = round(interpolate(self.__MIN_X, [buffered_x, x0], [buffered_y, y0]))
#                         buffered_x = self.__MIN_X
#                     # если вдруг вторая точка выходит за пределы окна
#                     if x0 > self.__MAX_X:
#                         y0 = round(interpolate(self.__MAX_X, [buffered_x, x0], [buffered_y, y0]))
#                         x0 = self.__MAX_X
#                     self._qp.drawLine(QLineF(buffered_x, buffered_y, x0, y0))
#                     bufferizations = 0

#             if self.__MIN_X <= x0 <= self.__MAX_X and self.__MIN_X <= x1 <= self.__MAX_X:
#                 self._qp.drawLine(QLineF(x0, y0, x1, y1))
#                 bufferizations = 0
#                 buffered_x = x1
#                 buffered_y = y1

#             if x_end:
#                 return

#     def __redraw_plot(self, n_plot: int) -> None:
#         """Перерисовывание одного графика"""
#         if len(self._plots[n_plot]) == 0 or self._plots[n_plot].animated:
#             return

#         if self._plots[n_plot].is_dotted:
#             pen = QPen(self._plots[n_plot].pen)
#             pen.setWidthF(self._plots[n_plot].marker_width)
#             self._qp.setPen(pen)
#             for x, y in zip(self._plots[n_plot].Xwin, self._plots[n_plot].Ywin):
#                 if self.__MIN_X < x < self.__MAX_X and self.__MIN_Y < y < self.__MAX_Y:
#                     self._qp.drawPoint(QPointF(x, y))

#         if not self._plots[n_plot].draw_line:
#             return

#         if self._plots[n_plot].bar:
#             self.__draw_hist(self._plots[n_plot].Xwin, self._plots[n_plot].Ywin,
#                              self._plots[n_plot].x_ascending, pen=self._plots[n_plot].pen,
#                              heatmap=self._plots[n_plot].heatmap)
#             if self._plots[n_plot].heatmap:
#                 x = self.__x + 5
#                 y = self._y + 5
#                 w = int(self.__w * 0.2)
#                 h = 20
#                 gradient = QLinearGradient(x, y, x + w, y + h)
#                 gradient.setColorAt(0, QColor(68, 1, 84))
#                 gradient.setColorAt(0.5, QColor(33, 141, 140))
#                 gradient.setColorAt(1, QColor(253, 231, 36))

#                 self._qp.setBrush(gradient)
#                 self._qp.drawRect(x, y, w, h)

#                 self._qp.setPen(QColor(0, 0, 0))
#                 self._qp.setFont(QFont("bahnschrift", 8))

#                 self._qp.drawText(x, y + h + 10, str(min(self._plots[n_plot].Y)))
#                 self._qp.drawText(x + w - 15, y + h + 10, str(max(self._plots[n_plot].Y)))
#         else:
#             self._qp.setPen(self._plots[n_plot].pen)  # берём нужную ручку
#             self.__draw_static_plot(self._plots[n_plot].Xwin, self._plots[n_plot].Ywin,
#                                     self._plots[n_plot].x_ascending)

#     def __redraw_animated_plots(self):
#         if not self.__animated:
#             return

#         if self.__master and self.__master.slave_restart_flags[self.__my_index]:
#             self.restart_animation()

#         for i, plt in enumerate(self._plots):
#             if not plt.visible or len(plt) < 2 or not plt.animated:
#                 continue

#             if self.__paused:
#                 self._qp.setPen(plt.pen)
#                 if plt.draw_line:
#                     self.__draw_static_plot(plt.Xwin, plt.Ywin)
#                 if plt.is_dotted:
#                     pen = QPen(plt.pen)
#                     pen.setWidthF(plt.marker_width)
#                     self._qp.setPen(pen)
#                     for x, y in zip(plt.Xwin, plt.Ywin):
#                         if self.__MIN_X < x < self.__MAX_X and self.__MIN_Y < y < self.__MAX_Y:
#                             self._qp.drawPoint(QPointF(x, y))
#                         if x >= self.__MAX_X:
#                             break
#                 continue

#             self._qp.setPen(plt.pen)
#             buffered_x = plt.X[0]
#             buffered_x_win = self.real_to_window_x(buffered_x)
#             buffered_y = plt.Y[0]
#             buffered_y_win = self.real_to_window_y(buffered_y)

#             for j, x in enumerate(plt.X):
#                 if j == 0:
#                     if x > self.xstart:
#                         self.xstart = x
#                         self.x_axis_min = x
#                     continue
#                 x0 = plt.X[j - 1]
#                 x1 = plt.X[j]
#                 y0 = plt.Y[j - 1]
#                 y1 = plt.Y[j]
#                 if y0 == y1:
#                     # если значение У не изменилось
#                     if buffered_y != y0:
#                         # сохраняем значение в память, если ещё этого не сделали
#                         buffered_y = y0
#                         buffered_x_win = self.real_to_window_x(x0)
#                         buffered_y_win = self.real_to_window_y(y0)
#                 else:
#                     buffered_y = y0
#                     buffered_x_win = self.real_to_window_x(x0)
#                     buffered_y_win = self.real_to_window_y(y0)

#                 if self.xstart < x1 < self.xstop and self._ystart <= y1 <= self._ystop and x0 > self.xstart:
#                     x = self.real_to_window_x(x1)
#                     y = self.real_to_window_y(y1)
#                     if plt.draw_line:
#                         self._qp.drawLine(QLineF(max(buffered_x_win, self.__MIN_X), buffered_y_win, x, y))

#                     if plt.is_dotted:
#                         pen = QPen(plt.pen)
#                         pen.setWidthF(plt.marker_width)
#                         self._qp.setPen(pen)
#                         self._qp.drawPoint(QPointF(x, y))

#         if self.__paused:
#             return

#         maximums = [plt.max(1) for plt in self._plots if plt.visible]
#         minimums = [plt.min(1) for plt in self._plots if plt.visible]

#         if len(maximums):
#             y_max = max(maximums)
#             y_min = min(minimums)
#             if abs(y_max - y_min) < 1e-10:
#                 y_max += 1
#         else:
#             y_max = 1
#             y_min = 0

#         if self.__zero_y_fixed:
#             if y_min > 0:
#                 y_min = 0
#             if y_max < 0:
#                 y_max = 0

#         self.__Y_STOP_COEFF = (y_max - y_min) / 20
#         ystart = y_min if self.__zero_y_fixed and y_min == 0 else y_min - self.__Y_STOP_COEFF
#         ystop = y_max if self.__zero_y_fixed and y_max == 0 else y_max + self.__Y_STOP_COEFF
#         self.set_y_stop(ystop)
#         self._y_axis_max = y_max

#         self.set_y_start(ystart)
#         self._y_axis_min = y_min
#         self.update_step_y()

#     def __draw_vertical_lines(self):
#         self._qp.setFont(QFont('consolas', 10))
#         # вертикальные линии для масштабирования
#         prev_val_line_coord_xwin = 0
#         prev_val_line_coord_xreal = 0
#         for i in range(len(self.__master.VertLines if self.__master else self.VertLines)):
#             if self._dark:
#                 color = 'lightblue' if self.VertLineSelected[i] else QColor(103, 115, 229)
#             else:
#                 color = 'lightblue' if self.VertLineSelected[i] else 'darkblue'
#             pen = QPen(QColor(color), 1)
#             self._qp.setPen(pen)
#             x_real = self.__master.VertLines[i] if self.__master is not None else self.VertLines[i]
#             x_win = self.real_to_window_x(x_real)
#             self._qp.drawLine(QLineF(x_win, self.__MIN_Y, x_win, self.__MAX_Y))

#             # формируем подпись со значением Х, на котором стоит линия
#             tmp_str = convert_timestamp_to_human_time(x_real + self.__initial_timestamp, millis=True) \
#                 if self.__convert_to_hhmmss else f"{x_real:.2f}"

#             font = QFont('bahnschrift', 10)
#             font.setBold(True)
#             self._qp.setFont(font)
#             qm = QFontMetrics(font)
#             text_width = qm.size(0, tmp_str).width()  # измеряем текст

#             rectX = x_win - text_width - 15 if x_win > self.__MIN_X + self.__w / 2 else x_win + 5
#             rectY = self._y + 18 + 20 * i
#             rectW = text_width + 10
#             rectH = 15
#             self._qp.setPen(QColor(0, 0, 0, alpha=0))
#             self._qp.setBrush(QColor(0, 128, 128))
#             self._qp.drawRoundedRect(QRectF(rectX, rectY, rectW, rectH), 5, 5)
#             self._qp.setPen(QColor(255, 255, 255, alpha=255))
#             self._qp.drawText(QRectF(rectX, rectY, rectW, rectH), Qt.AlignmentFlag.AlignCenter, tmp_str)

#             if i > 0:
#                 self._qp.setPen(QColor(100, 100, 100))
#                 y = self.__MIN_Y + 2
#                 if self._dark:
#                     pen = QPen(QColor(200, 200, 200))
#                 else:
#                     pen = QPen(QColor(0, 0, 0))
#                 pen.setStyle(Qt.PenStyle.DotLine)
#                 self._qp.setPen(pen)
#                 self._qp.drawLine(QLineF(x_win, y, prev_val_line_coord_xwin, y))

#                 self._qp.setPen(QColor(0, 0, 0, alpha=0))
#                 self._qp.setBrush(QColor(0, 102, 172, alpha=255))

#                 dx = abs(x_real - prev_val_line_coord_xreal)
#                 if self.__convert_to_hhmmss:
#                     tmp_str = convert_timestamp_to_human_time(dx, millis=True)
#                 else:
#                     if self.__step_grid_x < 0.001:
#                         tmp_str = f"{dx:.3e}"
#                     elif self.__step_grid_x > 9999:
#                         tmp_str = f"{dx:.2E}"
#                     else:
#                         tmp_str = f"{dx:.3f}"
#                 font = QFont("consolas", 9)
#                 font.setBold(True)
#                 if self._dark:
#                     self._qp.setPen(QColor(255, 255, 255))
#                 else:
#                     self._qp.setPen(QColor(100, 100, 100))
#                 self._qp.setFont(font)
#                 text_width = qm.size(0, tmp_str).width()
#                 rectW = text_width + 10
#                 rect_x = (min(prev_val_line_coord_xwin, x_win) +
#                           (abs(prev_val_line_coord_xwin - x_win) - rectW) // 2)
#                 rectH = 15
#                 rectY = y + 3
#                 if abs(prev_val_line_coord_xwin - x_win) < rectW:
#                     if rect_x > self.__x + self.__w / 2:
#                         rect_x -= rectW
#                     else:
#                         rect_x += rectW

#                 self._qp.drawText(QRectF(rect_x, rectY, rectW, rectH),
#                                   Qt.AlignmentFlag.AlignCenter, tmp_str)

#             prev_val_line_coord_xwin = x_win
#             prev_val_line_coord_xreal = x_real

#     def __get_value_line_coord(self, val):
#         return int(val * self.__w)

#     def __draw_scanners(self):
#         # вертикальные линии-сканеры
#         if len(self.ValueLines) == 0:
#             return
#         prev_val_line_coord_xwin = -1
#         prev_val_line_coord_xreal = -1
#         for i, ValueLine in enumerate(self.ValueLines):
#             x_win = self.__get_value_line_coord(ValueLine)
#             x_real = self.window_to_real_x(float(x_win))
#             if self.xstart < x_real < self.xstop:
#                 if self.__convert_to_hhmmss:
#                     tmp_str = convert_timestamp_to_human_time(x_real + self.__initial_timestamp, millis=True)
#                 else:
#                     if self.__step_grid_x < 0.001:
#                         tmp_str = f"{x_real:.3e}"
#                     elif self.__step_grid_x > 9999:
#                         tmp_str = f"{x_real:.2E}"
#                     else:
#                         tmp_str = f"{x_real:.3f}"

#                 font = QFont("consolas", 10)
#                 font.setBold(True)
#                 self._qp.setFont(font)
#                 qm = QFontMetrics(font)
#                 text_width = qm.size(0, tmp_str).width()  # измеряем текст

#                 self._qp.setPen(QColor(0, 0, 0, alpha=0))
#                 self._qp.setBrush(QColor(0, 162, 232, alpha=255))
#                 rectX = x_win - text_width - 15 + self.__MIN_X
#                 if rectX < self.__MIN_X:
#                     rectX = x_win + 10 + self.__MIN_X
#                 rectW = text_width + 10
#                 rectH = 17
#                 rectY = self.__MAX_Y - rectH - 3
#                 if rectX + rectW > self.__MAX_X - (200 if self.__master is None else 150):
#                     rectY -= 27
#                 self._qp.drawRoundedRect(QRectF(rectX, rectY, rectW, rectH), 5, 5)
#                 self._qp.setPen(QColor(255, 255, 255, alpha=255))

#                 self._qp.drawText(QRectF(rectX, rectY, rectW, rectH),
#                                   Qt.AlignmentFlag.AlignCenter, tmp_str)  # значение по Х

#                 if self._dark:
#                     col = (102, 189, 108) if self.ValueLineSelected[i] else (200, 200, 200)
#                 else:
#                     col = (102, 189, 108) if self.ValueLineSelected[i] else (0, 0, 0)
#                 th = 1 if self.ValueLineSelected[i] else 1
#                 self._qp.setPen(QPen(QColor(*col), th))
#                 self._qp.drawLine(QLineF(x_win + self.__x, self.__MIN_Y, x_win + self.__x, self.__MAX_Y))

#                 if i > 0:
#                     self._qp.setPen(QColor(100, 100, 100))
#                     y = self.__MIN_Y + 2
#                     pen = QPen(QColor(0, 0, 0))
#                     pen.setStyle(Qt.PenStyle.DashLine)
#                     self._qp.setPen(pen)
#                     self._qp.drawLine(QLineF(x_win + self.__x, y, prev_val_line_coord_xwin, y))

#                     self._qp.setPen(QColor(0, 0, 0, alpha=0))
#                     self._qp.setBrush(QColor(0, 102, 172, alpha=255))

#                     dx = abs(x_real - prev_val_line_coord_xreal)
#                     if self.__convert_to_hhmmss:
#                         tmp_str = convert_timestamp_to_human_time(dx, millis=True)
#                     else:
#                         if self.__step_grid_x < 0.001:
#                             tmp_str = f"{dx:.3e}"
#                         elif self.__step_grid_x > 9999:
#                             tmp_str = f"{dx:.2E}"
#                         else:
#                             tmp_str = f"{dx:.3f}"
#                     font = QFont("consolas", 9)
#                     font.setBold(True)
#                     self._qp.setPen(QColor(100, 100, 100))
#                     self._qp.setFont(font)
#                     text_width = qm.size(0, tmp_str).width()
#                     rectW = text_width + 10
#                     rect_x = (min(prev_val_line_coord_xwin, (x_win + self.__x)) +
#                               (abs(prev_val_line_coord_xwin - (x_win + self.__x)) - rectW) // 2)
#                     rectH = 15
#                     rectY = y + 3
#                     if abs(prev_val_line_coord_xwin - (x_win + self.__x)) < rectW:
#                         if rect_x > self.__x + self.__w / 2:
#                             rect_x -= rectW
#                         else:
#                             rect_x += rectW

#                     self._qp.drawText(QRectF(rect_x, rectY, rectW, rectH),
#                                       Qt.AlignmentFlag.AlignCenter, tmp_str)

#                 prev_val_line_coord_xwin = x_win + self.__x
#                 prev_val_line_coord_xreal = x_real

#     def __draw_scaling_rect(self):
#         if self.__scaling_rect_drawing:
#             # рисуем масштабирующий прямоугольничек
#             if self._dark:
#                 self._qp.setPen(QPen(QColor(200, 200, 200), 1))
#             else:
#                 self._qp.setPen(QPen(QColor(0, 0, 0), 1))
#             self._qp.setBrush(QColor(0, 0, 0, alpha=0))
#             self._qp.drawRect(self.__rectX0 + self.__x,
#                               self.__rectY0 + self._y - self.__OFFSET_Y,
#                               (self.__rectX1 - self.__rectX0),
#                               (self.__rectY1 - self.__rectY0))

#     def __draw_points(self):
#         N_points = len(self.points)
#         if N_points:
#             font = QFont("consolas", 12)
#             self._qp.setFont(font)
#             metr = QFontMetrics(QFont("consolas", 12))
#             for i, point in enumerate(self.points):
#                 if self.xstart <= point["x"] <= self.xstop and self._ystart <= point["y"] <= self._ystop:
#                     self._qp.setPen(QPen(QColor(point["color"]), point["size"], cap=point["shape"]))
#                     x = self.real_to_window_x(point["x"])
#                     y = self.real_to_window_y(point["y"])
#                     self._qp.drawPoint(QPointF(x, y))
#                     text_width = metr.size(0, point["text"]).width()
#                     text_height = metr.size(0, point["text"]).height()
#                     self._qp.drawText(QRectF(x - text_width / 2, y - text_height * 3 / 2, text_width, text_height),
#                                       Qt.AlignmentFlag.AlignCenter, point["text"])

#     def __draw_plot_labels(self):
#         if len(self._plots) == 0:
#             return
#         total_width = 0
#         for gi in range(len(self._plots)):  # имена графиков
#             font = QFont('bahnschrift', 10)
#             font.setBold(True)
#             self._qp.setFont(font)
#             qm = QFontMetrics(font)

#             # измеряем текст
#             text_width = qm.horizontalAdvance(self._plots[gi].name)

#             text_width += 30
#             self._qp.setPen(self._plots[gi].pen)
#             x = self.__x + total_width + 16

#             if self.__MIN_X <= x <= self.__MAX_X:
#                 self._qp.drawText(x, self.__MIN_Y - self.__OFFSET_Y + 14,
#                                   self._plots[gi].name)  # пишем имя графика сверху нужным цветом

#             if len(self._plots) > 0 and len(self.__checkboxes) < len(self._plots):
#                 # если массив чекбоксов не заполнен до конца, добавляем новый
#                 chb = QtWidgets.QCheckBox(self.__frame)
#                 chb.setChecked(self._plots[gi].visible)
#                 chb.setGeometry(total_width, 2, 15, 15)
#                 # if self.__dark:
#                 #     chb.setStyleSheet("""
#                 #     QCheckBox::indicator {
#                 #                                     border : 2px solid white;
#                 #         width : 10px;
#                 #         height : 10px;
#                 #         border-radius : 7px;
#                 #         }
#                 #
#                 #     """)
#                 self.__checkboxes.append(chb)
#                 try:
#                     self.__checkboxes[-1].clicked.connect(self.force_redraw)
#                     self.__checkboxes[-1].show()
#                 except IndexError:
#                     pass

#             total_width += text_width

#     def __draw_y_values(self):
#         if len(self._plots) == 0:
#             return
#         for d, ValueLine in enumerate(self.ValueLines):
#             y_array = []
#             w_array = []
#             x_array = []
#             strings = []
#             n_points = []
#             ValueLine = self.__get_value_line_coord(ValueLine)

#             for gi in range(len(self._plots)):
#                 self._qp.setPen(self._plots[gi].pen)
#                 self._qp.setBrush(self._plots[gi].pen.color())

#                 x_real = self.window_to_real_x(ValueLine)

#                 if len(self.ValueLines) and not self.__relay_type and self.xstart < x_real < self.xstop:

#                     nearest_values = self._plots[gi].get_nearest(x_real)
#                     n_points.append(len(nearest_values))

#                     for nearest_value in nearest_values:
#                         indx = nearest_value[1]
#                         time_value = nearest_value[0]

#                         if self._plots[gi].bar:
#                             value_to_display = self._plots[gi].Y[indx]
#                         else:
#                             if self._plots[gi].length == 0:
#                                 value_to_display = 0
#                             else:
#                                 indx1 = (indx + 1) if time_value - x_real < 0 else (indx - 1)

#                                 if indx1 >= 0 and indx >= 0:
#                                     if (x_real >= self._plots[gi].X[-1] and
#                                             self._plots[gi].x_ascending):
#                                         value_to_display = self._plots[gi].Y[-1]
#                                     else:
#                                         # линейно интерполируем
#                                         i0 = min(indx1, indx)
#                                         ik = max(indx1, indx)
#                                         xp = [self._plots[gi].X[i0], self._plots[gi].X[ik]]
#                                         fp = [self._plots[gi].Y[i0], self._plots[gi].Y[ik]]
#                                         try:
#                                             value_to_display = np.interp(x_real, xp, fp)
#                                         except:
#                                             value_to_display = 0
#                                 else:
#                                     value_to_display = self._plots[gi].Y[0]

#                         if value_to_display == 0:
#                             tmp_str = "0.00"
#                         elif abs(value_to_display) < 0.001:
#                             tmp_str = f" {value_to_display:.3e}"
#                         elif abs(value_to_display) < 0.01:
#                             tmp_str = f" {value_to_display:.3f}"
#                         elif abs(value_to_display) > 9999:
#                             tmp_str = f" {value_to_display:.2E}"
#                         else:
#                             tmp_str = f" {value_to_display:4.2f}"
#                         self.__values_from_slider[d][gi] = value_to_display

#                         # ставим точку на графике на этом значении
#                         if self._plots[gi].visible:
#                             pen = QPen(self._plots[gi].pen.color())
#                             pen.setCapStyle(Qt.PenCapStyle.SquareCap)
#                             pen.setWidth(8)
#                             self._qp.setPen(pen)
#                             self._qp.drawPoint(QPointF(ValueLine + self.__x,
#                                                        min(max(self.real_to_window_y(value_to_display), self.__MIN_Y),
#                                                     self.__MAX_Y)))

#                         # готовимся рисовать прямоугольник со значением
#                         font = QFont('consolas', 10)
#                         self._qp.setFont(font)

#                         text_width = QFontMetrics(font).horizontalAdvance(tmp_str)  # измеряем текст

#                         strings.append(tmp_str)

#                         rectW = text_width + 10
#                         rectH = 15
#                         rectX = (ValueLine + 10 + self.__x) if ValueLine < self.__w * 0.7 else (ValueLine - rectW
#                                                                                                 + self.__x - 10)
#                         rectY = min(max(self.real_to_window_y(value_to_display), self.__MIN_Y),
#                                     self.__MAX_Y - rectH - (28 if ValueLine < self.__w * 0.7 else 50))
#                         if ValueLine >= self.__MAX_X - 210 - rectW:
#                             rectY = min(self.__MAX_Y - 70, rectY)
#                         if gi > 0:
#                             # если поставили больше одной метки
#                             i = 0
#                             while i < len(y_array):
#                                 if abs(rectY - y_array[i]) < 17 and abs(rectX - x_array[i]) < 25:
#                                     # если метки наезжают друг на друга, находясь на одном уровне по горизонтали
#                                     if ValueLine >= self.__w * 0.7:
#                                         rectX -= (w_array[i] + 5)
#                                     else:
#                                         rectX += w_array[i] + 5  # сдвигаем метку на ширину предыдущей метки
#                                 i += 1

#                         if gi < len(self.__checkboxes) and not self.__checkboxes[gi].isChecked():
#                             rectY = 0
#                             rectX = 0
#                             rectW = 0

#                         y_array.append(rectY)
#                         x_array.append(rectX)
#                         w_array.append(rectW)

#             for i in range(1, len(x_array)):
#                 for j in range(len(x_array)):
#                     if i <= j:
#                         continue
#                     if abs(y_array[j] - y_array[i]) < 17 and abs(x_array[j] - x_array[i]) < 25:
#                         if ValueLine >= self.__w * 0.7:
#                             x_array[i] -= w_array[j] + 5
#                         else:
#                             x_array[i] += w_array[j] + 5

#             if not self.__relay_type:
#                 length = len(self._plots)
#                 for i in range(length):
#                     pen = QPen(self._plots[i].pen.color())
#                     clr = pen.color()
#                     clr.setAlpha(255)
#                     if len(n_points) > i:
#                         for j in range(n_points[i]):
#                             if i > 0:
#                                 j += sum(n_points[:i])
#                             self._qp.setBrush(clr)
#                             self._qp.setPen(QColor(255, 255, 255, alpha=0))
#                             self._qp.drawRoundedRect(QRectF(x_array[j], y_array[j], w_array[j], 15), 5, 5)
#                             self._qp.setPen(QColor(255, 255, 255, alpha=255))
#                             self._qp.drawText(QRectF(x_array[j], y_array[j], w_array[j], 15),
#                                               Qt.AlignmentFlag.AlignCenter, strings[j])

#     def __call_master(self):
#         # сверяемся с мастером
#         if self.__master:
#             if self.__paused != self.__master.is_paused():
#                 self.__paused = self.__master.is_paused()
#                 if self.__paused:
#                     self.x_axis_min = self.__master.x_axis_min
#                     self.x_axis_max = self.__master.x_axis_max
#                     self.recalculate_window_coords()
#             if (self.__master.xstart != self.xstart or self.__master.xstop != self.xstop) and self.__x_auto_scale:
#                 self.set_x_start(self.__master.xstart)
#                 self.set_x_stop(self.__master.xstop)
#                 self.recalculate_window_coords()
#                 self.update_step_x()

#     def __button_tmr_proc(self):
#         TIMEOUT = 5
#         T = time.time() - self.__button_tmr
#         if T <= TIMEOUT and not self.__button_flag:
#             if self.__master is None:
#                 self.__clear_button.setVisible(True)
#                 self.__add_vert_button.setVisible(True)
#             self.__fix_button.setVisible(True)
#             self.__back_button.setVisible(True)
#             self.__save_button.setVisible(True)
#             self.__zoom_button.setVisible(True)
#             self.__more_button.setVisible(True)
#             self.__arrow_button.setVisible(True)

#             self.__button_flag = True

#         elif T > TIMEOUT and self.__button_flag:
#             if self.__master is None:
#                 self.__clear_button.setVisible(False)
#                 self.__add_vert_button.setVisible(False)
#             self.__fix_button.setVisible(False)
#             self.__back_button.setVisible(False)
#             self.__save_button.setVisible(False)
#             self.__zoom_button.setVisible(False)
#             self.__more_button.setVisible(False)

#             self.__button_flag = False

#     def _redraw_without_qp(self):
#         # перерисовываем графики
#         for i in range(len(self._plots)):
#             if self._plots[i].visible:
#                 self.__redraw_plot(i)
#         self.__redraw_animated_plots()

#         self.__draw_vertical_lines()
#         self.__draw_scanners()
#         self.__draw_scaling_rect()
#         self.__draw_point_on_graph()
#         self.__draw_points()
#         self.__draw_y_values()
#         self.__draw_plot_labels()

#         if not self.__animated:
#             self.__draw_x_slider()
#         # **********************************************************
#         if not self.__animated or self.__paused:
#             self.__redraw_flag = False

#         self.__button_tmr_proc()

#     def redraw_plots(self):
#         self.__button_tmr_proc()

#         if not self._visible:
#             return
#         self.check_graph_visibility()
#         self.update_extended_window()
#         self.__call_master()

#         self._qp.begin(self._widget)
#         self._qp.setRenderHint(QPainter.RenderHint.Antialiasing)
#         self._draw_axes()

#         # перерисовываем графики
#         for i in range(len(self._plots)):
#             if self._plots[i].visible:
#                 self.__redraw_plot(i)
#         self.__redraw_animated_plots()

#         self.__draw_vertical_lines()
#         self.__draw_scanners()
#         self.__draw_scaling_rect()
#         self.__draw_point_on_graph()
#         self.__draw_points()
#         self.__draw_y_values()
#         self.__draw_plot_labels()
#         self.__draw_plot_labels()

#         if not self.__animated:
#             self.__draw_x_slider()

#         self._qp.end()
#         # **********************************************************
#         if not self.__animated or self.__paused:
#             self.__redraw_flag = False
