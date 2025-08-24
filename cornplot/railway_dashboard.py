import math as mt
from collections.abc import Iterable

from PyQt5.QtGui import QPolygonF, QPen, QColor, QFont
from PyQt5.QtCore import QPointF, QRectF, Qt, QLineF

from .dashboard import Dashboard
from .railway.semaphore import SemaphoreColor
from .railway.train_data import TrainData
from .railway.track_data import TrackData
try:
    from track_profile import SlopeCreator

    class RailwayDashboard(Dashboard):

        def __init__(self, widget, x, y, w, h, kilometers=True, draw_track_data=True):
            super().__init__(widget, x, y, w, h)

            self.set_x_name("x, км" if kilometers else "x, м")
            self.set_y_name("h, м")

            if kilometers:
                self.set_x_divisor(1000)

            self.__train_data = TrainData()
            self.__track_data = TrackData(widget)

            self.__follow_train = False

            self.__profile_data = None
            self.__four_digits = True
            self.__draw_track_data = draw_track_data

            if kilometers:
                self._x_div = 1000

            self.__km = kilometers

            self._Y_STOP_RATIO = 4

        def set_track_data_visible(self, visible: bool):
            self.__draw_track_data = visible

        def set_dark(self, dark: bool):
            super().set_dark(dark)

            self.__track_data.set_dark(dark)
            self.__train_data.set_dark(dark)

        def set_profile(self, profile: SlopeCreator):
            if self.__profile_data is not profile:
                self.delete_all_plots()
                heights = profile.get_absolute_heights()
                self.add_plot(heights[0], heights[1], name="Высота пути", color=0x999999)
                self.__track_data.clear()

                if profile.semaphores:
                    for s in profile.semaphores:
                        self.add_semaphore(s.coord, s.name, profile.four_digit_blocking)
                if profile.stations:
                    for s in profile.stations:
                        self.add_station(s.coord, s.name, s.length)
                self.__profile_data = profile
                self.__recalculate_track_data_coords()

        def fix_y_zero(self, fix: bool) -> None:
            if self.__train_data is None:
                super().fix_y_zero(fix)

            self.__follow_train = not self.__follow_train

        def add_station(self, coord: float, name: str, length: float):
            self.__track_data.add_station(coord, name, length, self.dark)

        def add_semaphore(self, coord: float, name: str, four_digit: bool):
            self.__track_data.add_semaphore(coord, name, self.dark, four_digit=four_digit)

        def add_train(self, number: str, lengths: Iterable[float], colors: None | Iterable[str | QColor | int] = None):
            self.__train_data.add_train(number, lengths, colors)

        def update_train(self, number: str, first_car_coord_m: float):
            self.__train_data.update_train(number, first_car_coord_m)
            self._force_redraw()

        def __redraw_trains(self):
            coord_changed = False
            if self.__profile_data is None:
                return
            
            if self.height() == 0:
                return
            if len(self.__profile_data) == 0:
                return

            first = True
            for num, train in self.__train_data.trains.items():
                coords = []
                h = train.h

                if self.__profile_data.cyclic:
                    X = [x % len(self.__profile_data) for x in train.X]
                else:
                    X = train.X

                if self.__follow_train and first:
                    w = self._real_width
                    xtrg = X[0] - w / 2
                    if xtrg + w <= self._x_axis_max and xtrg >= self._x_axis_min:
                        self._set_x_start(xtrg)
                        self._set_x_stop(self._xstart + w)
                        self._update_x_borders(xtrg, self._xstart + w)
                    coord_changed = True
                    first = False

                x_stop = []
                yup = []
                ydown = []

                n_cars = len(train.X)
                self._qp.setFont(QFont("Consolas, Courier New", 10))
                if abs(self._real_to_window_x(train.X[0]) - self._real_to_window_x(train.X[-1])) <= 15:
                    x = self._real_to_window_x(X[0])
                    y = self._real_to_window_y(self.__profile_data.get_absolute_height(X[0]))
                    adder = (self._ystop - self._ystart) / (self._MAX_Y - self._MIN_Y) * 5
                    ydown.append(y)
                    y -= adder
                    self._qp.setPen(QPen(QColor(128, 128, 128), 1, Qt.PenStyle.DashDotDotLine))
                    self._qp.drawLine(QLineF(x, y, x, self._MAX_Y))
                    self._qp.drawText(QPointF(x + 5, self._MAX_Y - 14), str(num))
                    self._qp.drawText(QPointF(x + 5, self._MAX_Y - 2), f"x = {X[0] / self._x_axle.divisor:.2f} {'км' if self.__km else 'м'}; v = {train.speed:3.1f} км/ч")
                    self._qp.setPen(QPen(QColor(0xFF8000), 10, cap=Qt.PenCapStyle.SquareCap))
                    self._qp.drawPoint(QPointF(x, y))

                    x_stop.append(x + 5)

                    yup.append(y)
                else:
                    first_car = True
                    for x, l in zip(X, train.L):
                        if self._xstart < x < self._xstop + l:
                            x0 = max(x - l, self._xstart)
                            xk = min(x, self._xstop)
                            y0 = self.__profile_data.get_absolute_height(x0)
                            yk = self.__profile_data.get_absolute_height(xk)

                            if self.__follow_train:
                                delta = 0.4
                                up_point = max(y0, yk)
                                down_point = min(y0, yk)
                                hh = self._real_height
                                if up_point + delta >= self._ystop:
                                    if up_point + delta <= self._y_axis_max:
                                        self.set_y_stop(up_point + delta)
                                        self.set_y_start(self._ystop - hh)
                                        coord_changed = True

                                if down_point - delta <= self._ystart:
                                    if down_point - delta >= self._y_axis_min:
                                        self.set_y_start(down_point - delta)
                                        self.set_y_stop(self._ystart + hh)
                                        coord_changed = True
                            if not (self._ystart < y0 < self._ystop):
                                continue

                            ywin0 = self._real_to_window_y(y0)
                            ywink = self._real_to_window_y(yk)
                            xwin0 = self._real_to_window_x(x0)
                            xwink = self._real_to_window_x(xk)

                            if xwink - xwin0 < 1:
                                xwink = xwin0 + 1
                            angle = mt.atan2((ywin0 - ywink), (xwink - xwin0))

                            xp0 = xwin0
                            yp0 = ywin0

                            h1 = h
                            xp1 = xwin0 - h1 * mt.sin(angle)
                            yp1 = ywin0 - h1 * mt.cos(angle)

                            h2 = h
                            xp2 = xwink - h2 * mt.sin(angle)
                            yp2 = ywink - h2 * mt.cos(angle)

                            xp3 = xwink
                            yp3 = ywink

                            yup.append(min(yp0, yp1, yp2, yp3))
                            ydown.append(max(yp0, yp1, yp2, yp3))
                            x_stop.append(xp3)

                            lst = [QPointF(xp0, yp0),
                                   QPointF(xp1, yp1),
                                   QPointF(xp2, yp2),
                                   QPointF(xp3, yp3)]
                            polygon = QPolygonF(lst)
                            coords.append(polygon)

                            if first_car:
                                first_car = False
                                self._qp.setPen(QPen(QColor(128, 128, 128), 1, Qt.PenStyle.DashDotDotLine))
                                self._qp.drawLine(QLineF(xwink, ywin0, xwink, self._MAX_Y))

                                self._qp.drawText(QPointF(xwink + 5, self._MAX_Y - 14), str(num))
                                self._qp.drawText(QPointF(xwink + 5, self._MAX_Y - 2), f"x = {X[0] / self._x_axle.divisor:.2f} {'км' if self.__km else 'м'}; v = {train.speed:3.1f} км/ч")

                    train.draw(self._qp, coords, compact=abs(self._real_to_window_x(X[0]) - self._real_to_window_x(X[-1])) / n_cars < 2)

            if coord_changed:
                self._recalculate_window_coords()

        def __manage_semaphores(self):
            if len(self.__track_data.semaphores) < 3:
                return

            empty_sectors = list()
            for i, s in enumerate(self.__track_data.semaphores):
                on_sector = []
                for train in self.__train_data.trains.values():
                    if self.__profile_data.cyclic:
                        X = [x % len(self.__profile_data) for x in train.X]
                    else:
                        X = train.X

                    if i == len(self.__track_data.semaphores) - 1:
                        train_on_sector = (X[-1] > s.x or X[-1] < self.__track_data.semaphores[0].x or
                                           X[0] > s.x or X[0] < self.__track_data.semaphores[0].x)
                    else:
                        train_on_sector = (s.x < X[-1] < self.__track_data.semaphores[i + 1].x or
                                           s.x < X[0] < self.__track_data.semaphores[i + 1].x)
                    on_sector.append(train_on_sector)
                empty_sectors.append(not any(on_sector))

            for i in range(3):
                empty_sectors.append(empty_sectors[i])

            for i, s in enumerate(self.__track_data.semaphores):
                n_empty_sectors = 0
                for e in empty_sectors[i:]:
                    if e:
                        n_empty_sectors += 1
                    else:
                        break

                if n_empty_sectors == 0:
                   color = SemaphoreColor.red
                elif n_empty_sectors == 1:
                    color = SemaphoreColor.yellow
                elif n_empty_sectors == 2:
                    color = SemaphoreColor.green_yellow if self.__four_digits else SemaphoreColor.green
                else:
                    color = SemaphoreColor.green
                s.set_color(color)

        def _recalculate_window_coords(self) -> None:
            super()._recalculate_window_coords()
            self.__recalculate_track_data_coords()

        def __recalculate_track_data_coords(self):
            for semphr in self.__track_data.semaphores:
                semphr.x_win = self._real_to_window_x(semphr.x)
                semphr.y_real = self.__profile_data.get_absolute_height(semphr.x)
                semphr.y_win = self._real_to_window_y(semphr.y_real)
            for station in self.__track_data.stations:
                x0 = max(station.x, self._xstart)
                xk = min(station.x + station.l, self._xstop)

                y0 = self.__profile_data.get_absolute_height(x0)
                yk = self.__profile_data.get_absolute_height(xk)

                station.y0_real = y0
                station.yk_real = yk
                x0 = self._real_to_window_x(x0)
                y0 = self._real_to_window_y(y0) - 1
                xk = self._real_to_window_x(xk)
                yk = self._real_to_window_y(yk) - 1

                station.polygon = QPolygonF([
                    QPointF(x0, y0),
                    QPointF(x0, y0 - station.h),
                    QPointF(xk, yk - station.h),
                    QPointF(xk, yk)
                ])

        def __redraw_track_data(self):
            if self.__track_data is None or not self.__draw_track_data:
                return

            for semphr in self.__track_data.semaphores:
                if self._xstart < semphr.x < self._xstop:
                    semphr.draw(self._qp, semphr.x_win, semphr.y_win, up=(semphr.y_win - 2*semphr.r - semphr.h) > self._MIN_Y)


            for station in self.__track_data.stations:
                if not (self._xstart - station.l < station.x < self._xstop):
                    continue

                station.draw(self._qp, up_txt=(station.polygon[0].y() - 40 - station.h) > self._MIN_Y)

        def _redraw(self):
            if not self.visible:
                return
            
            super()._redraw()
            self._qp.setClipRect(QRectF(self._MIN_X, self._MIN_Y - 1, self.width(), self.height() - self._OFFSET_Y_UP - self._OFFSET_Y_DOWN + 1))
            self.__redraw_track_data()
            self.__redraw_trains()
            self._qp.setClipRect(QRectF(0, 0, self.width(), self.height()))
            self.__manage_semaphores()

except ModuleNotFoundError:
    pass