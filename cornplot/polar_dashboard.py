import os
from typing import Iterable
from array import array
from math import sqrt, atan2, degrees, pi

from PyQt6.QtGui import QPainter, QPainterPath, QPen, QFont, QFontMetrics, QAction
from PyQt6.QtWidgets import QMenu, QFileDialog
from PyQt6.QtCore import QPointF, QLineF, Qt, pyqtSlot as Slot, QRect

from .polar_axles import PolarAxles
from .polar_plot import PolarPlot
from .color_generator import ColorGenerator
from .utils import *
from .polar_scanner_line import PolarScannerLine
from .array_utils import *
from .value_rectangle import ValueRectangle


VALUE_FONT = QFont("Consolas, Courier New", 10)
VALUE_FONT.setBold(True)


class DashboardPolar(PolarAxles):
    __MAX_POINTS = 5000

    def __init__(self, widget, x, y, size):
        super().__init__(widget, x, y, size)

        self.__plots: list[PolarPlot] = list()
        self.__color_generator = ColorGenerator()
        self.__scanner_line = PolarScannerLine()

        self.__left_button_pressed = False
        self.__take_picture = False

        self.__menu = QMenu(self)

        self.__addScanner = QAction("Показывать сканер")
        self.__addScanner.setCheckable(True)
        self.__addScanner.toggled.connect(self.__show_scanner)

        self.__rotateScanner = QAction("Вращение сканера")
        self.__rotateScanner.setCheckable(True)
        self.__rotateScanner.toggled.connect(self.__start_scanner_rotation)

        self.__savePicture = QAction("Сохранить изображение")
        self.__savePicture.triggered.connect(self.__save_picture)

        self.__menu.addAction(self.__addScanner)
        self.__menu.addAction(self.__rotateScanner)
        self.__menu.addSeparator()
        self.__menu.addAction(self.__savePicture)

    @Slot()
    def __save_picture(self):
        fileName, _ = QFileDialog.getSaveFileName(self, "Сохранить картинку", "",
                                                            "PNG Files (*.png)")
        if len(fileName) > 0:
            self.__take_picture = True
            self.repaint()
            grab = self.grab(QRect(0, 0, self.width(), self.height()))
            grab.save(fileName, 'png')
            try:
                os.startfile(fileName)
            except:
                pass
            self.__take_picture = False
            self.repaint()

    def add_plot(self, amplitudes: Iterable[float], angles: Iterable[float], color='any',
                 linewidth=2.0, linestyle='solid', scatter=False):
        if not hasattr(amplitudes, "__iter__"):
            return False
        if not hasattr(angles, "__iter__"):
            return False
        if len(amplitudes) != len(amplitudes) or len(amplitudes) < 2:
            return False
        
        plt = PolarPlot(amplitudes, angles, self.__get_pen(color, linewidth, linestyle))
        plt.X = array("d", [self._polar_coords_to_x(r, a) for r, a in zip(amplitudes, angles)])
        plt.Y = array("d", [self._polar_coords_to_y(r, a) for r, a in zip(amplitudes, angles)])
        plt.draw_markers = scatter
        plt.draw_line = not scatter

        x_max, x_min = max(plt.X), min(plt.X)
        y_max, y_min = max(plt.Y), min(plt.Y)
        # все значения графика в одной точке
        if x_max - x_min == 0 and y_max - y_min == 0:
            return False

        maximum_abs_amplitude = np.max(np.abs(amplitudes))
        if maximum_abs_amplitude > self._max_value or len(self.__plots) == 0:
            self._max_value = maximum_abs_amplitude
            self._min_value = -maximum_abs_amplitude
            self._real_size = self._max_value - self._min_value
            self._start_value = self._min_value
            self._stop_value = self._max_value

        self.__plots.append(plt)

        self._recalculate_window_coords()
        self._update_step_x()
        self._force_redraw()

    def _redraw(self):
        self._qp.begin(self)
        self._qp.setRenderHint(QPainter.RenderHint.Antialiasing)
        self._draw_grid(self.__take_picture)

        path = QPainterPath(QPointF(self.x() + self._MIN_X, self.y() + self.height() / 2))
        path.addEllipse(QPointF(self.width() / 2, self.height() / 2), self.width() // 2, self.height() // 2)
        self._qp.setClipPath(path)
        self.__redraw_plots()
        if self.__scanner_line.visible and self.__scanner_line.rotate:
            self.__scanner_line.angle += 2 * pi / 720
            if self.__scanner_line.angle >= 2 * pi:
                self.__scanner_line.angle = 0
            self._force_redraw()
        self._qp.end()

    def _recalculate_window_coords(self) -> None:
        """Пересчёт массивов оконных координат графиков"""
        super()._recalculate_window_coords()
        try:
            for plt in self.__plots:
                self.__recalculate_plot_coords(plt)
        except:
            pass

    def __recalculate_plot_coords(self, plt: PolarPlot):
        step = 1 if plt.accurate else max(1, int((1 + len(plt.X)) / self.__MAX_POINTS))
        self.__recalculate_window_xy(plt, step)

    def mousePressEvent(self, a0):
        if a0.button() == Qt.MouseButton.LeftButton:
            self.__left_button_pressed = True

    def mouseReleaseEvent(self, a0):
        if a0.button() == Qt.MouseButton.LeftButton:
            self.__left_button_pressed = False

    def mouseMoveEvent(self, a0):
        line = self.__scanner_line
        if line.visible:
            if self.__left_button_pressed:
                if line.selected:
                    dx = a0.pos().x() - self.width() / 2
                    dy = a0.pos().y() - self.height() / 2
                    line.angle = atan2(-dy, dx)
                    self._force_redraw()
            else:
                d = self.__distance_from_point_to_line(a0.pos(), line.line)
                sel = d <= 10
                if line.selected != sel:
                    self._force_redraw()
                line.selected = sel

    def contextMenuEvent(self, a0):
        self.__menu.exec(a0.globalPos())

    @Slot(bool)
    def __start_scanner_rotation(self, val: bool):
        self.__scanner_line.rotate = val
        self._force_redraw()

    @Slot(bool)
    def __show_scanner(self, val: bool):
        self.__scanner_line.visible = val
        if val:
            self.__scanner_line.angle = np.random.uniform(-pi, pi)
        self._force_redraw()

    def __create_value_pointer(self, angle, plt: PolarPlot):
        if len(plt.Y) <= 1:
            return None
        nearest = plt.get_nearest(angle)

        res: tuple[ValueRectangle] = tuple()
        for _, i in nearest:
            y = plt.Y[i]
            x = plt.X[i]
            ywin = max(self._real_to_window_y(y), self._MIN_Y)
            ywin = min(ywin, self._MAX_Y)
            xwin = self._real_to_window_x(x)

            if len(nearest) > 1 and (y > self._stop_value or y < self._start_value):
                continue

            digits_count = get_digit_count_after_dot(self._step_grid) + 1
            if self._step_grid <= 1.0:
                digits_count = max(3, digits_count)

            tmp_str = round_value(plt.radiuses[i], digits_count)

            text_width = QFontMetrics(VALUE_FONT).horizontalAdvance(tmp_str)

            yrect = ywin
            wrect = text_width + 10
            if xwin < self.width() / 2:
                xrect = xwin + 10
            else:
                xrect = xwin - wrect - 10
            hrect = 18

            add = True
            new_point = QPointF(xwin, ywin)
            for rect in res:
                if abs(rect.point.x() - new_point.x()) < 1e-10 and abs(rect.point.y() - new_point.y()) < 1e-10:
                    add = False
                    break
            if add:
                res += ValueRectangle(xrect, yrect, wrect, hrect, tmp_str, plt.pen.color(), new_point, xwin > self.width() / 2),
            if len(res) > 4:
                break
        return res

    @staticmethod
    def __distance_from_point_to_line(point: QPointF, line: QLineF) -> float:
        # Get the coordinates of the point
        x0, y0 = point.x(), point.y()

        # Get the start and end points of the line
        p1 = line.p1()
        p2 = line.p2()

        # Calculate the coefficients A, B, C for the line equation Ax + By + C = 0
        # A = y2 - y1
        # B = x1 - x2
        # C = -A*x1 - B*y1
        A = p2.y() - p1.y()
        B = p1.x() - p2.x()
        C = -A * p1.x() - B * p1.y()

        # Calculate the distance using the formula
        numerator = abs(A * x0 + B * y0 + C)
        denominator = sqrt(A**2 + B**2)

        # Handle the case of a zero-length line (or vertical/horizontal lines where
        # denominator might be very close to zero due to floating point inaccuracies)
        if denominator == 0:
            return 0.0  # Or handle as an error, depending on requirements

        return numerator / denominator

    def mouseDoubleClickEvent(self, a0):
        if a0.button() == Qt.MouseButton.LeftButton:
            pass
        elif a0.button() == Qt.MouseButton.RightButton:
            self.__scanner_line.visible = False
            self._force_redraw()

    def __draw_scanner_lines(self, value_rects: list[ValueRectangle]):
        line = self.__scanner_line
        if not line.visible:
            return
        p0 = QPointF(self._real_polar_to_window_x(self._min_value, line.angle),
                    self._real_polar_to_window_y(self._min_value, line.angle))
        p1 = QPointF(self._real_polar_to_window_x(self._max_value, line.angle),
                        self._real_polar_to_window_y(self._max_value, line.angle))
        self._qp.setPen(QColor(0x66BD6C) if line.selected else QColor(0))
        self._qp.drawLine(p0, p1)
        line.line = QLineF(p0, p1)

        font = QFont("Consolas, Courier New", 10)
        metrics = QFontMetrics(font)
        angle = self.__win_to_real_angle(line.angle)
        self._draw_angle_text(f"{round(degrees(angle), 1)}°", metrics, self.width() / 2 - 5, line.angle, draw_rect=True)

        for rect in value_rects:
            self._qp.setPen(QColor(255, 255, 255, 127))
            self._qp.setBrush(rect.color)
            self._qp.drawRoundedRect(rect, 5, 5)
            self._qp.setPen(QColor(255, 255, 255))
            self._qp.setFont(VALUE_FONT)
            self._qp.drawText(rect, Qt.AlignmentFlag.AlignCenter, rect.text)
            
            self._qp.setPen(QPen(rect.color, 10, Qt.PenStyle.DashLine, Qt.PenCapStyle.RoundCap))
            self._qp.drawPoint(rect.point)

    def __recalculate_window_xy(self, plt: PolarPlot, step):
        Xwin = self.__recalculate_plot_x(plt, step)
        Ywin = self.__recalculate_plot_y(plt, step)
        
        length = len(plt.X)
        if length == 0:
            return

        if plt.draw_line and plt.pen.style() == Qt.PenStyle.SolidLine:
            plt.lines = [QLineF(Xwin[i - 1], Ywin[i - 1], Xwin[i], Ywin[i]) for i in range(1, len(Xwin))]
        if plt.draw_markers or plt.pen.style() != Qt.PenStyle.SolidLine:
            plt.points = [QPointF(x, y) for x, y in zip(Xwin, Ywin)]

    def __recalculate_plot_x(self, plt: PolarPlot, step):
        return c_recalculate_window_x(list(plt.X), self._MIN_X, self._get_width(), self._real_size, self._start_value, 0, len(plt.Y), step)
    
    def __recalculate_plot_y(self, plt: PolarPlot, step):
        return c_recalculate_window_y(list(plt.Y), self._MIN_Y, self._get_heignt(), self._real_size, self._stop_value, 0, len(plt.Y), step)
    
    def __win_to_real_angle(self, angle: float) -> float:
        if angle < 0:
            return 3 * pi - (abs(angle) + pi)
        else:
            return angle

    def __redraw_plots(self):
        value_rects: list[ValueRectangle] = list()
        for plt in self.__plots:
            if plt.draw_line:
                self._qp.setPen(QPen(plt.pen.color(), 2.0))
                self._qp.drawLines(plt.lines)
            if plt.draw_markers:
                self._qp.setPen(QPen(plt.pen.color(), 5, Qt.PenStyle.DashLine, Qt.PenCapStyle.RoundCap))
                self._qp.drawPoints(plt.points)

            line = self.__scanner_line
            if line.visible:
                rects = self.__create_value_pointer(self.__win_to_real_angle(line.angle), plt)
                if rects:
                    for rect in rects:
                        value_rects.append(rect)

        for i_fixed in range(len(value_rects)):
            for i_mobile in range(i_fixed + 1, len(value_rects)):
                if not value_rects[i_mobile].intersects(value_rects[i_fixed]):
                    continue
                if value_rects[i_mobile].move_left:
                    value_rects[i_mobile].moveLeft(value_rects[i_fixed].x() - value_rects[i_mobile].width() - 5)
                else:
                    value_rects[i_mobile].moveLeft(value_rects[i_mobile].x() + value_rects[i_fixed].width() + 5)
        self.__draw_scanner_lines(value_rects)

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
