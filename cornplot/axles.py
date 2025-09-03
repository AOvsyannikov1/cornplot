import os, warnings
from math import log10, floor, ceil, pow
from typing import overload

from PyQt6.QtCore import Qt, QLineF, QRectF, pyqtSlot as Slot, QRect, QTimer
from PyQt6.QtGui import QPen, QColor, QPainter, QFont, QFontMetrics, QGuiApplication
from PyQt6.QtWidgets import (
    QFileDialog, QWidget, QGestureEvent, 
    QPinchGesture, QPanGesture, QTapGesture, 
    QTapAndHoldGesture, QSizePolicy
    )

from .utils import *

from .button_group import ButtonGroup
from .axle_slider import AxleSlider
from .colors import *
from .action_buffer import ActionBuffer
from .array_utils import *
from .axle_group_data import AxleGroupData, MAX_SCANNER_LINES
from .coordinate_ax import CoordinateAx
from .scanner_lines import VerticalLineList


axle_groups: dict[str, AxleGroupData] = dict()


class Axles(QWidget):
    _OFFSET_Y_UP = 22             # смещение по У для размещения шапки
    _OFFSET_Y_DOWN = 25
    _OFFSET_X = 100
    _Y_STOP_RATIO = 20
    _Y_STOP_COEFF = 0.05

    def __init__(self, widget, x: int, y: int, w: int, h: int):
        super().__init__()
        self._widget = widget
        self.setParent(widget)
        self.__group = AxleGroupData()
        self.__scale_lines: VerticalLineList = self.__group.scale_lines
        self.__scanner_lines: VerticalLineList = self.__group.scanner_lines

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

        self._xstart = 0.0
        self._xstop = 10.0
        self._x_axis_min = 0.0
        self._x_axis_max = 10.0
        self._real_width = self._xstop - self._xstart  # длина оси Х в реальных единицах
        self.__step_grid_x = self._real_width / 2

        self.__group.x_start = self._xstart
        self.__group.x_stop = self._xstop

        self._ystart = 0.0
        self._ystop = 1.0
        self._y_axis_min = 0.0
        self._y_axis_max = 1.0
        self._real_height = self._ystop - self._ystart  # длина оси У в реальных единицах
        self._step_grid_y = self._real_height / 2

        self.__scaling_rect = QRectF(0.0, 0.0, 0.0, 0.0)

        # флаги
        self.__convert_to_hhmmss = False    # конвертировать ли значения Х в ЧЧ:ММ:СС
        self.__animated = False
        self._visible = True
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

        self._digits_count = -1

        self._x_axle = CoordinateAx()
        self._y_axle = CoordinateAx()

        self._x_axle.met_size = 50
        self._x_axle.label_size = 100
        self._x_axle.name = "X"

        self._y_axle.met_size = self._OFFSET_X
        self._y_axle.label_size = 20
        self._y_axle.name = "Y"        
       
        self.__background_color = QColor(255, 255, 255)
        self.__font = QFont("Bahnschrift, Arial", 11)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.__touch_x = 0
        self.__touch_y = 0

        self.__initial_x = 0
        self.__initial_y = 0

        self.__mouse_on = False

        self.__initial_timestamp = 0

        self._qp = QPainter()

        super().setGeometry(self.__x - self._OFFSET_X, self.__y - self._OFFSET_Y_UP, self.__w + self._OFFSET_X, self.__h + self._OFFSET_Y_UP + self._OFFSET_Y_DOWN)
        self.setMouseTracking(True)
        self.show()

        self.__btn_group = ButtonGroup(self, self.__w, self.__h)
        self.__btn_group.add_vert_button.clicked.connect(self.__add_scanner)
        self.__btn_group.clear_button.clicked.connect(self.__clear_axles)
        self.__btn_group.zoom_button.clicked.connect(self._zoom_in)
        self.__btn_group.back_button.clicked.connect(self.__cancel_scaling)
        self.__btn_group.setGeometry(self._MIN_X, self._OFFSET_Y_DOWN - self._OFFSET_Y_UP, self.__w, self.__h)
        self.__btn_group.save_button.clicked.connect(self.__save_picture)
        self.__btn_group.more_button.clicked.connect(self._show_extended_window)
        self.__btn_group.pause_button.clicked.connect(lambda: self.pause(not self.__paused))
        self.__btn_group.restart_button.clicked.connect(lambda: self.restart_animation(signal=True))
        self.__btn_group.fix_button.clicked.connect(lambda: self.fix_y_zero(not self.__zero_y_fixed))

        self._value_rect_max_y = self._MAX_Y

        self.grabGesture(Qt.GestureType.PinchGesture)
        self.grabGesture(Qt.GestureType.PanGesture)
        self.grabGesture(Qt.GestureType.TapAndHoldGesture)
        self.grabGesture(Qt.GestureType.TapGesture)

        self.__tapped = False

        self._update_step_x()
        self._update_step_y()
        self.__recalculate_slider_coords()

        self.setCursor(Qt.CursorShape.ArrowCursor)

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

        self.__draw_background()
        self._draw_grid()

    def __draw_background(self):
        self._qp.setPen(QColor(0, 0, 0, 0))
        self._qp.setBrush(background_color(self.__dark))
        self._qp.drawRect(self._OFFSET_X, self._OFFSET_Y_UP, self.__w, self.__h)  # поле графика

        # оси координат по необходимости
        x = self._real_to_window_x(0)
        y = self._real_to_window_y(0)
        if self._x_axle.draw_ax and self._MIN_Y <= y <= self._MAX_Y:
            self._qp.setPen(self._x_axle.origin_pen)
            self._qp.drawLine(QLineF(self._MIN_X, y, self._MAX_X, y))
        if self._y_axle.draw_ax and self._MIN_X <= x <= self._MAX_X:
            self._qp.setPen(self._y_axle.origin_pen)
            self._qp.drawLine(QLineF(x, self._MIN_Y, x, self._MAX_Y))

    @Slot()
    def __timer_callback(self):
        self.__check_color_theme()
        self.__btn_group.process_visibility()
        self.__check_group_x_borders()
        if self._needs_redrawing():
            self.update()

    def __check_color_theme(self):
        if self.__dark and QGuiApplication.styleHints().colorScheme() != Qt.ColorScheme.Dark:
            self.set_dark(False)
            self._redraw_required = True
        elif not self.__dark and QGuiApplication.styleHints().colorScheme() != Qt.ColorScheme.Light:
            self.set_dark(True)
            self._redraw_required = True

    @property
    def visible(self):
        return self.isVisible()

    def setGeometry(self, ax: int, ay: int, aw: int, ah: int) -> None:
        if self.__x != ax or self.__y != ay or self.__w != aw or self.__h != ah:

            if ax > 0:
                self.__x = ax
            if ay > 0:
                self.__y = ay
            if aw > 0:
                self.__w = aw
            if ah > 0:
                self.__h = ah
            super().setGeometry(self.__x - self._OFFSET_X, self.__y - self._OFFSET_Y_UP, self.__w + self._OFFSET_X, self.__h + self._OFFSET_Y_UP + self._OFFSET_Y_DOWN)

            self._MAX_X = self._MIN_X + self.__w
            self._MAX_Y = self._MIN_Y + self.__h

            self.__btn_group.setGeometry(self._MIN_X, self._OFFSET_Y_DOWN - self._OFFSET_Y_UP, self.__w, self.__h)

            self._update_step_x()
            self._update_step_y()
            self._calculate_y_parameters()
            self._recalculate_window_coords()

    @Slot()
    def __add_scanner(self):
        x0 = 1 / MAX_SCANNER_LINES
        self.__scanner_lines.add_line(x0 + self.__scanner_lines.line_count() / (MAX_SCANNER_LINES + 1))
        self._redraw_required = True
        self.__group.line_move_signal.emit()

    @Slot()
    def __clear_axles(self):
        for line in self.__scale_lines:
            line.hide()
        for line in self.__scanner_lines:
            line.hide()
        self.__group.line_clear_signal.emit(self)
        self._redraw_required = True
        self.update()

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
        self.__group.line_move_signal.connect(self.update)
        self.__group.pause_signal.connect(self.__pause)
        self.__group.restart_signal.connect(self.__restart_animation)
        self.__group.line_clear_signal.connect(self.__redraw_after_clear_lines)

    def __redraw_after_clear_lines(self, sender: object):
        if sender is not self:
            self.update()

    def fix_y_zero(self, fix: bool) -> None:
        if fix != self.__zero_y_fixed:
            self.__zero_y_fixed = fix
            self._calculate_y_parameters()
            self._update_step_y()
            self._recalculate_window_coords()
            self._redraw_required = True

    def _update_step_x(self) -> float:
        """Вычисление шага по оси Х"""
        if not self._x_axle.autoscale:
            return self.__step_grid_x
        try:
            new_step = 10 ** (round(log10(self._real_width)) - 1)
        except ValueError:
            new_step = 1.0

        ticks_count = self._real_width / new_step
        if ticks_count > 10:
            n = 3
            while (ticks_count := self._real_width / new_step) > 10:
                n += 1
                new_step *= self.__get_factor(n)
        else:
            n = 0
            while (ticks_count := self._real_width / new_step) < 10:
                n += 1
                new_step /= self.__get_factor(n)
        tick_width_px = new_step / self._real_width * self.__w
        while (tick_width_px := new_step / self._real_width * self.__w) < self._x_axle.met_size + 15:
            new_step *= self.__get_factor(n)
            n += 1

        if 150 < tick_width_px:
            new_step /= self.__get_factor(n)

        if new_step == 0:
            new_step = self._real_width / 1

        self.__step_grid_x = new_step        
        return new_step

    def _update_step_y(self) -> float:
        """Вычисление шага по оси У"""

        if not self._y_axle.autoscale:
            return self._step_grid_y

        if self._ystart == self._ystop:
            self._ystart -= 0.5
            self._ystop += 0.5
            self._real_height = 1

        try:
            self._step_grid_y = 10 ** (round(log10(self._real_height)) - 1)
        except ValueError:
            self._step_grid_y = 1.0
        n = 0

        if self._real_height / self._step_grid_y >= 10:
            n = 3
            while self._real_height / self._step_grid_y >= 10:
                n += 1
                self._step_grid_y *= self.__get_factor(n)

        elif self._real_height / self._step_grid_y < 8:
            while self._real_height / self._step_grid_y <= 10:
                n += 1
                self._step_grid_y /= self.__get_factor(n)

        while self._step_grid_y / self._real_height * self.__h < 25:  # высота не менее 30 пикселей
            n += 1
            self._step_grid_y *= self.__get_factor(n)

        if self._step_grid_y / self._real_height * self.__h > 100:
            self._step_grid_y /= self.__get_factor(n)

        return self._step_grid_y

    def __get_factor(self, n):
        return 2.5 if n % 4 == 0 else 2

    def _is_animated(self) -> bool:
        return self.__animated

    def set_x_name(self, name: str) -> None:
        if name == self._x_axle.name:
            return
        self._x_axle.name = name
        self._redraw_required = True

    def set_y_name(self, name: str) -> None:
        if self._y_axle.name == name:
            return
        self._y_axle.name = name
        self._redraw_required = True

    @Slot()
    def _zoom_in(self):
        if self.__scale_lines.line_count() < 2:
            return
        if self.__animated and not self.__paused:
            return
        if self._x_axle.logarithmic or self._y_axle.logarithmic:
            return
        # увеличиваем график между двуми вертикальными линиями
        line_coords = [self._get_line_window_coord(line) - self._MIN_X for line in self.__scale_lines]
        x0 = self._window_to_real_x(min(line_coords))
        x1 = self._window_to_real_x(max(line_coords))

        if x1 - x0 > 0.02 * self._real_width:
            self.__action_buffer.add_action(self._xstart, self._xstop, self._ystart, self._ystop)
            self._set_x_start(x0)
            self._set_x_stop(x1)
            self._update_step_x()
            self._calculate_y_parameters()
            self._update_step_y()
            self._recalculate_window_coords()
            self.__group.update_x_borders(self._xstart, self._xstop)
            self._redraw_required = True

        self.__delete_scale_lines()
        self.setCursor(Qt.CursorShape.ArrowCursor)
        
    def _zoom_out(self):
        if self._x_axle.logarithmic or self._y_axle.logarithmic:
            return
        self.__action_buffer.add_action(self._xstart, self._xstop, self._ystart, self._ystop)
        if self.__MAXIMUM_X_WIDTH == -1:
            self._set_x_start(self._x_axis_min)
            self._set_x_stop(self._x_axis_max)
        else:
            x_center = self._window_to_real_x(round(self._MAX_X / 2))
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
        self._redraw_required = True

    def __check_group_x_borders(self):
        if self._xstart != self.__group.x_start or self._xstop != self.__group.x_stop:
            if self._x_axle.logarithmic:
                self._set_x_start(self.__group.x_start if self.__group.x_start > 0 else 0.01)
                self._set_x_stop(self.__group.x_stop)
            else:
                self._set_x_start(self.__group.x_start)
                self._set_x_stop(self.__group.x_stop)
            self._recalculate_window_coords()
            self._update_step_x()
            self._redraw_required = True

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
        self.__slider.x += mouse_x - self.__slider.x0

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

        if self._x_axle.logarithmic and x_start <= 0:
            pass
        else:
            self._set_x_start(x_start)
            self._set_x_stop(x_stop)
            self._recalculate_window_coords()
            self.__group.update_x_borders(x_start, x_stop)

    @Slot()
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
        self._redraw_required = True

    def _recalculate_window_coords(self):
        self.__recalculate_slider_coords()

    def _calculate_x_parameters(self):
        pass

    def _calculate_y_parameters(self):
        pass

    @Slot()
    def __save_picture(self):
        was_paused = self.__paused
        if self.__animated and not self.__paused:
            self.pause(True)
        self.__btn_group.set_buttons_visible(False)
        grab = self.grab(QRect(0, 0, self.width() + 10, self.height()))
        fileName, _ = QFileDialog.getSaveFileName(self, "Сохранить картинку", "",
                                                            "PNG Files (*.png)")
        if len(fileName) > 0:
            grab.save(fileName, 'png')
            try:
                os.startfile(fileName)
            except:
                pass
        self.__btn_group.set_buttons_visible(True)
        if self.__animated:
            self.pause(was_paused)

    def leaveEvent(self, a0):
        self.clearFocus()
        self.__mouse_on = False
        self.__ctrl_pressed = False
        self.__shift_pressed = False
        self.__left_button_pressed = False
        self.__slider.set_mouse_on(False)
        self.__deselect_all_lines()
        self.setCursor(Qt.CursorShape.ArrowCursor)

    def enterEvent(self, a0):
        self.setFocus()
        self.__mouse_on = True

    def mouseMoveEvent(self, a0):
        pos = a0.pos()
        if pos.y() < self._MIN_Y and not self.__zoom_active:
            self.__slider.release()
        
        pos_x = pos.x() - self._MIN_X

        if self.__slider.mouse_on():
            self.__deselect_all_lines()
            self._redraw_required = True
        
            # обработка слайдера
            if self.__slider.is_pressed() and (self._xstart != self._x_axis_min or self._xstop != self._x_axis_max):
                self.__move_slider(pos.x() + self._MIN_X)
        else:
            self.__slider.release()
        
            if not self.__left_button_pressed and not self.__slider.is_pressed() and not self.__zoom_active:
                for line in self.__scanner_lines:
                    if line.is_visible():
                        old_val = line.is_selected()
                        line.select(abs(pos.x() - self._get_line_window_coord(line)) < 15)
                        if old_val != line.is_selected():
                            self._redraw_required = True
                            self.update()
                            self.__group.line_move_signal.emit()

                if self.__scanner_lines.any_selected():
                    for line in self.__scale_lines:
                        line.select(False)
                else:
                    for line in self.__scale_lines:
                        old_val = line.is_selected()
                        line.select(abs(pos.x() - self._get_line_window_coord(line)) < 15)
                        if old_val != line.is_selected():
                            self._redraw_required = True
                            self.update()
                            self.__group.line_move_signal.emit()

        if self.__left_button_pressed:
            if self.__ctrl_pressed:
                if self.__animated and not self.__paused:
                    return

                # движение графика при нажатой клавише ctrl
                tmpX = self._window_to_real_x(self.__initial_x) - self._window_to_real_x(pos.x())
                new_xstart = max(min(tmpX, self._x_axis_max - self._real_width), self._x_axis_min)
                if self._x_axle.logarithmic and new_xstart <= 0:
                    new_xstart = self._xstart
                self._xstart = new_xstart
                self._xstop = self._xstart + self._real_width

                tmpY = self.__initial_y - self._window_to_real_y(pos.y())
                self._ystart += tmpY
                min_possible_y = (0 if self.__zero_y_fixed and self._y_axis_min >= 0
                                    else self._y_axis_min - self._Y_STOP_COEFF)
                max_possible_y = self._y_axis_max + (0 if (self.__zero_y_fixed and self._y_axis_max <= 0)
                                                        else self._Y_STOP_COEFF)
                if self._ystart < min_possible_y:
                    self._ystart = min_possible_y
                if self._ystart + self._real_height > max_possible_y:
                    self._ystart = max_possible_y - self._real_height
                self._ystop = self._ystart + self._real_height

                self._calculate_y_parameters()
                self._recalculate_window_coords()
                self.__group.update_x_borders(self._xstart, self._xstop)

                self._redraw_required = True

            # движение линий сканеров
            if self.__scanner_lines.nearest_line != -1:
                new_coord = min(max(pos_x, 2), self.__w - 1)
                self.__scanner_lines.get_nearest_line().set_x_coord(new_coord / (self._MAX_X - self._MIN_X))
                self.__scanner_lines.last_line = self.__scanner_lines.nearest_line
                self._redraw_required = True
                self.update()
                self.__group.line_move_signal.emit()

            # движение масштабирующих линий
            if self.__scale_lines.line_under_mouse() != -1 and not self.__scanner_lines.line_under_mouse():
                new_coord = min(max(pos_x, 1), self.__w - 1)
                self.__scale_lines.get_nearest_line().set_x_coord(new_coord / (self._MAX_X - self._MIN_X))
                self._redraw_required = True
                self.update()
                self.__group.line_move_signal.emit()

            # определение координат масштабирующего прямоугольника
            if self.__scaling_rect_drawing:
                if self.__animated and not self.__paused:
                    return
                self.__scaling_rect.setRight(min(max(pos_x, 0), self.__w))
                self.__scaling_rect.setBottom(min(max(pos.y() - self._MIN_Y, 0), self.__h))
                self._redraw_required = True
        else:
            self.__slider.set_mouse_on(self.__slider.x <= pos.x() <= self.__slider.x + self.__slider.w and 
                                    self.__slider.y <= pos.y() <= self.__slider.y + self.__slider.h)

    def mousePressEvent(self, a0):
        pos = a0.pos()
        
        if pos.y() < self._OFFSET_Y_UP:
            return
        
        self.__initial_x = pos.x() + self._MIN_X - self._real_to_window_x(self._x_axis_min if self._x_axle.logarithmic else 0)
        # расстояние от точки касания до осей в пикселях
        self.__initial_y = self._window_to_real_y(pos.y())

        self.__touch_x = pos.x()
        self.__touch_y = pos.y()

        match a0.button():
            case Qt.MouseButton.LeftButton:
                self.__left_button_pressed = True

                if self.__ctrl_pressed:
                    self.setCursor(Qt.CursorShape.ClosedHandCursor)

                if not self.__scanner_lines.any_selected() and not self.__scale_lines.any_selected():
                    if self.__animated and not self.__paused:
                        return
                    if self.__slider.mouse_on():
                        self.__slider.press()
                        self.__slider.set_initial_x(pos.x() + self._OFFSET_X)
                        self._redraw_required = True
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
                    self._redraw_required = True
            case Qt.MouseButton.XButton1:
                self.__cancel_scaling()

    def mouseReleaseEvent(self, a0):
        pos = a0.pos()
        
        match a0.button():
            case Qt.MouseButton.LeftButton:
                self.__left_button_pressed = False
                self.__scaling_rect_drawing = False

                if self.__ctrl_pressed:
                    self.setCursor(Qt.CursorShape.OpenHandCursor)
                else:
                    self.setCursor(Qt.CursorShape.ArrowCursor)

                if self.__slider.is_pressed():
                    self.__slider.release()
                    return

                self.__scanner_lines.nearest_line = -1
                self.__scale_lines.nearest_line = -1
                if self.__animated and not self.__paused or self.__scale_lines.any_selected() or self.__scanner_lines.any_selected():
                    return
                else:
                    if not self._x_axle.logarithmic and not self._y_axle.logarithmic:
                        if pos.x() > self._MIN_X and self.__scaling_rect.width() == 0 and self.__scaling_rect.height() == 0 and not self.__zoom_active:
                            if self.__touch_x == pos.x() and self.__touch_y == pos.y() and not self._point_added:
                                self.__scale_lines.add_line((pos.x() - self._MIN_X) / (self._MAX_X - self._MIN_X))
                                self.__group.line_move_signal.emit()
                        else:
                            if abs(self.__scaling_rect.width()) > 10 and abs(self.__scaling_rect.height()) > 10:
                                x0 = self._window_to_real_x(min(self.__scaling_rect.left(), self.__scaling_rect.right()))
                                x1 = self._window_to_real_x(max(self.__scaling_rect.left(), self.__scaling_rect.right()))
                                y0 = self._window_to_real_y(max(self.__scaling_rect.top(), self.__scaling_rect.bottom()) + self._OFFSET_Y_UP)
                                y1 = self._window_to_real_y(min(self.__scaling_rect.top(), self.__scaling_rect.bottom()) + self._OFFSET_Y_UP)
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
                                self._redraw_required = True

                self.__zoom_active = False
                self.__scaling_rect.setCoords(0, 0, 0, 0)
                self.__scaling_rect_drawing = False
                self._redraw_required = True

                if self._point_added:
                    self._point_added = False

    def mouseDoubleClickEvent(self, a0):
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
                self._redraw_required = True
                self.__group.line_move_signal.emit()
    
    def keyPressEvent(self, a0):
        match a0.key():
            case Qt.Key.Key_Shift:
                if not self.__slider.mouse_on():
                    if not self._x_axle.logarithmic and not self._y_axle.logarithmic:
                        self.__shift_pressed = True
                        self.setCursor(Qt.CursorShape.CrossCursor)
                self.__ctrl_pressed = False
            case Qt.Key.Key_Control:
                if not self.__slider.mouse_on():
                    self.__ctrl_pressed = True
                    self.setCursor(Qt.CursorShape.OpenHandCursor)
                self.__shift_pressed = False
            case Qt.Key.Key_Plus:
                if self.__scale_lines.line_count() == 2:
                    self._zoom_in()
            case Qt.Key.Key_Minus:
                self._zoom_out()

    def keyReleaseEvent(self, a0):
        match a0.key():
            case Qt.Key.Key_Shift:
                self.__scaling_rect_drawing = False
                self.__shift_pressed = False
                self.setCursor(Qt.CursorShape.ArrowCursor)
            case Qt.Key.Key_Control:
                self.__ctrl_pressed = False
                self.setCursor(Qt.CursorShape.ArrowCursor)

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
        self._redraw_required = True

    def event(self, a0):
        if isinstance(a0, QGestureEvent):
            for gesture in a0.gestures():
                if isinstance(gesture, QPinchGesture):
                    self.__pinch_gesture_event(gesture)     # масштабирование двумя пальцами
                elif isinstance(gesture, QPanGesture):
                    self.__pan_gesture_event(gesture)       # перемещение двумя пальцами
                elif isinstance(gesture, QTapGesture):
                    self.__tap_gesture_event(gesture)
                elif isinstance(gesture, QTapAndHoldGesture):
                    self.__tap_and_hold_gesture_event(gesture)
            a0.accept()
            return True
        return super().event(a0)
    
    def __pinch_gesture_event(self, gesture: QPinchGesture):
        """Увеличение или уменьшение масштаба двумя пальцами"""
        if self.__animated and not self.__paused:
            return
        if gesture.state() == Qt.GestureState.GestureStarted:
            ...
        elif gesture.state() == Qt.GestureState.GestureUpdated:
            center = gesture.centerPoint()
            center = self.mapFromGlobal(center)
            center.setX(self._window_to_real_x(center.x() - self._MIN_X))
            center.setY(self._window_to_real_y(center.y() - self._MIN_Y))

            scale_factor_x = gesture.scaleFactor()
            scale_factor_y = gesture.scaleFactor()
            
            left_size = abs(center.x() - self._xstart) /(scale_factor_x)
            right_size = abs(self._xstop - center.x()) / (scale_factor_x)

            self._xstart = center.x() - left_size
            self._xstop = center.x() + right_size
            recalc = False
            if self._xstart < self._x_axis_min and self._xstop > self._x_axis_max:
                self._xstart = self._x_axis_min
                self._xstop = self._x_axis_max
            elif self._xstop > self._x_axis_max:
                self._xstop = self._x_axis_max
                self._update_step_x()
                recalc = True
            elif self._xstart < self._x_axis_min:
                self._xstart = self._x_axis_min
                self._update_step_x()
                recalc = True
            else:
                self._update_step_x()
                recalc = True
            self._real_width = self._xstop - self._xstart
            self._update_x_borders(self._xstart, self._xstop)

            down_size = abs(center.y() - self._ystart) / scale_factor_y
            up_size = abs(self._ystop - center.y()) / scale_factor_y

            ystart_new = center.y() - down_size
            ystop_new = center.y() + up_size
            ymax = self._y_axis_max + self._Y_STOP_COEFF
            ymin = self._y_axis_min - self._Y_STOP_COEFF
            if ystart_new < ymin and ystop_new > ymax:
                self._ystart = ymin
                self._ystop = ymax
            elif ystop_new > ymax:
                self._ystop = ymax
                self._ystart = ystart_new
                self._update_step_y()
                recalc = True
            elif ystart_new < ymin:
                self._ystart = ymin
                self._ystop = ystop_new
                self._update_step_y()
                recalc = True
            elif ystop_new - ystart_new < self._Y_STOP_COEFF:
                pass
            else:
                self._update_step_y()
                recalc = True
                self._ystart = ystart_new
                self._ystop = ystop_new
            self._real_height = self._ystop - self._ystart
            if recalc:
                self._recalculate_window_coords()
            self._redraw_required = True
        elif gesture.state() == Qt.GestureState.GestureFinished:
            pass

    def __pan_gesture_event(self, gesture: QPanGesture):
        if self.__animated and not self.__paused:
            return
        if gesture.state() == Qt.GestureState.GestureStarted:
           pass
        elif gesture.state() == Qt.GestureState.GestureUpdated:
            dx, dy = gesture.delta().x(), gesture.delta().y()
            dx_real = -dx / (self._MAX_X - self._MIN_X) * self._real_width
            dy_real = dy / (self._MAX_Y - self._MIN_Y) * self._real_height
            
            xstart_new = self._xstart + dx_real
            xstop_new = self._xstop + dx_real
            recalc = False
            if xstart_new > self._x_axis_min and xstop_new < self._x_axis_max:
                self._set_x_start(xstart_new)
                self._set_x_stop(xstop_new)
                self._update_x_borders(self._xstart, self._xstop)
                recalc = True

            ystart_new = self._ystart + dy_real
            ystop_new = self._ystop + dy_real
            ymax = self._y_axis_max + self._Y_STOP_COEFF
            ymin = self._y_axis_min - self._Y_STOP_COEFF
            if ystart_new >= ymin and ystop_new <= ymax:
                self._set_y_start(ystart_new)
                self._set_y_stop(ystop_new)
                recalc = True
            
            if recalc:
                self._recalculate_window_coords()
            self._redraw_required = True
        elif gesture.state() == Qt.GestureState.GestureFinished:
            pass

    def __tap_gesture_event(self, gesture: QTapGesture):
        if gesture.state() == Qt.GestureState.GestureStarted:
            self.__tapped = True
        elif gesture.state() == Qt.GestureState.GestureUpdated:
            pass
        elif gesture.state() == Qt.GestureState.GestureCanceled:
            self.__tapped = False
        elif gesture.state() == Qt.GestureState.GestureFinished:
            self.__tapped = False

    def __tap_and_hold_gesture_event(self, gesture: QTapAndHoldGesture):
        if self.__animated and not self.__paused:
            return
        if gesture.state() == Qt.GestureState.GestureStarted:
            if self.__tapped:
                self._zoom_out()
                self.__tapped = False
        elif gesture.state() == Qt.GestureState.GestureUpdated:
            pass
        elif gesture.state() == Qt.GestureState.GestureFinished:
            self.__tapped = False
    
    def _get_width(self):
        return self.__w
    
    def _get_heignt(self):
        return self.__h

    def _real_to_window_x(self, x: float) -> float:
        """Перевод реальных координат оси х в оконные"""
        return c_real_to_window_x(x, self._MIN_X, self.__w, self._real_width, self._xstart)
    
    def __real_to_window_x_linear(self, x: float) -> float:
        return c_real_to_window_x(x, self._MIN_X, self.__w, self._real_width, self._xstart)
    
    def __real_to_window_x_log(self, x: float) -> float:
        return c_real_to_window_x_log(x, self._MIN_X, self.__w, self._xstart, self._xstop)

    def _real_to_window_y(self, y: float) -> float:
        """Перевод реальных координат оси у в оконные"""
        return c_real_to_window_y(y, self._MIN_Y, self.__h, self._real_height, self._ystop)
    
    def __real_to_window_y_linear(self, y: float) -> float:
        return c_real_to_window_y(y, self._MIN_Y, self.__h, self._real_height, self._ystop)
    
    def __real_to_window_y_log(self, y: float) -> float:
        return c_real_to_window_y_log(y, self._MIN_Y, self._MAX_Y, self.__h, self._ystart, self._ystop)

    def _window_to_real_x(self, x: float) -> float:
        """Перевод оконных координат оси х в реальные"""
        return c_window_to_real_x(x, self.__w, self._real_width, self._xstart)
    
    def __window_to_real_x_linear(self, x: float) -> float:
        return c_window_to_real_x(x, self.__w, self._real_width, self._xstart) 
    
    def __window_to_real_x_log(self, x: float) -> float:
        return c_window_to_real_x_log(x, self.__w, self._xstart, self._xstop)

    def _window_to_real_y(self, y: float) -> float:
        return c_window_to_real_y(y, self.__h, self._real_height, self._ystop, self._OFFSET_Y_UP)
    
    def __window_to_real_y_linear(self, y: float) -> float:
        return c_window_to_real_y(y, self.__h, self._real_height, self._ystop, self._OFFSET_Y_UP)
    
    def __window_to_real_y_log(self, y: float) -> float:
        return c_window_to_real_y_log(y, self.__h, self._ystart, self._ystop, self._OFFSET_Y_UP)
    
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
        self.__draw_grid_x()
        self.__draw_grid_y()      

    def __draw_grid_x(self):
        font = QFont(self.__font)
        font.setBold(True)
        self._qp.setFont(font)

        txt_pen = QPen(text_color(self.__dark))
        self._qp.setPen(txt_pen)

        self._x_axle.label_size = QFontMetrics(font).horizontalAdvance(self._x_axle.name)
          
        if self._x_axle.draw_label:
            self._qp.drawText(self._MAX_X - self._x_axle.label_size, self._MAX_Y + 3, self._x_axle.label_size, 20,
                              Qt.AlignmentFlag.AlignRight, self._x_axle.name)  # имя оси Х
        
        font.setBold(False)
        self._qp.setFont(font)
        
        # формируем метки по оси Х
        x0 = round_custom(self._xstart, self.__step_grid_x)
        xk = max(self._x_axis_max, self._xstop)

        if self._x_axle.logarithmic:
            if x0 <= 0:
                x0 += self.__step_grid_x
            initial_x_power = floor(log10(self._xstart))
            end_x_power = ceil(log10(self._xstop))
            x_metki_coords = [10 ** i for i in range(initial_x_power, end_x_power + 1)]
        else:
            x_metki_coords = np.round(arange(x0, xk + self.__step_grid_x, self.__step_grid_x), 15)
        new_x_met_width = self._x_axle.met_size
        self._x_axle.met_size = 0

        divised_step = self.__step_grid_x / self._x_axle.divisor
        digit_count = max(get_digit_count_after_dot(x / self._x_axle.divisor) for x in x_metki_coords)
        digit_count = max(get_digit_count_after_dot(divised_step), digit_count)
        if divised_step < 0.5:
            digit_count = max(2, digit_count)
        
        for x in x_metki_coords:
            x_w = self._real_to_window_x(x)  # оконная координата метки
            
            if self._MIN_X < x_w < self._MAX_X:
                if not (x == 0 and self.__draw_origin) and self._x_axle.draw_major_grid:
                    self._qp.setPen(self._x_axle.pen_major)
                    self._qp.drawLine(QLineF(x_w, self._MAX_Y, x_w, self._MIN_Y))

                if self._x_axle.draw_ticks:
                    # подписи осей
                    self._qp.setPen(txt_pen)
                    x = x / self._x_axle.divisor
                    if self.__convert_to_hhmmss and self._x_axis_min >= 0:
                        tmp_str = convert_timestamp_to_human_time(x + self.__initial_timestamp, divised_step < 1)
                    else:
                        if self._x_axle.logarithmic:
                            power_of_ten = int(log10(x))
                            tmp_str = "10" + get_upper_index(power_of_ten)
                        else:
                            tmp_str = self.__get_rounded_tick(x, divised_step, digit_count if self._digits_count < 0 else self._digits_count)

                    tmp_str_width = QFontMetrics(font).horizontalAdvance(tmp_str)
                    if tmp_str_width > self._x_axle.met_size:
                        self._x_axle.met_size = tmp_str_width

                    if self._MIN_X + 30 < x_w < self._MAX_X - self._x_axle.label_size - tmp_str_width:
                        self._qp.drawText(QRectF(x_w - (tmp_str_width >> 1), self._MAX_Y + 1, tmp_str_width, 20),
                                          Qt.AlignmentFlag.AlignCenter, tmp_str)

            if self._x_axle.logarithmic:
                x0_minor = 2 * x
                xk_minor = 10 * x
                xstep_minor = x
            elif self._x_axle.draw_minor_grid:  # побочная сетка
                x0_minor = x + self.__step_grid_x / self._x_axle.minor_step_ratio
                xk_minor = x + self.__step_grid_x
                xstep_minor = self.__step_grid_x / self._x_axle.minor_step_ratio
            else:
                continue
            x_min = arange(x0_minor, xk_minor + xstep_minor / 2, xstep_minor)
            x_minor = [self._real_to_window_x(x_m) for x_m in x_min]
            self._qp.setPen(self._x_axle.pen_minor)
            for x_m in x_minor:
                if self._MIN_X < x_m < self._MAX_X and x_w != x_m:
                    self._qp.drawLine(QLineF(x_m, self._MAX_Y, x_m, self._MIN_Y))
        
        if new_x_met_width != self._x_axle.met_size:
            old_step = self.__step_grid_x
            new_step = self._update_step_x()
            old_width_px = new_step / self._real_width * self.__w
            if old_step > new_step:
                if old_width_px <= self._x_axle.met_size:
                    self._redraw_required = True
                    self.__step_grid_x = new_step
                else:
                    self.__step_grid_x = old_step

    def __draw_grid_y(self):
        font = QFont(self.__font)
        font.setBold(True)
        self._qp.setFont(font)
        self._y_axle.label_size = QFontMetrics(font).height()

        txt_pen = QPen(text_color(self.__dark))
        self._qp.setPen(txt_pen)

        if self._y_axle.draw_label:
            max_y_label_width = QFontMetrics(font).horizontalAdvance(self._y_axle.name) + 10
            self._qp.drawText(self._MIN_X - max_y_label_width - 10, self._MIN_Y, max_y_label_width, self._y_axle.label_size,
                            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, self._y_axle.name)  # имя оси У
        else:
            max_y_label_width = 0
        
        font.setBold(False)
        self._qp.setFont(font)

        y0 = round_custom(self._ystart, self._step_grid_y)

        if self._y_axle.logarithmic:
            if y0 <= 0:
                y0 += self._step_grid_y
            initial_y_power = floor(log10(self._ystart))
            end_y_power = ceil(log10(self._ystop))
            y_metki_coords = [10 ** i for i in range(initial_y_power, end_y_power + 1)]
        else:
            y_metki_coords = arange(y0, self._ystop + self._step_grid_y, self._step_grid_y)

        divised_step = self._step_grid_y / self._y_axle.divisor
        digit_count = max(get_digit_count_after_dot(round(y / self._y_axle.divisor, 10)) for y in y_metki_coords)
        digit_count = max(get_digit_count_after_dot(divised_step), digit_count)
        if divised_step < 0.5:
            digit_count = max(2, digit_count)

        for y in y_metki_coords:
            y_w = self._real_to_window_y(y)

            if self._y_axle.logarithmic:
                self._step_grid_y = y

            if self._MIN_Y < y_w < self._MAX_Y:
                if not (y == 0 and self.__draw_origin) and self._y_axle.draw_major_grid:
                    self._qp.setPen(self._y_axle.pen_major)
                    self._qp.drawLine(QLineF(self._MIN_X, y_w, self._MAX_X, y_w))
                if self._y_axle.draw_ticks:
                    self._qp.setPen(txt_pen)
                    y /=  self._y_axle.divisor
                    if self._y_axle.logarithmic:
                        power_of_ten = int(log10(y))
                        tmp_str = "10" + get_upper_index(power_of_ten)
                    else:
                        tmp_str = self.__get_rounded_tick(y, divised_step, digit_count if self._digits_count < 0 else self._digits_count)

                    tmp_str_width = QFontMetrics(font).horizontalAdvance(tmp_str) + 10
                    max_y_label_width = max(max_y_label_width, tmp_str_width)

                    if y_w > self._MIN_Y + self._y_axle.label_size + 15:
                        self._qp.drawText(QRectF(self._MIN_X - 110, y_w - 10, 100, 20),
                                          Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, tmp_str)

            if self._y_axle.logarithmic:
                y0_minor = 2 * y
                yk_minor = 10 * y
                ystep_minor = y
            elif self._y_axle.draw_minor_grid:  # побочная сетка
                y0_minor = y + self._step_grid_y / self._y_axle.minor_step_ratio
                yk_minor = y + self._step_grid_y
                ystep_minor = self._step_grid_y / self._y_axle.minor_step_ratio
            else:
                continue

            y_min = arange(y0_minor, yk_minor + ystep_minor / 2, ystep_minor)
            y_minor = [self._real_to_window_y(y_m) for y_m in y_min]
            self._qp.setPen(self._y_axle.pen_minor)
            for y_m in y_minor:
                if self._MIN_Y <= y_m <= self._MAX_Y and y_w != y_m:
                    self._qp.drawLine(QLineF(self._MIN_X, y_m, self._MAX_X, y_m))

        if self._y_axle.draw_minor_grid:
            y0_minor = y_metki_coords[0]
            yk_minor = self._ystart - self._step_grid_y
            ystep_minor = self._step_grid_y / self._y_axle.minor_step_ratio
            y_min = arange(y0_minor, yk_minor + ystep_minor / 2, -ystep_minor)
            y_minor = [self._real_to_window_y(y_m) for y_m in y_min]
            for y_m in y_minor:
                if self._MIN_Y <= y_m <= self._MAX_Y and y_w != y_m:
                    self._qp.drawLine(QLineF(self._MIN_X, y_m, self._MAX_X, y_m))

        if self._y_axle.met_size != max_y_label_width:
            self._y_axle.met_size = max_y_label_width
            self._resize_frame()

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

    def _resize_frame(self):
        self._OFFSET_X = self._y_axle.met_size
        self._MIN_X = self._OFFSET_X
        self._MAX_X = self._MIN_X + self.__w
        super().setGeometry(self.__x - self._OFFSET_X, self.__y - self._OFFSET_Y_UP, self.__w + self._OFFSET_X, self.__h + self._OFFSET_Y_UP + self._OFFSET_Y_DOWN)
        self.__btn_group.setGeometry(self._MIN_X, self._OFFSET_Y_DOWN - self._OFFSET_Y_UP, self.__w, self.__h)
        self._recalculate_window_coords()
        self._update_step_x()
        self.update()

    def _draw_scanner_lines(self, value_rects):
        line_real_coords = list()
        line_window_coords = list()

        for line in self.__scanner_lines:
            if not line.is_visible():
                continue

            x_win = self._get_line_window_coord(line)
            x_real = self._window_to_real_x(x_win - self._MIN_X)

            if self._xstart < x_real < self._xstop:
                x_real /= self._x_axle.divisor
                if self.__convert_to_hhmmss:
                    tmp_str = convert_timestamp_to_human_time(x_real + self.__initial_timestamp, millis=True)
                else:
                    digit_count = get_digit_count_after_dot(self.__step_grid_x / self._x_axle.divisor) + 1
                    tmp_str = f"{x_real:.{digit_count}f}"

                font = QFont("Consolas, Courier New", 10)
                font.setBold(True)
                self._qp.setFont(font)
                qm = self._qp.fontMetrics()
                text_width = qm.horizontalAdvance(tmp_str)  # измеряем текст

                self._qp.setPen(QColor(0, 0, 0, 0))
                self._qp.setBrush(0x00A2E8)
                rectX = x_win - text_width - 15
                if rectX < self._MIN_X:
                    rectX = x_win + 10
                rectW = text_width + 10
                rectH = qm.height() + 2
                rectY = self._MAX_Y - rectH - 3
                if rectX + rectW > self._MAX_X - 200:
                    rectY -= 27
                self._qp.drawRoundedRect(QRectF(rectX, rectY, rectW, rectH), 5, 5)
                self._value_rect_max_y = rectY - 25

                self._qp.setPen(0xFFFFFF)
                self._qp.drawText(QRectF(rectX, rectY, rectW, rectH),
                                  Qt.AlignmentFlag.AlignCenter, tmp_str)  # значение по Х

                if self.__dark:
                    col = 0x66BD6C if line.is_selected() else 0xC8C8C8
                else:
                    col = 0x66BD6C if line.is_selected() else 0
                th = 1 if False else 1
                self._qp.setPen(QPen(QColor(col), th, Qt.PenStyle.DashLine))
                self._qp.drawLine(QLineF(x_win, self._MIN_Y, x_win, self._MAX_Y))

                line_real_coords.append(x_real)
                line_window_coords.append(x_win)
            
        if len(line_real_coords) > 1:
            line_real_coords.sort()
            line_window_coords.sort()

            for i, (x_win, x_real) in enumerate(zip(line_window_coords, line_real_coords)):
                if i == 0:
                    continue

                y = self._MIN_Y + 2
                pen = QPen(0xFFFFFF if self.dark else 0)
                pen.setWidthF(1)
                pen.setStyle(Qt.PenStyle.DashDotLine)
                self._qp.setPen(pen)
                self._qp.drawLine(QLineF(x_win, y, line_window_coords[i - 1], y))

                self._qp.setPen(QColor(0, 0, 0, 0))

                dx = abs(x_real - line_real_coords[i - 1])
                if self.__convert_to_hhmmss:
                    tmp_str = convert_timestamp_to_human_time(dx, millis=True)
                else:
                    digit_count = get_digit_count_after_dot(self.__step_grid_x / self._x_axle.divisor) + 1
                    tmp_str = f"{dx:.{digit_count}f}"
                font = QFont("Consolas, Courier New", 10)
                font.setBold(True)
                self._qp.setPen(0xFFFFFF if self.dark else 0)
                self._qp.setFont(font)
                text_width = qm.size(0, tmp_str).width()
                rectW = text_width + 10
                rect_x = (min(line_window_coords[i - 1], (x_win)) +
                          (abs(line_window_coords[i - 1] - (x_win)) - rectW) // 2)
                rectY = y + 3
                if abs(line_window_coords[i - 1] - (x_win)) < rectW:
                    if rect_x > self.__w / 2:
                        rect_x -= rectW
                    else:
                        rect_x += rectW

                self._qp.drawText(QRectF(rect_x, rectY, rectW, rectH),
                                  Qt.AlignmentFlag.AlignCenter, tmp_str)

    def _draw_scale_lines(self):
        self._qp.setFont(QFont("Consolas, Courier New", 10))
        # вертикальные линии для масштабирования
        prev_val_line_coord_xwin = 0
        prev_val_line_coord_xreal = 0
        for i, line in enumerate(self.__scale_lines):
            if not line.is_visible():
                continue

            if self.__dark:
                color = 'lightblue' if line.is_selected() else QColor(85, 170, 255)
            else:
                color = 'lightblue' if line.is_selected() else 'darkblue'

            pen = QPen(QColor(color), 1)
            self._qp.setPen(pen)

            x_win = self._get_line_window_coord(line)
            x_real = self._window_to_real_x(x_win - self._MIN_X)
            
            self._qp.drawLine(QLineF(x_win, self._MIN_Y, x_win, self._MAX_Y))

            # формируем подпись со значением Х, на котором стоит линия
            x_real /= self._x_axle.divisor
            digit_count = get_digit_count_after_dot(self.__step_grid_x / self._x_axle.divisor) + 1
            tmp_str = convert_timestamp_to_human_time(x_real + self.__initial_timestamp, millis=True) \
                if self.__convert_to_hhmmss else f"{x_real:.{digit_count}f}"

            font = QFont("Consolas, Courier New", 10)
            font.setBold(True)
            self._qp.setFont(font)
            qm = QFontMetrics(font)
            text_width = qm.horizontalAdvance(tmp_str)  # измеряем текст
            text_height = qm.height()

            rectX = x_win - text_width - 15 if x_win > self.__w / 2 else x_win + 5
            rectY = self._MIN_Y + 18 + 20 * i
            rectW = text_width + 10
            rectH = text_height + 2
            self._qp.setPen(QColor(0, 0, 0, 0))
            self._qp.setBrush(0x8080)
            self._qp.drawRoundedRect(QRectF(rectX, rectY, rectW, rectH), 5, 5)
            self._qp.setPen(0xFFFFFF)
            self._qp.drawText(QRectF(round(rectX), round(rectY), rectW, rectH), Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter, tmp_str)

            if i > 0:
                y = self._MIN_Y + 2
                if self.__dark:
                    pen = QPen(0xC8C8C8)
                else:
                    pen = QPen(0)
                pen.setStyle(Qt.PenStyle.DotLine)
                self._qp.setPen(pen)
                self._qp.drawLine(QLineF(x_win, y, prev_val_line_coord_xwin, y))

                dx = abs(x_real - prev_val_line_coord_xreal)
                if self.__convert_to_hhmmss:
                    tmp_str = convert_timestamp_to_human_time(dx, millis=True)
                else:
                    digit_count = get_digit_count_after_dot(self.__step_grid_x / self._x_axle.divisor) + 1
                    tmp_str = f"{dx:.{digit_count}f}"
                font = QFont("Consolas, Courier New", 9)
                font.setBold(True)
                self._qp.setPen(text_color(self.__dark))
                self._qp.setFont(font)
                text_width = qm.size(0, tmp_str).width()
                rectW = text_width + 10
                rect_x = (min(prev_val_line_coord_xwin, x_win) +
                          (abs(prev_val_line_coord_xwin - x_win) - rectW) / 2)
                rectY = y + 3
                if abs(prev_val_line_coord_xwin - x_win) < rectW:
                    if rect_x > self._MIN_X + self.__w / 2:
                        rect_x -= rectW
                    else:
                        rect_x += rectW

                self._qp.drawText(QRectF(rect_x, rectY, rectW, rectH),
                                  Qt.AlignmentFlag.AlignCenter, tmp_str)

            prev_val_line_coord_xwin = x_win
            prev_val_line_coord_xreal = x_real

    def _draw_x_slider(self) -> None:
        """Рисование указателя положения окна просмотра относительно всей имеющейся оси Х"""
        if self.is_animated() and not self.is_paused():
            return
        if self._xstart <= self._x_axis_min and self._xstop >= self._x_axis_max:
            return

        R = 5
        x0 = self._MIN_X + round((1 - self.__slider.length - 0.01) * self.__w)
        x1 = x0 + round(self.__w * self.__slider.length)
        y0 = self.__slider.y

        self._qp.setPen(QColor(0, 0, 0, 0))
        if self.__dark:
            self._qp.setBrush(QColor(150, 150, 150, 255 if self.__slider.is_pressed() else 100))
        else:
            self._qp.setBrush(QColor(230, 230, 230, 255 if self.__slider.is_pressed() else 100))
        self._qp.drawRoundedRect(QRectF(x0, y0, x1 - x0, self.__slider.h), R, R)

        if self.__slider.is_pressed():
            color = QColor(92, 126, 170) if self.__dark else QColor(112, 146, 190)
        elif self.__slider.mouse_on():
            color = QColor(190, 190, 190, 100)
        else:
            color = QColor(150, 150, 150, 100)

        self._qp.setBrush(color)
        self._qp.drawRoundedRect(QRectF(self.__slider.x, y0, self.__slider.w, self.__slider.h), R, R)

    def _draw_scaling_rect(self):
        if self.__scaling_rect_drawing:
            # рисуем масштабирующий прямоугольничек
            if self.__dark:
                self._qp.setPen(QPen(0xC8C8C8, 1, Qt.PenStyle.DashLine))
            else:
                self._qp.setPen(QPen(0, 1, Qt.PenStyle.DashLine))
            self._qp.setBrush(QColor(0, 0, 0, 0))
            rect = QRectF(self.__scaling_rect)
            rect.setLeft(self.__scaling_rect.left() + self._MIN_X)
            rect.setRight(self.__scaling_rect.right() + self._MIN_X)
            rect.setTop(self.__scaling_rect.top() + self._MIN_Y)
            rect.setBottom(self.__scaling_rect.bottom() + self._MIN_Y)
            self._qp.drawRect(rect)
        
    def _scanner_coords(self):
        return tuple(self._get_line_window_coord(line) for line in self.__scanner_lines)
    
    def _scanner_count(self):
        return self.__scanner_lines.line_count()
    
    def enable_human_time_display(self):
        if self._x_axle.logarithmic:
            return
        self._redraw_required = True
        self.__convert_to_hhmmss = True

    def disable_human_time_display(self):
        self._redraw_required = True
        self.__convert_to_hhmmss = False

    def human_time_display_enabled(self) -> bool:
        return self.__convert_to_hhmmss

    def set_x_autoscale(self, state: bool):
        if self._x_axle.autoscale == state:
            return
        if state:
            self._set_x_start(self.x_axis_min)
            self._set_x_stop(self.x_axis_max)
            self._update_step_x()
            self.__group.update_x_borders(self._xstart, self._xstop)
        self._recalculate_window_coords()
        self._x_axle.autoscale = state
        self._redraw_required = True

    def set_y_autoscale(self, state: bool):
        if self._y_axle.autoscale == state:
            return
        
        if state:
            self._calculate_y_parameters()
        self._update_step_y()
        
        self._recalculate_window_coords()
        self._y_axle.autoscale = state
        self._redraw_required = True

    def set_step_x(self, step: int):
        if step <= 0 or step > self._real_width or step == self.__step_grid_x:
            return
        self.__step_grid_x = step
        self._redraw_required = True

    def set_step_y(self, step: int):
        if step <= 0 or step > self._real_height or step == self._step_grid_y:
            return
        self._step_grid_y = step
        self._redraw_required = True

    def set_x_borders(self, xmin: float, xmax: float):
        if self._x_axle.autoscale or xmin >= xmax:
            return
        self._set_x_start(xmin)
        self._set_x_stop(xmax)
        self._recalculate_window_coords()
        self.__group.update_x_borders(self._xstart, self._xstop)
        self._redraw_required = True

    def set_x_start(self, x: float):
        if self._x_axle.autoscale or x >= self._xstop:
            return
        if self._xstart == x:
            return
        self._set_x_start(x)
        self.__group.update_x_borders(self._xstart, self._xstop)
        self._recalculate_window_coords()
        self._redraw_required = True

    def set_x_stop(self, x: float):
        if self._x_axle.autoscale or x <= self._xstart:
            return
        if self._xstop == x:
            return
        self._set_x_stop(x)
        self.__group.update_x_borders(self._xstart, self._xstop)
        self._recalculate_window_coords()
        self._redraw_required = True

    def set_y_borders(self, ymin: float, ymax: float):
        if self._y_axle.autoscale or ymin >= ymax:
            return
        if self._ystart == ymin and self._ystop == ymax:
            return
        self._set_y_start(ymin)
        self._set_y_stop(ymax)
        self._calculate_y_parameters()
        self._recalculate_window_coords()
        self._redraw_required = True

    def set_y_start(self, y: float):
        if self._y_axle.autoscale or y >= self._ystop:
            return
        if self._ystart == y:
            return
        self._set_y_start(y)
        self._update_step_y()
        self._recalculate_window_coords()
        self._redraw_required = True

    def set_y_stop(self, y: float):
        if self._y_axle.autoscale or y <= self._ystart:
            return
        if self._ystop == y:
            return
        self._set_y_stop(y)
        self._update_step_y()
        self._recalculate_window_coords()
        self._redraw_required = True

    def enable_major_grid_x(self, enable: bool):
        if self._x_axle.draw_major_grid != enable:
            self._redraw_required = True
        self._x_axle.draw_major_grid = enable

    def enable_minor_grid_x(self, enable: bool):
        if self._x_axle.draw_minor_grid != enable:
            self._redraw_required = True
        self._x_axle.draw_minor_grid = enable

    def enable_major_grid_y(self, enable: bool):
        if self._y_axle.draw_major_grid != enable:
            self._redraw_required = True
        self._y_axle.draw_major_grid = enable

    def enable_minor_grid_y(self, enable: bool):
        if self._y_axle.draw_minor_grid != enable:
            self._redraw_required = True
        self._y_axle.draw_minor_grid = enable

    def enable_origin_drawing_x(self, enable: bool, width=1.0):
        if enable != self._x_axle.draw_ax or width != self._x_axle.origin_pen.widthF():
            self._redraw_required = True
        self._x_axle.draw_ax = enable
        if 0.25 <= width <= 4:
            self._x_axle.origin_pen.setWidthF(width)

    def enable_origin_drawing_y(self, enable: bool, width=1.0):
        if enable != self._y_axle.draw_ax or width != self._y_axle.origin_pen.widthF():
            self._redraw_required = True
        self._y_axle.draw_ax = enable
        if 0.25 <= width <= 4:
            self._y_axle.origin_pen.setWidthF(width)

    def set_major_grid_style_x(self, style: str, width=1.0):
        match style:
            case "dot":
                self._x_axle.pen_major.setStyle(Qt.PenStyle.DotLine)
            case "dash":
                self._x_axle.pen_major.setStyle(Qt.PenStyle.DashLine)
            case "solid":
                self._x_axle.pen_major.setStyle(Qt.PenStyle.SolidLine)
        self._x_axle.pen_major.setWidthF(width)
        self._redraw_required = True

    def set_minor_grid_style_x(self, style="dot", width=1.0, step_ratio=5):
        match style:
            case "dot":
                self._x_axle.pen_minor.setStyle(Qt.PenStyle.DotLine)
            case "dash":
                self._x_axle.pen_minor.setStyle(Qt.PenStyle.DashLine)
            case "solid":
                self._x_axle.pen_minor.setStyle(Qt.PenStyle.SolidLine)
        self._x_axle.pen_minor.setWidthF(width)
        if step_ratio > 0:
            self._x_axle.minor_step_ratio = step_ratio
        self._redraw_required = True

    def set_major_grid_style_y(self, style: str, width=1.0):
        match style:
            case "dot":
                self._y_axle.pen_major.setStyle(Qt.PenStyle.DotLine)
            case "dash":
                self._y_axle.pen_major.setStyle(Qt.PenStyle.DashLine)
            case "solid":
                self._y_axle.pen_major.setStyle(Qt.PenStyle.SolidLine)
        self._y_axle.pen_major.setWidthF(width)
        self._redraw_required = True

    def set_minor_grid_style_y(self, style="dot", width=1.0, step_ratio=5):
        match style:
            case "dot":
                self._y_axle.pen_minor.setStyle(Qt.PenStyle.DotLine)
            case "dash":
                self._y_axle.pen_minor.setStyle(Qt.PenStyle.DashLine)
            case "solid":
                self._y_axle.pen_minor.setStyle(Qt.PenStyle.SolidLine)
        self._y_axle.pen_minor.setWidthF(width)
        if step_ratio > 0:
            self._y_axle.minor_step_ratio = step_ratio
        self._redraw_required = True

    @Slot(bool)
    def enable_x_ticks(self, enable: bool):
        if enable != self._x_axle.draw_ticks:
            self._redraw_required = True
        self._x_axle.draw_ticks = enable

    @Slot(bool)
    def enable_y_ticks(self, enable: bool):
        if enable != self._y_axle.draw_ticks:
            self._redraw_required = True
        self._y_axle.draw_ticks = enable

    @Slot(bool)
    def enable_x_label(self, enable: bool):
        if enable != self._x_axle.draw_label:
            self._redraw_required = True
        self._x_axle.draw_label = enable

    @Slot(bool)
    def enable_y_label(self, enable: bool):
        if enable != self._y_axle.draw_label:
            self._redraw_required = True
        self._y_axle.draw_label = enable

    def _show_extended_window(self):
        ...
    
    @Slot(bool)
    def pause(self, pause: bool):
        if pause != self.__paused:
            self.__btn_group.pause(pause)
            self.__group.pause_signal.emit(pause)
        self.__paused = pause
        self._redraw_required = True

    @Slot(bool)
    def __pause(self, pause: bool):
        if pause != self.__paused:
            self.__btn_group.pause(pause)
        self.__paused = pause
        self._redraw_required = True

    @Slot()
    def restart_animation(self, **kwargs):
        if "signal" in kwargs and kwargs["signal"]:
            self.__group.restart_signal.emit(self)

    @Slot(object)
    def __restart_animation(self, sender: object):
        if sender is not self:
            self.restart_animation()

    def set_x_logarithmic(self, log: bool) -> bool:
        if self._x_axle.logarithmic != log:
            if log:
                if self.is_animated():
                    return False
                if self._x_axis_min < 0:
                    warnings.warn("Область определения содержит значения меньше или равные нулю. Логарифмический масштаб не может быть установлен.", stacklevel=2)
                    return False
                elif self._x_axis_min == 0:
                    self._set_x_start(0.01)
                    self._x_axis_min = 0
                self.disable_human_time_display()
                self._real_to_window_x = self.__real_to_window_x_log
                self._window_to_real_x = self.__window_to_real_x_log
            else:
                self._real_to_window_x = self.__real_to_window_x_linear
                self._window_to_real_x = self.__window_to_real_x_linear
            self._x_axle.logarithmic = log
            self._recalculate_window_coords()
            self._update_step_x()
            self._redraw_required = True
        return True

    def set_y_logarithmic(self, log: bool):
        if self._y_axle.logarithmic != log:
            if log:
                if self.is_animated():
                    return False
                if self._y_axis_min < 0:
                    warnings.warn("Область значений содержит значения меньше или равные нулю. Логарифмический масштаб не может быть установлен.", stacklevel=2)
                    return False
                else:
                    self._set_y_start(self._y_axis_min)
                self._real_to_window_y = self.__real_to_window_y_log
                self._window_to_real_y = self.__window_to_real_y_log
            else:
                self._real_to_window_y = self.__real_to_window_y_linear
                self._window_to_real_y = self.__window_to_real_y_linear
                self._calculate_y_parameters()
            self._y_axle.logarithmic = log
            self._recalculate_window_coords()
            self._update_step_y()
            self._redraw_required = True
            return True

    def set_x_divisor(self, divisor: int):
        if divisor < 1:
            return
        if divisor != self._x_axle.divisor:
            self._x_axle.divisor = divisor
            self._update_step_x()
            self._redraw_required = True

    def set_y_divisor(self, divisor: int):
        if divisor < 1:
            return
        if divisor != self._y_axle.divisor:
            self._y_axle.divisor = divisor
            self._update_step_y()
            self._redraw_required = True

    @Slot(QFont)
    def set_font(self, font: QFont):
        if font:
            self.__font = font
            self._redraw_required = True
    
    @property 
    def x_name(self):
        return self._x_axle.name
    
    @property
    def y_name(self):
        return self._y_axle.name
    
    @property
    def x_ticks_enabled(self):
        return self._x_axle.draw_ticks
    
    @property
    def y_ticks_enabled(self):
        return self._y_axle.draw_ticks
    
    @property
    def x_label_enabled(self):
        return self._x_axle.draw_label
    
    @property
    def y_label_enabled(self):
        return self._y_axle.draw_label
    
    @property
    def origin_is_drawing(self):
        return self.__draw_origin
    
    @property
    def step_x(self):
        return self.__step_grid_x
    
    @property
    def step_y(self):
        return self._step_grid_y
    
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
    def x_major_ticks_enabled(self):
        return self._x_axle.draw_major_grid
    
    @property
    def x_minor_ticks_enabled(self):
        return self._x_axle.draw_minor_grid
    
    @property
    def y_major_ticks_enabled(self):
        return self._y_axle.draw_major_grid
    
    @property
    def y_minor_ticks_enabled(self):
        return self._y_axle.draw_minor_grid
    
    @property
    def x_axis_min(self):
        return self._x_axis_min
    
    @property
    def x_axis_max(self):
        return self._x_axis_max
    
    @property
    def x_major_grid_width(self):
        return self._x_axle.pen_major.widthF()
    
    @property
    def x_minor_grid_width(self):
        return self._x_axle.pen_minor.widthF()
    
    @property
    def x_major_grid_style(self):
        return self._x_axle.pen_major.style().name
    
    @property
    def x_minor_grid_atyle(self):
        return self._x_axle.pen_minor.style().name
    
    @property
    def y_major_grid_width(self):
        return self._y_axle.pen_major.widthF()
    
    @property
    def y_minor_grid_width(self):
        return self._y_axle.pen_minor.widthF()
    
    @property
    def y_major_grid_style(self):
        return self._y_axle.pen_major.style().name
    
    @property
    def y_minor_grid_atyle(self):
        return self._y_axle.pen_minor.style().name
    
    def set_dark(self, dark: bool):
        if dark != self.__dark:
            self.__background_color = background_color(self.__dark)
            self.__btn_group.set_dark(dark)
            self._redraw_required = True
            self.__dark = dark

    def _set_buttons_visible(self, visible: bool):
        self.__btn_group.set_buttons_visible(visible)

    def set_background_color(self, color: QColor):
        self.__background_color = color
        self._redraw_required = True

    @property
    def background_color(self) -> QColor:
        return self.__background_color
    
    @property
    def x_is_logarithmic(self) -> bool:
        return self._x_axle.logarithmic
    
    @property
    def y_is_logarithmic(self) -> bool:
        return self._y_axle.logarithmic

    @property
    def dark(self):
        return self.__dark
    
    @property
    def font(self) -> QFont:
        return self.__font
    
    def _get_line_window_coord(self, line):
        return self._MIN_X + (self._MAX_X - self._MIN_X) * line.x()

    def _get_line_real_coord(self, line):
        return self._xstart + self._real_width * line.x()
    
    @Slot(int)
    def set_digits_count(self, count: int):
        if self._digits_count != count:
            self._redraw_required = True
        if count < 0:
            self._digits_count = -1
        count = min(count, 6)
        self._digits_count = count
            
    