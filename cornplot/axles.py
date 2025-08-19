import os, time, warnings
from math import log10, floor, ceil, pow

from PyQt6.QtCore import Qt, QLineF, QRectF, pyqtSlot, QRect, QTimer
from PyQt6.QtGui import QPen, QColor, QPainter, QFont, QFontMetrics 
from PyQt6.QtWidgets import QFrame, QFileDialog

from .utils import convert_timestamp_to_human_time, round_custom, arange, set_cursor_shape, set_default_cursor

from .button_group import ButtonGroup
from .axle_slider import AxleSlider
from .action_buffer import ActionBuffer
from .array_utils import *
from .axle_group_data import AxleGroupData, MAX_SCANNER_LINES


axle_groups: dict[str, AxleGroupData] = dict()


class Axles(QFrame):
    _OFFSET_Y_UP = 22             # смещение по У для размещения шапки
    _OFFSET_Y_DOWN = 25
    _OFFSET_X = 100
    _Y_STOP_RATIO = 20

    def __init__(self, widget, x: int, y: int, w: int, h: int):
        super().__init__()

        self.setParent(widget)
        self.__group = AxleGroupData()
        self.__scale_lines = self.__group.scale_lines
        self.__scanner_lines = self.__group.scanner_lines

        self.__slider = AxleSlider()
        self.__action_buffer = ActionBuffer()

        self.__x = int(x)
        self.__y = int(y)
        self.__h = int(h)
        self.__w = int(w)

        self._MIN_X = self._OFFSET_X
        self._MAX_X = self._MIN_X + self.__w
        self._MIN_Y = self._OFFSET_Y_UP
        self._MAX_Y = self._MIN_Y + self.__h

        self.__MAXIMUM_X_WIDTH = -1

        self.__x_name = "X"
        self.__y_name = "Y"  # имя оси У
        self.__Y_STOP_COEFF = 1  # увеличение максимума У

        self.__x_label_width = 100
        self.__x_met_width = 50
        self.__y_label_high = 20

        self._xstart = 0
        self._xstop = 10
        self._x_axis_min = 0
        self._x_axis_max = 10
        self._real_width = self._xstop - self._xstart  # длина оси Х в реальных единицах
        self.__step_grid_x = self._real_width / 2

        self.__group.x_start = self._xstart
        self.__group.x_stop = self._xstop

        self._ystart = 0
        self._ystop = 1
        self._y_axis_min = 0
        self._y_axis_max = 1
        self._real_height = self._ystop - self._ystart  # длина оси У в реальных единицах
        self.__step_grid_y = self._real_height / 2

        self.__scaling_rect = QRectF(0, 0, 0, 0)

        # флаги
        self.__convert_to_hhmmss = False    # конвертировать ли значения Х в ЧЧ:ММ:СС
        self.__animated = False
        self.__x_auto_scale = True
        self.__y_auto_scale = True
        self._visible = True
        self.__draw_major_grid = True
        self.__draw_minor_grid = False
        self.__draw_x = True                  # отображать ли подписи оси Х
        self.__draw_y = True
        self.__draw_origin = False
        self._y_scaled = False
        self.__left_button_pressed = False
        self.__scaling_rect_drawing = False
        self._redraw_required = True               # в графике что-то поменялось, нужно перерисовать
        self._point_added = False
        self.__paused = False
        self.__zero_y_fixed = False              # ноль по Х всегда виден
        self.__zoom_active = False
        self.__ctrl_pressed = False
        self.__shift_pressed = False
        self.__dark = False
        self.__visible = True
        self._x_logarithmic = False
        self._y_logarithmic = False

        self._pointsToSelect = 0
        self._selectingPointGraph = -1

        # ручки
        self.__pen_grid = QPen(QColor(145, 145, 145), 1)
        self.__pen_grid.setStyle(Qt.PenStyle.DotLine)
        self.__pen_grid_minor = QPen(QColor(145, 145, 145), 0.5)
        self.__pen_grid_minor.setStyle(Qt.PenStyle.DotLine)
        self.__origin_pen = QPen(QColor(0, 0, 0), 0.5)

        self.__minor_step_ratio = 5     # доля от шага основных линий - шаг дополнительных линий

        self.__touch_x = 0
        self.__touch_y = 0

        self.__initial_x = 0
        self.__initial_y = 0

        self.__mouse_on = False

        self.__initial_timestamp = 0

        self._qp = QPainter()

        self.setGeometry(self.__x - self._OFFSET_X, self.__y - self._OFFSET_Y_UP, self.__w + self._OFFSET_X, self.__h + self._OFFSET_Y_UP + self._OFFSET_Y_DOWN)
        self.setMouseTracking(True)
        self.show()

        self.__btn_group = ButtonGroup(self, self.__w, self.__h)
        self.__btn_group.add_vert_button.clicked.connect(self.__add_line)
        self.__btn_group.clear_button.clicked.connect(self.__clear_axles)
        self.__btn_group.zoom_button.clicked.connect(self._zoom_in)
        self.__btn_group.back_button.clicked.connect(self.__cancel_scaling)
        self.__btn_group.set_geometry(self._MIN_X, self._OFFSET_Y_DOWN - self._OFFSET_Y_UP, self.__w, self.__h)
        self.__btn_group.save_button.clicked.connect(self.__save_picture)
        self.__btn_group.more_button.clicked.connect(self._show_extended_window)
        self.__btn_group.pause_button.clicked.connect(lambda: self.pause(not self.__paused))
        self.__btn_group.restart_button.clicked.connect(lambda: self.restart_animation(signal=True))

        self.__Y_STOP_COEFF = 0
        self._value_rect_max_y = self._MAX_Y

        self._update_step_x()
        self._update_step_y()
        self.__recalculate_slider_coords()

        set_default_cursor()

        self.tmr = QTimer(self)
        self.tmr.timeout.connect(self.__timer_callback)
        self.tmr.start(25)

    def paintEvent(self, a0):
        self._qp.begin(self)
        self._redraw()
        self._qp.end()

    def _redraw(self) -> None:
        if not self.__visible:
            return

        if self.__dark:
            self._qp.setPen(QColor(40, 47, 60))
            self._qp.setBrush(QColor(40, 47, 60))
        else:
            self._qp.setPen(QColor(255, 255, 255))
            self._qp.setBrush(QColor(255, 255, 255))
        self._qp.drawRect(self._OFFSET_X, self._OFFSET_Y_UP, self.__w, self.__h)  # поле графика
        
        # оси координат по необходимости
        if self.__draw_origin:
            self._qp.setPen(self.__origin_pen)
            x = self.real_to_window_x(0)
            y = self.real_to_window_y(0)
            if self._MIN_Y <= y <= self._MAX_Y:
                self._qp.drawLine(QLineF(self._MIN_X, y, self._MAX_X, y))
            if self._MIN_X <= x <= self._MAX_X:
                self._qp.drawLine(QLineF(x, self._MIN_Y, x, self._MAX_Y))

        self._draw_grid()
        #self._draw_scanner_lines()
        self._draw_x_slider()

    @pyqtSlot()
    def __timer_callback(self):
        self.__btn_group.process_visibility()
        self.__check_group_x_borders()
        if self._needs_redrawing():
            self.update()

    def set_visible(self, visible: bool) -> None:
        self.setVisible(visible)

    @property
    def visible(self):
        return self.__visible

    def set_geometry(self, x: int, y: int, w: int, h: int) -> None:
        if self.__x != x or self.__y != y or self.__w != w or self.__h != h:
            old_scanner_coords = [line.x() / self.width() for line in self.__scanner_lines]

            if x > 0:
                self.__x = x
            if y > 0:
                self.__y = y
            if w > 0:
                self.__w = w
            if h > 0:
                self.__h = h
            super().setGeometry(self.__x - self._OFFSET_X, self.__y - self._OFFSET_Y_UP, self.__w + self._OFFSET_X, self.__h + self._OFFSET_Y_UP + self._OFFSET_Y_DOWN)

            self._MAX_X = self._MIN_X + self.__w
            self._MAX_Y = self._MIN_Y + self.__h

            self.__btn_group.set_geometry(self._MIN_X, self._OFFSET_Y_DOWN - self._OFFSET_Y_UP, self.__w, self.__h)

            self._update_step_x()
            self._update_step_y()
            self._calculate_y_parameters()
            self._recalculate_window_coords()

            for i, line in enumerate(self.__scanner_lines):
                line.set_x_coord(self.width() * old_scanner_coords[i])

    @pyqtSlot()
    def __add_line(self):
        x0 = round(self.__w * (1 / (MAX_SCANNER_LINES + 1)))
        self.__scanner_lines.add_line(x0 + round(self.__w * (self.__scanner_lines.line_count() / (MAX_SCANNER_LINES + 1))))
        self._force_redraw()
        self.__group.line_move_signal.emit()

    @pyqtSlot()
    def __clear_axles(self):
        for line in self.__scale_lines:
            line.hide()
        for line in self.__scanner_lines:
            line.hide()
        self._force_redraw()

    def _update_x_borders(self, x0, xk):
        self.__group.update_x_borders(x0, xk)

    def set_initial_timestamp(self, ts: int) -> None:
        self.__initial_timestamp = ts

    def get_initial_timestamp(self):
        return self.__initial_timestamp
    
    def is_paused(self) -> bool:
        return self.__paused

    def is_animated(self) -> bool:
        return self.__animated
    
    def _set_animated(self, val: bool) -> None:
        if self.__animated != val:
            self.__btn_group.set_animated(val)
        self.__animated = val
    
    def _needs_redrawing(self) -> bool:
        return self._redraw_required

    def _force_redraw(self) -> None:
        self._redraw_required = True

    def move_to_group(self, grp_name: str):
        if grp_name not in axle_groups:
            axle_groups[grp_name] = AxleGroupData()
            axle_groups[grp_name].x_start = self._xstart
            axle_groups[grp_name].x_stop = self._xstop

        self.__group = axle_groups[grp_name]
        self.__scanner_lines = self.__group.scanner_lines
        self.__scale_lines = self.__group.scale_lines
        self.__group.line_move_signal.connect(self._force_redraw)
        self.__group.pause_signal.connect(self.__pause)
        self.__group.restart_signal.connect(self.__restart_animation)

    def _update_step_x(self) -> None:
        """Установка шага оси Х. Происходит с таким расчётом,
        чтобы на оси было не более 10 меток"""
        if not self.__x_auto_scale:
            return
        try:
            self.__step_grid_x = 10 ** round(log10(self._real_width)) / 10
        except ValueError:
            self.__step_grid_x = 1.0

        if self._real_width / self.__step_grid_x > 10:
            n = 3
            while self._real_width / self.__step_grid_x > 10:
                n += 1
                self.__step_grid_x *= (2.5 if n % 4 == 0 else 2)
        else:
            n = 0
            while self._real_width / self.__step_grid_x < 10:
                n += 1
                self.__step_grid_x /= (2.5 if n % 4 == 0 else 2)

        while self.__step_grid_x / self._real_width * self.__w < self.__x_met_width:
            self.__step_grid_x *= (2.5 if n % 4 == 0 else 2)
            n += 1

        if self.__step_grid_x / self._real_width * self.__w > 150:
            self.__step_grid_x /= (2.5 if n % 4 == 0 else 2)

        if self.__step_grid_x == 0:
            self.__step_grid_x = self._real_width / 1

    def _update_step_y(self) -> None:
        """См. ось Х"""

        if not self.__y_auto_scale:
            return

        if self._ystart == self._ystop:
            self._ystart -= 0.5
            self._ystop += 0.5
            self._real_height = 1

        self.__step_grid_y = 10 ** round(log10(self._real_height)) / 10
        n = 0

        if self._real_height / self.__step_grid_y >= 10:
            n = 3
            while self._real_height / self.__step_grid_y >= 10:
                n += 1
                self.__step_grid_y *= (2.5 if n % 4 == 0 else 2)

        elif self._real_height / self.__step_grid_y < 8:
            while self._real_height / self.__step_grid_y <= 10:
                n += 1
                self.__step_grid_y /= (2.5 if n % 4 == 0 else 2)

        while self.__step_grid_y / self._real_height * self.__h < 25:  # высота не менее 30 пикселей
            n += 1
            self.__step_grid_y *= (2.5 if n % 4 == 0 else 2)

        if self.__step_grid_y / self._real_height * self.__h > 100:
            self.__step_grid_y /= (2.5 if n % 4 == 0 else 2)

    def _is_animated(self) -> bool:
        return self.__animated

    def set_x_name(self, name: str) -> None:
        if name == self.__x_name:
            return
        self.__x_name = name
        self._force_redraw()

    def set_y_name(self, name: str) -> None:
        if self.__y_name == name:
            return
        self.__y_name = name
        self._force_redraw()

    def leaveEvent(self, a0):
        self.clearFocus()
        self.__mouse_on = False
        self.__ctrl_pressed = False
        self.__shift_pressed = False
        self.__left_button_pressed = False
        self.__right_button_pressed = False
        self.__slider.set_mouse_on(False)
        self.__deselect_all_lines()
        # set_cursor_shape(Qt.CursorShape.ArrowCursor)

    def enterEvent(self, a0):
        self.setFocus()
        self.__mouse_on = True

    @pyqtSlot()
    def _zoom_in(self):
        if self.__scale_lines.line_count() < 2:
            return
        if self.__animated and not self.__paused:
            return
        # увеличиваем график между двуми вертикальными линиями
        line_coords = [line.x() for line in self.__scale_lines]
        x0 = self.window_to_real_x(min(line_coords))
        x1 = self.window_to_real_x(max(line_coords))

        if x1 - x0 > 0.02 * self._real_width:
            self.__action_buffer.add_action(self._xstart, self._xstop, self._ystart, self._ystop)
            self._set_x_start(x0)
            self._set_x_stop(x1)
            self._update_step_x()
            self._calculate_y_parameters()
            self._update_step_y()
            self._recalculate_window_coords()
            self.__group.update_x_borders(self._xstart, self._xstop)
            self._force_redraw()

        self.__delete_scale_lines()
        set_default_cursor()
        
    def _zoom_out(self):
        x_center = self.window_to_real_x(round(self._MAX_X / 2))
        self.__action_buffer.add_action(self._xstart, self._xstop, self._ystart, self._ystop)
        if self.__MAXIMUM_X_WIDTH == -1:
            self._set_x_start(self._x_axis_min)
            self._set_x_stop(self._x_axis_max)
        else:
            self._set_x_start(max(self._x_axis_min, round(x_center - self.__MAXIMUM_X_WIDTH / 2)))
            self._set_x_stop(min(self._x_axis_max, round(x_center + self.__MAXIMUM_X_WIDTH / 2)))
        self._update_step_x()
        self._y_scaled = False
        self._set_y_start(self._y_axis_min)
        self._set_y_stop(self._y_axis_max)
        self._update_step_y()
        self.__delete_scale_lines()
        self._calculate_y_parameters()
        self._recalculate_window_coords()
        self.__group.update_x_borders(self._xstart, self._xstop)
        self._force_redraw()

    def __check_group_x_borders(self):
        if self._xstart != self.__group.x_start or self._xstop != self.__group.x_stop:
            if self._x_logarithmic:
                self._set_x_start(self.__group.x_start if self.__group.x_start > 0 else 0.01)
                self._set_x_stop(self.__group.x_stop)
            else:
                self._set_x_start(self.__group.x_start)
                self._set_x_stop(self.__group.x_stop)
            self._recalculate_window_coords()
            self._update_step_x()
            self._force_redraw()

    def __delete_scanner_lines(self):
        for line in self.__scanner_lines:
            line.hide()
            line.select(False)

    def __delete_scale_lines(self):
        for line in self.__scale_lines:
            line.hide()
            line.select(False)

    def __deselect_all_lines(self):
        for line in self.__scanner_lines:
            line.select(False)
        for line in self.__scale_lines:
            line.select(False)

    def _set_x_stop(self, xmax: float) -> None:
        """Установка максимального отображаемого значения Х"""
        if self.__MAXIMUM_X_WIDTH == -1 or xmax - self._xstart <= self.__MAXIMUM_X_WIDTH:
            self._xstop = xmax
            self._real_width = self._xstop - self._xstart
        else:
            self._xstop = self._xstart + self.__MAXIMUM_X_WIDTH
            self._real_width = self.__MAXIMUM_X_WIDTH

    def _set_x_start(self, xmin: float) -> None:
        """Установка минимального отображаемого значения Х"""
        self._xstart = xmin
        self._real_width = self._xstop - self._xstart

    def _set_y_stop(self, ymax: float) -> None:
        """Установка максимального отображаемого значения У"""
        self._ystop = ymax
        self._real_height = self._ystop - self._ystart

    def _set_y_start(self, ymin: float) -> None:
        """Установка минимального отображаемого значения У"""
        self._ystart = ymin
        self._real_height = self._ystop - self._ystart

    def _reset_y_axle(self) -> None:
        self._ystart = self._y_axis_min
        self._ystop = self._y_axis_max
        self._real_height = abs(self._ystop - self._ystart)

    def __move_slider(self, mouse_x):
        self.__slider.x += (mouse_x - self.__slider.x0)

        slider_width = self.__w * self.__slider.length

        x0 = self._MIN_X + (1 - self.__slider.length - 0.01) * self.__w
        x1 = x0 + slider_width

        if self.__slider.x < x0:
            self.__slider.x = x0
        if self.__slider.x + self.__slider.w > x1:
            self.__slider.x = x1 - self.__slider.w

        self.__slider.x0 = mouse_x

        x_len = self._x_axis_max - self._x_axis_min

        x_start = x_len * (self.__slider.x - x0) / slider_width + self._x_axis_min
        x_stop = x_len * (self.__slider.x - x0 + self.__slider.w) / slider_width + self._x_axis_min

        self._set_x_start(x_start)
        self._set_x_stop(x_stop)
        self._recalculate_window_coords()
        self.__group.update_x_borders(x_start, x_stop)

    @pyqtSlot()
    def __cancel_scaling(self):
        action = self.__action_buffer.get_last_action()
        if action is False:
            return
        xstart, xstop, ystart, ystop = action
        self._set_x_start(xstart)
        self._set_x_stop(xstop)
        self._set_y_start(ystart)
        self._set_y_stop(ystop)
        self._update_step_x()
        self._update_step_y()
        self.__group.update_x_borders(xstart, xstop)
        self._calculate_y_parameters()
        self._recalculate_window_coords()
        self._force_redraw()

    def mouseMoveEvent(self, a0):
        pos = a0.pos()
        if pos.y() < self._MIN_Y and not self.__zoom_active:
            set_default_cursor()
            self.__slider.release()
        
        pos_x = pos.x() - self._MIN_X

        if self.__slider.mouse_on():
            self.__deselect_all_lines()
            self._force_redraw()
        
            # обработка слайдера
            if self.__slider.is_pressed() and (self._xstart != self._x_axis_min or self._xstop != self._x_axis_max):
                self.__move_slider(pos.x() + self._MIN_X)
        else:
            self.__slider.release()
        
            if not self.__left_button_pressed and not self.__slider.is_pressed() and not self.__zoom_active:
                for line in self.__scanner_lines:
                    if line.is_visible():
                        old_val = line.is_selected()
                        line.select(abs(pos_x - line.x()) < 15)
                        if old_val != line.is_selected():
                            self._force_redraw()
                            self.__group.line_move_signal.emit()

                if self.__scanner_lines.any_selected():
                    for line in self.__scale_lines:
                        line.select(False)
                else:
                    for line in self.__scale_lines:
                        old_val = line.is_selected()
                        line.select(abs(pos_x - line.x()) < 15)
                        if old_val != line.is_selected():
                            self._force_redraw()
                            self.__group.line_move_signal.emit()

        if self.__left_button_pressed:
            if self.__mouse_on and self.__ctrl_pressed:
                if self.__animated and not self.__paused:
                    return

                # движение графика при нажатой клавише ctrl
                tmpX = self.window_to_real_x(self.__initial_x) - self.window_to_real_x(pos.x())
                self._xstart = max(min(tmpX, self._x_axis_max - self._real_width), self._x_axis_min)
                self._xstop = self._xstart + self._real_width

                tmpY = self.__initial_y - self.window_to_real_y(pos.y())
                self._ystart += tmpY
                min_possible_y = (0 if self.__zero_y_fixed and self._y_axis_min >= 0
                                    else self._y_axis_min - self.__Y_STOP_COEFF)
                max_possible_y = self._y_axis_max + (0 if (self.__zero_y_fixed and self._y_axis_max <= 0)
                                                        else self.__Y_STOP_COEFF)
                if self._ystart < min_possible_y:
                    self._ystart = min_possible_y
                if self._ystart + self._real_height > max_possible_y:
                    self._ystart = max_possible_y - self._real_height
                self._ystop = self._ystart + self._real_height

                self._calculate_y_parameters()
                self._recalculate_window_coords()
                self.__group.update_x_borders(self._xstart, self._xstop)

                self._force_redraw()

            # движение линий сканеров
            if self.__scanner_lines.nearest_line != -1:
                self.__scanner_lines[self.__scanner_lines.nearest_line].set_x_coord(min(max(pos_x, 2), self.__w - 1))
                self.__scanner_lines.last_line = self.__scanner_lines.nearest_line
                self._force_redraw()
                self.__group.line_move_signal.emit()

            # движение масштабирующих линий
            if self.__scale_lines.nearest_line != -1 and self.__scanner_lines.nearest_line == -1:
                self.__scale_lines[self.__scale_lines.nearest_line].set_x_coord(min(max(pos_x, 1), self.__w - 1))
                self._force_redraw()
                self.__group.line_move_signal.emit()

            # определение координат масштабирующего прямоугольника
            if self.__scaling_rect_drawing:
                if self.__animated and not self.__paused:
                    return
                self.__scaling_rect.setRight(min(max(pos_x, 0), self.__w))
                self.__scaling_rect.setBottom(min(max(pos.y() - self._MIN_Y, 0), self.__h))
                self._force_redraw()
        else:
            self.__slider.set_mouse_on(self.__slider.x <= pos.x() <= self.__slider.x + self.__slider.w and 
                                    self.__slider.y <= pos.y() <= self.__slider.y + self.__slider.h)

    def mousePressEvent(self, a0):
        if not self.__mouse_on:
            return
        
        pos = a0.pos()
        
        if pos.y() < self._OFFSET_Y_UP:
            return
        
        self.__initial_x = pos.x() + self._MIN_X - self.real_to_window_x(self._x_axis_min if self._x_logarithmic else 0)
        # расстояние от точки касания до осей в пикселях
        self.__initial_y = self.window_to_real_y(pos.y())

        self.__touch_x = pos.x()
        self.__touch_y = pos.y()

        match a0.button():
            case Qt.MouseButton.LeftButton:
                self.__left_button_pressed = True
                if not self.__scanner_lines.any_selected() and not self.__scale_lines.any_selected():
                    if self.__animated and not self.__paused:
                        return
                    if self.__slider.mouse_on():
                        self.__slider.press()
                        self.__slider.set_initial_x(pos.x() + self._OFFSET_X)
                        self._force_redraw()
                        return
                    
                    if self.__shift_pressed:
                        self.__scaling_rect_drawing = True

                    pos_x = pos.x() - self._MIN_X
                    pos_y = pos.y() - self._MIN_Y
                    self.__scaling_rect.setCoords(pos_x, pos_y, pos_x, pos_y)
                else:
                    for i, line in enumerate(self.__scanner_lines):
                        if line.is_selected():
                            self.__scanner_lines.nearest_line = i
                            break
                    for i, line in enumerate(self.__scale_lines):
                        if line.is_selected():
                            self.__scale_lines.nearest_line = i
                            break
                    self._force_redraw()
            case Qt.MouseButton.XButton1:
                self.__cancel_scaling()

    def mouseReleaseEvent(self, a0):
        pos = a0.pos()

        if pos.y() < self._OFFSET_Y_UP and not self.__zoom_active:
            return
        
        match a0.button():
            case Qt.MouseButton.LeftButton:
                self.__left_button_pressed = False
                self.__scaling_rect_drawing = False

                if self.__slider.is_pressed():
                    self.__slider.release()
                    return

                self.__scanner_lines.nearest_line = -1
                self.__scale_lines.nearest_line = -1
                if self.__animated and not self.__paused or self.__scale_lines.any_selected() or self.__scanner_lines.any_selected():
                    return
                else:
                    if self.__scaling_rect.width() == 0 and self.__scaling_rect.height() == 0 and not self.__zoom_active:
                        if self.__touch_x == pos.x() and self.__touch_y == pos.y() and not self._point_added:
                            self.__scale_lines.add_line(pos.x() - self._OFFSET_X)
                            self.__group.line_move_signal.emit()
                    else:
                        if abs(self.__scaling_rect.width()) > 10 and abs(self.__scaling_rect.height()) > 10:
                            x0 = self.window_to_real_x(min(self.__scaling_rect.left(), self.__scaling_rect.right()))
                            x1 = self.window_to_real_x(max(self.__scaling_rect.left(), self.__scaling_rect.right()))
                            y0 = self.window_to_real_y(max(self.__scaling_rect.top(), self.__scaling_rect.bottom()) + self._OFFSET_Y_UP)
                            y1 = self.window_to_real_y(min(self.__scaling_rect.top(), self.__scaling_rect.bottom()) + self._OFFSET_Y_UP)
                            self.__action_buffer.add_action(self._xstart, self._xstop, self._ystart, self._ystop)
                            self._set_x_start(x0)
                            self._set_x_stop(x1)
                            self._set_y_start(y0)
                            self._set_y_stop(y1)
                            self._update_step_y()
                            self._update_step_x()
                            self.__group.update_x_borders(x0, x1)
                            self._recalculate_window_coords()
                            self._y_scaled = True
                            self._force_redraw()

                self.__zoom_active = False
                self.__scaling_rect.setCoords(0, 0, 0, 0)
                self.__scaling_rect_drawing = False
                self._force_redraw()

                if self._point_added:
                    self._point_added = False

    def _recalculate_window_coords(self):
        self.__recalculate_slider_coords()

    def _calculate_x_parameters(self):
        pass

    def _calculate_y_parameters(self):
        pass

    def __save_picture(self):
        if self.__animated:
            self.pause(True)
        self.__btn_group.set_buttons_visible(False)
        grab = self.grab(QRect(0, 0, self.width() + 10, self.height()))
        fileName, _ = QFileDialog.getSaveFileName(self, "Сохранить картинку", "",
                                                            "PNG Files (*.png)")
        if len(fileName) > 0:
            grab.save(fileName, 'png')
            os.startfile(fileName)
        self.__btn_group.set_buttons_visible(True)
        if self.__animated:
            self.pause(False)

    def mouseDoubleClickEvent(self, a0):
        set
        if a0.pos().y() < self._OFFSET_Y_UP or self.__slider.is_pressed():
            return
        match a0.button():
            case Qt.MouseButton.RightButton:
                if a0.pos().y() < self._OFFSET_Y_UP or (self.__animated and not self.__paused):
                    return
                # возвращаем исходный масштаб
                self._zoom_out()
                self.__group.line_move_signal.emit()

            case Qt.MouseButton.MiddleButton:
                self.__delete_scanner_lines()
                self._force_redraw()
                self.__group.line_move_signal.emit()
    
    def keyPressEvent(self, a0):
        match a0.key():
            case Qt.Key.Key_Shift:
                if not self.__slider.mouse_on():
                    self.__shift_pressed = True
                    set_cursor_shape(Qt.CursorShape.CrossCursor)
                self.__ctrl_pressed = False
            case Qt.Key.Key_Control:
                if not self.__slider.mouse_on():
                    self.__ctrl_pressed = True
                    set_cursor_shape(Qt.CursorShape.SizeAllCursor)
                self.__shift_pressed = False
            case Qt.Key.Key_Plus:
                if self.__scale_lines.line_count() == 2:
                    self._zoom_in()
            case Qt.Key.Key_Minus:
                self._zoom_out()

    def wheelEvent(self, a0):
        delta = a0.angleDelta().y()

        d = self._real_width * 0.05 * abs(delta / 120)
        w = self._real_width
        if delta > 0:
            self._set_x_stop(min(self._x_axis_max, self._xstop + d))
            self._set_x_start(self._xstop - w)
        elif delta < 0:
            self._set_x_start(max(self._x_axis_min, self._xstart - d))
            self._set_x_stop(self._xstart + w)
        self.__group.update_x_borders(self._xstart, self._xstop)
        self._recalculate_window_coords()
        self._force_redraw()

    def keyReleaseEvent(self, a0):
        match a0.key():
            case Qt.Key.Key_Shift:
                self.__scaling_rect_drawing = False
                self.__shift_pressed = False
                set_default_cursor()
            case Qt.Key.Key_Control:
                self.__ctrl_pressed = False
                set_default_cursor()

    def real_to_window_x(self, x: float) -> float:
        """Перевод реальных координат оси х в оконные"""
        return c_real_to_window_x(x, self._MIN_X, self.__w, self._real_width, self._xstart) # type: ignore
    
    def __real_to_window_x_linear(self, x: float) -> float:
        return c_real_to_window_x(x, self._MIN_X, self.__w, self._real_width, self._xstart) # type: ignore
    
    def __real_to_window_x_log(self, x: float) -> float:
        if x <= 0:
            return self._MIN_X
        return c_real_to_window_x(log10(x), self._MIN_X, self.__w, log10(self._xstop / self._xstart), log10(self._xstart)) # type: ignore

    def real_to_window_y(self, y: float) -> int:
        """Перевод реальных координат оси у в оконные"""
        return c_real_to_window_y(y, self._MIN_Y, self.__h, self._real_height, self._ystop) # type: ignore
    
    def __real_to_window_y_linear(self, y: float) -> int:
        return c_real_to_window_y(y, self._MIN_Y, self.__h, self._real_height, self._ystop) # type: ignore
    
    def __real_to_window_y_log(self, y: float) -> int:
        if y <= 0:
            return self._MAX_Y
        return c_real_to_window_y(log10(y), self._MIN_Y, self.__h, log10(self._ystop / self._ystart), log10(self._ystop)) # type: ignore

    def window_to_real_x(self, x: float) -> float:
        """Перевод оконных координат оси х в реальные"""
        return c_window_to_real_x(x, self.__w, self._real_width, self._xstart) # type: ignore
    
    def __window_to_real_x_linear(self, x: float) -> float:
        return c_window_to_real_x(x, self.__w, self._real_width, self._xstart) # type: ignore
    
    def __window_to_real_x_log(self, x: float) -> float:
        return pow(10, c_window_to_real_x(x, self.__w, log10(self._xstop / self._xstart), log10(self._xstart))) # type: ignore

    def window_to_real_y(self, y: float) -> float:
        return c_window_to_real_y(y, self.__h, self._real_height, self._ystop, self._OFFSET_Y_UP) # type: ignore
    
    def __window_to_real_y_linear(self, y: float) -> float:
        return c_window_to_real_y(y, self.__h, self._real_height, self._ystop, self._OFFSET_Y_UP) # type: ignore
    
    def __window_to_real_y_log(self, y: float) -> float:
        return pow(10, c_window_to_real_y(y, self.__h, log10(self._xstop / self._xstart), log10(self._ystop), self._OFFSET_Y_UP)) # type: ignore
    
    def __recalculate_slider_coords(self):
        if self.__slider.is_pressed():
            return

        x0 = self._MIN_X + int((1 - self.__slider.length - 0.01) * self.__w)

        x_axis_length = self._x_axis_max - self._x_axis_min
        if x_axis_length == 0:
            return
        x01 = x0 + int(self.__w * self.__slider.length * (self._xstart - self._x_axis_min) / x_axis_length)
        x11 = x0 + int(self.__w * self.__slider.length * (self._xstop - self._x_axis_min) / x_axis_length)
        self.__slider.x = x01
        self.__slider.y = self._MIN_Y + 5
        self.__slider.w = max(4, x11 - x01)
        self.__slider.h = 12

    def _draw_grid(self):
        major = list()
        minor = list()

        self.__draw_grid_x(major, minor)
        self.__draw_grid_y(major, minor)      

        self._qp.setPen(self.__pen_grid)
        self._qp.drawLines(major)
        self._qp.setPen(self.__pen_grid_minor)
        self._qp.drawLines(minor)

    def __draw_grid_x(self, major_lines, minor_lines):
        font = QFont('bahnschrift', 11)
        font.setBold(True)
        self._qp.setFont(font)

        txt_pen = QPen(QColor(210, 210, 210)) if self.__dark else QPen(QColor(0, 0, 0))
        self._qp.setPen(txt_pen)

        self.__x_label_width = QFontMetrics(font).horizontalAdvance(self.__x_name)
          
        if self.__draw_x:
            self._qp.drawText(self._MAX_X - 500, self._MAX_Y + 3, 500, 20,
                              Qt.AlignmentFlag.AlignRight, self.__x_name)  # имя оси Х
        
        font.setBold(False)
        self._qp.setFont(font)
        
        # формируем метки по оси Х
        x0 = round_custom(self._xstart, self.__step_grid_x)
        xk = min(self._x_axis_max, self._xstop)

        if self._x_logarithmic:
            if x0 <= 0:
                x0 += self.__step_grid_x
            initial_x_power = floor(log10(self._xstart))
            end_x_power = ceil(log10(self._xstop))
            x_metki_coords = [10 ** i for i in range(initial_x_power, end_x_power + 1)]
        else:
            x_metki_coords = arange(x0, xk + self.__step_grid_x, self.__step_grid_x)
        tmp_x_met = self.__x_met_width
        self.__x_met_width = 0
        
        for x in x_metki_coords:
            if self._x_logarithmic:
                log_width = log10(self._xstop) - log10(self._xstart)
                x_w = self.__w / log_width * (log10(x) - log10(self._xstart)) + self._MIN_X
            else:
                x_w = self.real_to_window_x(x)  # оконная координата метки
            
            if self._MIN_X < x_w < self._MAX_X:
                if not (x == 0 and self.__draw_origin) and self.__draw_major_grid:
                    major_lines.append(QLineF(x_w, self._MAX_Y, x_w, self._MIN_Y))

                if self.__draw_x:
                    # подписи осей
                    self._qp.setPen(txt_pen)
                    if self.__convert_to_hhmmss and self._x_axis_min >= 0:
                        tmp_str = convert_timestamp_to_human_time(x + self.__initial_timestamp, self.__step_grid_x < 1)
                    else:
                        if self.__step_grid_x < 0.001:
                            tmp_str = f"{x:.3e}"
                        elif self.__step_grid_x < 0.01:
                            tmp_str = f"{x:.4f}"
                            if tmp_str[-1] == '0':
                                tmp_str = tmp_str[:-1]
                        elif self.__step_grid_x < 2.5:
                            tmp_str = f"{x:.2f}"
                        elif self.__step_grid_x < 25:
                            tmp_str = f"{x:.1f}"
                        elif self.__step_grid_x > 9999:
                            tmp_str = f"{x:.2E}"
                        else:
                            tmp_str = f"{round(x)}"

                    tmp_str_width = QFontMetrics(font).horizontalAdvance(tmp_str)
                    if tmp_str_width > self.__x_met_width:
                        self.__x_met_width = tmp_str_width

                    if self._MIN_X + 30 < x_w < self._MAX_X - self.__x_label_width - tmp_str_width:
                        self._qp.drawText(QRectF(x_w - (tmp_str_width >> 1), self._MAX_Y + 1, tmp_str_width, 20),
                                          Qt.AlignmentFlag.AlignCenter, tmp_str)

            if self._x_logarithmic:
                x0_minor = 2 * x
                xk_minor = 10 * x
                xstep_minor = x
            elif self.__draw_minor_grid:  # побочная сетка
                x0_minor = x + self.__step_grid_x / self.__minor_step_ratio
                xk_minor = x + self.__step_grid_x
                xstep_minor = self.__step_grid_x / self.__minor_step_ratio
            else:
                continue
            x_min = arange(x0_minor, xk_minor + xstep_minor / 2, xstep_minor)
            x_minor = [self.real_to_window_x(x_m) for x_m in x_min]
            for x_m in x_minor:
                if self._MIN_X < x_m < self._MAX_X and x_w != x_m:
                    minor_lines.append(QLineF(x_m, self._MAX_Y, x_m, self._MIN_Y))
        if tmp_x_met != self.__x_met_width:
            self._update_step_x()

        return major_lines, minor_lines

    def __draw_grid_y(self, major_lines, minor_lines):
        font = QFont('bahnschrift', 11)
        font.setBold(True)
        self._qp.setFont(font)
        self.__y_label_high = QFontMetrics(font).height()

        txt_pen = QPen(QColor(210, 210, 210)) if self.__dark else QPen(QColor(0, 0, 0))
        self._qp.setPen(txt_pen)

        if self.__draw_y:
            self._qp.drawText(self._MIN_X - 110, self._MIN_Y, 100, self.__y_label_high,
                            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, self.__y_name)  # имя оси У
        
        font.setBold(False)
        self._qp.setFont(font)

        y0 = round_custom(self._ystart, self.__step_grid_y)
        y_metki_coords = arange(y0, self._ystop + self.__step_grid_y, self.__step_grid_y)

        if self._y_logarithmic:
            if y0 <= 0:
                y0 += self.__step_grid_y
            initial_y_power = floor(log10(self._ystart))
            end_y_power = ceil(log10(self._ystop))
            y_metki_coords = [10 ** i for i in range(initial_y_power, end_y_power + 1)]
        else:
            y_metki_coords = arange(y0, self._ystop + self.__step_grid_y, self.__step_grid_y)

        first = True

        for y in y_metki_coords:
            y_w = self.real_to_window_y(y)

            if self._y_logarithmic:
                self.__step_grid_y = y

            if self._MIN_Y < y_w < self._MAX_Y:
                if not (y == 0 and self.__draw_origin) and self.__draw_major_grid:
                    major_lines.append(QLineF(self._MIN_X, y_w, self._MAX_X, y_w))
                if self.__draw_y:
                    self._qp.setPen(txt_pen)

                    if self.__step_grid_y < 0.001:
                        tmp_str = f"{y:.3e}"
                    elif self.__step_grid_y < 0.01:
                        tmp_str = f"{y:.3f}"
                    elif self.__step_grid_y < 5:
                        tmp_str = f"{y:.2f}"
                    elif self.__step_grid_y > 9999:
                        tmp_str = f"{y:.2E}"
                    else:
                        tmp_str = f"{int(y)}"

                    if y_w > self._MIN_Y + self.__y_label_high + 15:
                        self._qp.drawText(QRectF(self._MIN_X - 110, y_w - 10, 100, 20),
                                          Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, tmp_str)

            if self._y_logarithmic:
                y0_minor = 2 * y
                yk_minor = 10 * y
                ystep_minor = y
            elif self.__draw_minor_grid:  # побочная сетка
                y0_minor = y + self.__step_grid_y / self.__minor_step_ratio
                yk_minor = y + self.__step_grid_y
                ystep_minor = self.__step_grid_y / self.__minor_step_ratio

                # if first:
                #     first = False
                #     y0_minor = self._ystart + ystep_minor
            else:
                continue

            y_min = arange(y0_minor, yk_minor + ystep_minor / 2, ystep_minor)
            y_minor = [self.real_to_window_y(y_m) for y_m in y_min]

            for y_m in y_minor:
                if self._MIN_Y <= y_m <= self._MAX_Y and y_w != y_m:
                    minor_lines.append(QLineF(self._MIN_X, y_m, self._MAX_X, y_m))

        return major_lines, minor_lines

    def _draw_scanner_lines(self):
        for i, line in enumerate(self.__scanner_lines):
            if not line.is_visible():
                continue

            x_win = line.x()
            x_real = self.window_to_real_x(float(x_win))

            if self._xstart < x_real < self._xstop:
                if self.__convert_to_hhmmss:
                    tmp_str = convert_timestamp_to_human_time(x_real + self.__initial_timestamp, millis=True)
                else:
                    if self.__step_grid_x < 0.001:
                        tmp_str = f"{x_real:.3e}"
                    elif self.__step_grid_x > 9999:
                        tmp_str = f"{x_real:.2E}"
                    else:
                        tmp_str = f"{x_real:.3f}"

                font = QFont("consolas", 10)
                font.setBold(True)
                self._qp.setFont(font)
                qm = QFontMetrics(font)
                text_width = qm.size(0, tmp_str).width()  # измеряем текст

                self._qp.setPen(QColor(0, 0, 0, alpha=0))
                self._qp.setBrush(QColor(0, 162, 232, alpha=255))
                rectX = x_win - text_width - 15 + self._MIN_X
                if rectX < self._MIN_X:
                    rectX = x_win + 10 + self._MIN_X
                rectW = text_width + 10
                rectH = 17
                rectY = self._MAX_Y - rectH - 3
                if rectX + rectW > self._MAX_X - 200:
                    rectY -= 27
                self._qp.drawRoundedRect(QRectF(rectX, rectY, rectW, rectH), 5, 5)
                self._value_rect_max_y = rectY - 25

                self._qp.setPen(QColor(255, 255, 255, alpha=255))

                self._qp.drawText(QRectF(rectX, rectY, rectW, rectH),
                                  Qt.AlignmentFlag.AlignCenter, tmp_str)  # значение по Х

                if self.__dark:
                    col = (102, 189, 108) if line.is_selected() else (200, 200, 200)
                else:
                    col = (102, 189, 108) if line.is_selected() else (0, 0, 0)
                th = 1 if False else 1
                self._qp.setPen(QPen(QColor(*col), th))
                self._qp.drawLine(QLineF(x_win + self._MIN_X, self._MIN_Y, x_win + self._MIN_X, self._MAX_Y))

                if i > 0:
                    self._qp.setPen(QColor(100, 100, 100))
                    y = self._MIN_Y + 2
                    pen = QPen(QColor(0, 0, 0))
                    pen.setStyle(Qt.PenStyle.DashLine)
                    self._qp.setPen(pen)
                    self._qp.drawLine(QLineF(x_win + self._MIN_X, y, prev_val_line_coord_xwin, y))

                    self._qp.setPen(QColor(0, 0, 0, alpha=0))
                    self._qp.setBrush(QColor(0, 102, 172, alpha=255))

                    dx = abs(x_real - prev_val_line_coord_xreal)
                    if self.__convert_to_hhmmss:
                        tmp_str = convert_timestamp_to_human_time(dx, millis=True)
                    else:
                        if self.__step_grid_x < 0.001:
                            tmp_str = f"{dx:.3e}"
                        elif self.__step_grid_x > 9999:
                            tmp_str = f"{dx:.2E}"
                        else:
                            tmp_str = f"{dx:.3f}"
                    font = QFont("consolas", 9)
                    font.setBold(True)
                    self._qp.setPen(QColor(100, 100, 100))
                    self._qp.setFont(font)
                    text_width = qm.size(0, tmp_str).width()
                    rectW = text_width + 10
                    rect_x = (min(prev_val_line_coord_xwin, (x_win + self._MIN_X)) +
                              (abs(prev_val_line_coord_xwin - (x_win + self._MIN_X)) - rectW) // 2)
                    rectH = 15
                    rectY = y + 3
                    if abs(prev_val_line_coord_xwin - (x_win + self._MIN_X)) < rectW:
                        if rect_x > self._MIN_X + self.__w / 2:
                            rect_x -= rectW
                        else:
                            rect_x += rectW

                    self._qp.drawText(QRectF(rect_x, rectY, rectW, rectH),
                                      Qt.AlignmentFlag.AlignCenter, tmp_str)

                prev_val_line_coord_xwin = x_win + self._MIN_X
                prev_val_line_coord_xreal = x_real

    def _draw_scale_lines(self):
        self._qp.setFont(QFont('consolas', 10))
        # вертикальные линии для масштабирования
        prev_val_line_coord_xwin = 0
        prev_val_line_coord_xreal = 0
        for i, line in enumerate(self.__scale_lines):
            if not line.is_visible():
                continue

            if self.__dark:
                color = 'lightblue' if line.is_selected() else QColor(103, 115, 229)
            else:
                color = 'lightblue' if line.is_selected() else 'darkblue'

            pen = QPen(QColor(color), 1)
            self._qp.setPen(pen)

            x_win = line.x()
            x_real = self.window_to_real_x(x_win)
            
            self._qp.drawLine(QLineF(x_win + self._MIN_X, self._MIN_Y, x_win + self._MIN_X, self._MAX_Y))

            # формируем подпись со значением Х, на котором стоит линия
            tmp_str = convert_timestamp_to_human_time(x_real + self.__initial_timestamp, millis=True) \
                if self.__convert_to_hhmmss else f"{x_real:.2f}"

            font = QFont('bahnschrift', 10)
            font.setBold(False)
            self._qp.setFont(font)
            qm = QFontMetrics(font)
            text_width = qm.size(0, tmp_str).width()  # измеряем текст

            rectX = self._MIN_X + x_win - text_width - 15 if x_win > self._MIN_X + self.__w / 2 else x_win + self._MIN_X + 5
            rectY = self._MIN_Y + 18 + 20 * i
            rectW = text_width + 10
            rectH = 15
            self._qp.setPen(QColor(0, 0, 0, alpha=0))
            self._qp.setBrush(QColor(0, 128, 128))
            self._qp.drawRoundedRect(QRectF(rectX, rectY, rectW, rectH), 5, 5)
            self._qp.setPen(QColor(255, 255, 255, alpha=255))
            self._qp.drawText(QRectF(rectX, rectY + 1, rectW, rectH), Qt.AlignmentFlag.AlignCenter, tmp_str)

            if i > 0:
                self._qp.setPen(QColor(100, 100, 100))
                y = self._MIN_Y + 2
                if self.__dark:
                    pen = QPen(QColor(200, 200, 200))
                else:
                    pen = QPen(QColor(0, 0, 0))
                pen.setStyle(Qt.PenStyle.DotLine)
                self._qp.setPen(pen)
                self._qp.drawLine(QLineF(x_win + self._MIN_X, y, prev_val_line_coord_xwin, y))

                self._qp.setPen(QColor(0, 0, 0, alpha=0))
                self._qp.setBrush(QColor(0, 102, 172, alpha=255))

                dx = abs(x_real - prev_val_line_coord_xreal)
                if self.__convert_to_hhmmss:
                    tmp_str = convert_timestamp_to_human_time(dx, millis=True)
                else:
                    if self.__step_grid_x < 0.001:
                        tmp_str = f"{dx:.3e}"
                    elif self.__step_grid_x > 9999:
                        tmp_str = f"{dx:.2E}"
                    else:
                        tmp_str = f"{dx:.3f}"
                font = QFont("consolas", 9)
                font.setBold(True)
                if self.__dark:
                    self._qp.setPen(QColor(255, 255, 255))
                else:
                    self._qp.setPen(QColor(100, 100, 100))
                self._qp.setFont(font)
                text_width = qm.size(0, tmp_str).width()
                rectW = text_width + 10
                rect_x = (min(prev_val_line_coord_xwin, x_win) +
                          (abs(prev_val_line_coord_xwin - x_win) - rectW) // 2) + self._MIN_X / 2
                rectH = 15
                rectY = y + 3
                if abs(prev_val_line_coord_xwin - x_win) < rectW:
                    if rect_x > self._MIN_X + self.__w / 2:
                        rect_x -= rectW
                    else:
                        rect_x += rectW

                self._qp.drawText(QRectF(rect_x, rectY, rectW, rectH),
                                  Qt.AlignmentFlag.AlignCenter, tmp_str)

            prev_val_line_coord_xwin = x_win + self._MIN_X
            prev_val_line_coord_xreal = x_real

    def _draw_x_slider(self) -> None:
        """Рисование указателя положения окна просмотра относительно всей имеющейся оси Х"""
        if self._xstart <= self._x_axis_min and self._xstop >= self._x_axis_max:
            return

        self._qp.setPen(QPen(QColor(100, 100, 100, 0), 1))
        self._qp.setBrush(QColor(230, 230, 230, 255 if self.__slider.is_pressed() else 100))

        x0 = self._MIN_X + round((1 - self.__slider.length - 0.01) * self.__w)
        x1 = x0 + round(self.__w * self.__slider.length)
        y0 = self.__slider.y
        R = 5
        self._qp.drawRoundedRect(QRectF(x0, y0, x1 - x0, self.__slider.h), R, R)

        if self.__slider.is_pressed():
            color = QColor(112, 146, 190, 255)
        elif self.__slider.mouse_on():
            color = QColor(190, 190, 190, 150)
        else:
            color = QColor(150, 150, 150, 150)

        self._qp.setBrush(color)
        self._qp.drawRoundedRect(QRectF(self.__slider.x, y0, self.__slider.w, self.__slider.h), R, R)

    def _draw_scaling_rect(self):
        if self.__scaling_rect_drawing:
            # рисуем масштабирующий прямоугольничек
            if self.__dark:
                self._qp.setPen(QPen(QColor(200, 200, 200), 1, Qt.PenStyle.DashLine))
            else:
                self._qp.setPen(QPen(QColor(0, 0, 0), 1, Qt.PenStyle.DashLine))
            self._qp.setBrush(QColor(0, 0, 0, alpha=0))
            rect = QRectF(self.__scaling_rect)
            rect.setLeft(self.__scaling_rect.left() + self._MIN_X)
            rect.setRight(self.__scaling_rect.right() + self._MIN_X)
            rect.setTop(self.__scaling_rect.top() + self._MIN_Y)
            rect.setBottom(self.__scaling_rect.bottom() + self._MIN_Y)
            self._qp.drawRect(rect)
        
    def _scanner_coords(self):
        return tuple(line.x() for line in self.__scanner_lines)
    
    def _scanner_count(self):
        return self.__scanner_lines.line_count()
    
    def enable_human_time_display(self):
        if self._x_logarithmic:
            return
        self._force_redraw()
        self.__convert_to_hhmmss = True

    def disable_human_time_display(self):
        self._force_redraw()
        self.__convert_to_hhmmss = False

    def human_time_display_enabled(self) -> bool:
        return self.__convert_to_hhmmss

    def set_x_autoscale(self, state: bool):
        if self.__x_auto_scale == state:
            return
        if state:
            self._set_x_start(self.x_axis_min)
            self._set_x_stop(self.x_axis_max)
            self._update_step_x()
            self.__group.update_x_borders(self._xstart, self._xstop)
        self._recalculate_window_coords()
        self.__x_auto_scale = state
        self._force_redraw()

    def set_y_autoscale(self, state: bool):
        if self.__y_auto_scale == state:
            return
        
        if state:
            self._calculate_y_parameters()
        self._update_step_y()
        
        self._recalculate_window_coords()
        self.__y_auto_scale = state
        self._force_redraw()

    def set_step_x(self, step: int):
        if step <= 0 or step > self._real_width or step == self.__step_grid_x:
            return
        self.__step_grid_x = step
        self._force_redraw()

    def set_step_y(self, step: int):
        if step <= 0 or step > self._real_height or step == self.__step_grid_y:
            return
        self.__step_grid_y = step
        self._force_redraw()

    def set_x_borders(self, xmin: float, xmax: float):
        if self.__x_auto_scale or xmin >= xmax:
            return
        self._set_x_start(xmin)
        self._set_x_stop(xmax)
        self._recalculate_window_coords()
        self.__group.update_x_borders(self._xstart, self._xstop)
        self._force_redraw()

    def set_x_start(self, x: float):
        if self.__x_auto_scale or x >= self._xstop:
            return
        if self._xstart == x:
            return
        self._set_x_start(x)
        self.__group.update_x_borders(self._xstart, self._xstop)
        self._recalculate_window_coords()
        self._force_redraw()

    def set_x_stop(self, x: float):
        if self.__x_auto_scale or x <= self._xstart:
            return
        if self._xstop == x:
            return
        self._set_x_stop(x)
        self.__group.update_x_borders(self._xstart, self._xstop)
        self._recalculate_window_coords()
        self._force_redraw()

    def set_y_borders(self, ymin: float, ymax: float):
        if self.__y_auto_scale or ymin >= ymax:
            return
        if self._ystart == ymin and self._ystop == ymax:
            return
        self._set_y_start(ymin)
        self._set_y_stop(ymax)
        self._calculate_y_parameters()
        self._recalculate_window_coords()
        self._force_redraw()

    def set_y_start(self, y: float):
        if self.__y_auto_scale or y >= self._ystop:
            return
        if self._ystart == y:
            return
        self._set_y_start(y)
        self._update_step_y()
        self._recalculate_window_coords()
        self._force_redraw()

    def set_y_stop(self, y: float):
        if self.__y_auto_scale or y <= self._ystart:
            return
        if self._ystop == y:
            return
        self._set_y_stop(y)
        self._update_step_y()
        self._recalculate_window_coords()
        self._force_redraw()

    def enable_major_grid(self, enable: bool):
        if self.__draw_major_grid != enable:
            self._force_redraw()
        self.__draw_major_grid = enable

    def enable_minor_grid(self, enable: bool):
        if self.__draw_minor_grid != enable:
            self._force_redraw()
        self.__draw_minor_grid = enable

    def enable_origin_drawing(self, enable: bool, width=1.0):
        self._force_redraw()
        self.__draw_origin = enable
        if 0.25 <= width <= 4:
            self.__origin_pen.setWidthF(width)

    def set_major_grid_style(self, style: str, width=1.0):
        match style:
            case "dot":
                self.__pen_grid.setStyle(Qt.PenStyle.DotLine)
            case "dash":
                self.__pen_grid.setStyle(Qt.PenStyle.DashLine)
            case "solid":
                self.__pen_grid.setStyle(Qt.PenStyle.SolidLine)
        self.__pen_grid.setWidthF(width)
        self._force_redraw()

    def set_minor_grid_style(self, style="dot", width=1.0, step_ratio=5):
        match style:
            case "dot":
                self.__pen_grid_minor.setStyle(Qt.PenStyle.DotLine)
            case "dash":
                self.__pen_grid_minor.setStyle(Qt.PenStyle.DashLine)
            case "solid":
                self.__pen_grid_minor.setStyle(Qt.PenStyle.SolidLine)
        self.__pen_grid_minor.setWidthF(width)
        if step_ratio > 0:
            self.__minor_step_ratio = step_ratio
        self._force_redraw()

    def enable_x_ticks(self, enable: bool):
        if enable != self.__draw_x:
            self._force_redraw()
        self.__draw_x = enable

    def enable_y_ticks(self, enable: bool):
        if enable != self.__draw_y:
            self._force_redraw()
        self.__draw_y = enable

    def _show_extended_window(self):
        ...
    
    @pyqtSlot(bool)
    def pause(self, pause: bool):
        if pause != self.__paused:
            self.__btn_group.pause(pause)
            self.__group.pause_signal.emit(pause)
        self.__paused = pause

    @pyqtSlot(bool)
    def __pause(self, pause: bool):
        if pause != self.__paused:
            self.__btn_group.pause(pause)
        self.__paused = pause

    @pyqtSlot()
    def restart_animation(self, **kwargs):
        if "signal" in kwargs and kwargs["signal"]:
            self.__group.restart_signal.emit(self)

    @pyqtSlot(object)
    def __restart_animation(self, sender: object):
        if sender is not self:
            self.restart_animation()

    def set_x_logarithmic(self, log: bool):
        
        if self._x_logarithmic != log:
            self._x_logarithmic = log
            if log:
                if self._x_axis_min <= 0:
                    warnings.warn("Значения меньше или равные нулю на оси Х не будут отображены при логарифмическом масштабе", stacklevel=2)
                    self._x_axis_min = 0.01
                    self._set_x_start(0.01)
                    self.__group.update_x_borders(self._xstart, self._xstop)
                self.disable_human_time_display()
                self.real_to_window_x = self.__real_to_window_x_log
                self.window_to_real_x = self.__window_to_real_x_log
            else:
                self.real_to_window_x = self.__real_to_window_x_linear
                self.window_to_real_x = self.__window_to_real_x_linear
            self._recalculate_window_coords()
            self._update_step_x()
            self._force_redraw()

    def set_y_logarithmic(self, log: bool):
        if log:
            if self._y_axis_min <= 0:
                warnings.warn("Значения меньше или равные нулю на оси У не будут отображены при логарифмическом масштабе", stacklevel=2)
                self._y_axis_min = 0.01
                self._set_y_start(0.01)
            else:
                self._set_y_start(self._y_axis_min)
        if self._y_logarithmic != log:
            self._y_logarithmic = log
            if log:
                self.real_to_window_y = self.__real_to_window_y_log
                self.window_to_real_y = self.__window_to_real_y_log
            else:
                self.real_to_window_y = self.__real_to_window_y_linear
                self.window_to_real_y = self.__window_to_real_y_linear
                self._calculate_y_parameters()
            self._recalculate_window_coords()
            self._update_step_y()
            self._force_redraw()
    
    @property 
    def x_name(self):
        return self.__x_name
    
    @property
    def y_name(self):
        return self.__y_name
    
    @property
    def x_ticks_enabled(self):
        return self.__draw_x
    
    @property
    def y_ticks_enabled(self):
        return self.__draw_y
    
    @property
    def origin_is_drawing(self):
        return self.__draw_origin
    
    @property
    def step_x(self):
        return self.__step_grid_x
    
    @property
    def step_y(self):
        return self.__step_grid_y
    
    @property
    def x_start(self):
        return self._xstart
    
    @property
    def x_stop(self):
        return self._xstop
    
    @property
    def y_start(self):
        return self._ystart
    
    @property
    def y_stop(self):
        return self._ystop
    
    @property
    def major_ticks_enabled(self):
        return self.__draw_major_grid
    
    @property
    def minor_ticks_enabled(self):
        return self.__draw_minor_grid
    
    @property
    def x_axis_min(self):
        return self._x_axis_min
    
    @property
    def x_axis_max(self):
        return self._x_axis_max
    
    @property
    def major_grid_width(self):
        return self.__pen_grid.widthF()
    
    @property
    def minor_grid_width(self):
        return self.__pen_grid_minor.widthF()
    
    @property
    def major_grid_style(self):
        return self.__pen_grid.style().name
    
    @property
    def minor_grid_atyle(self):
        return self.__pen_grid_minor.style().name
    
    def set_dark(self, dark: bool):
        self.__dark = dark
        self.__btn_group.set_dark(dark)
        self._force_redraw()

    def _set_buttons_visible(self, visible: bool):
        self.__btn_group.set_buttons_visible(visible)
    
    @property
    def x_is_logarithmic(self) -> bool:
        return self._x_logarithmic
    
    @property
    def y_is_logarithmic(self) -> bool:
        return self._y_logarithmic

    @property
    def dark(self):
        return self.__dark
    