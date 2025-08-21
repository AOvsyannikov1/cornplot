import math as mt

from PyQt6.QtGui import QPainter, QPolygonF, QFont, QFontMetrics, QPen, QColor
from PyQt6.QtCore import QPointF, QRectF, Qt

from .dashboard import Dashboard
from .railway.semaphore import SemaphoreColor
from .railway.train_data import TrainData
from .railway.track_data import TrackData
try:
    from track_profile import SlopeCreator

    class RailwayDashboard(Dashboard):

        def __init__(self, widget, x, y, w, h, dark=False, km=True, draw_track_data=True):
            super().__init__(widget, x, y, h, w, dark=dark, x_name="x, км" if km else "x, м", y_name="h, м")

            self.__train_data = TrainData(dark)
            self.__track_data = TrackData(widget)

            self.__follow_train = False

            self.__profile_data = None
            self.__four_digits = True
            self.__draw_track_data = draw_track_data

            if km:
                self._x_div = 1000

            self._Y_STOP_RATIO = 4

        def set_track_data_visible(self, visible: bool):
            self.__draw_track_data = visible

        def set_theme(self, dark: bool):
            super().set_theme(dark)

            self.__track_data.set_dark(dark)
            self.__train_data.set_dark(dark)

        def set_profile(self, profile: SlopeCreator):
            if self.__profile_data is not profile:
                self.delete_all_plots()
                self.add_plot(*profile.get_absolute_heights(), name="Высота пути", color=0x999999)
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

        def add_station(self, coord, name, length):
            self.__track_data.add_station(coord, name, length, self._dark)

        def add_semaphore(self, coord, name, four_digit):
            self.__track_data.add_semaphore(coord, name, self._dark, four_digit=four_digit)

        def add_train(self, number, lengths, colors = None):
            self.__train_data.add_train(number, lengths, colors)

        def update_train(self, number, car_coords):
            self.__train_data.update_train(number, car_coords)

        def __redraw_train(self, qp):
            coord_changed = False
            if self.__profile_data is None:
                return
            
            if self.h() == 0:
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
                        self.set_x_start(xtrg)
                        self.set_x_stop(self._xstart + w)
                    coord_changed = True
                    first = False

                x_stop = []
                yup = []
                ydown = []

                n_cars = len(train.X)

                if abs(self.real_to_window_x(train.X[0]) - self.real_to_window_x(train.X[-1])) <= 10:
                    x = self.real_to_window_x(X[0])
                    y = self.real_to_window_y(self.__profile_data.get_absolute_height(X[0]))
                    adder = (self._ystop - self._ystart) / self.h() * 5
                    ydown.append(y)
                    y -= adder
                    qp.setPen(QPen(QColor(0xFF8000), 10, cap=Qt.PenCapStyle.SquareCap))
                    qp.drawPoint(QPointF(x, y))

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

                            ywin0 = self.real_to_window_y(y0)
                            ywink = self.real_to_window_y(yk)
                            xwin0 = self.real_to_window_x(x0)
                            xwink = self.real_to_window_x(xk)

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

                            # h2 = min(h2, self.__y + self.__h + h - yp3)
                            # xp3 = xp2 - h2 * mt.sin(-angle)
                            # yp3 = yp2 + h2 * mt.cos(angle)

                            lst = [QPointF(xp0, yp0),
                                   QPointF(xp1, yp1),
                                   QPointF(xp2, yp2),
                                   QPointF(xp3, yp3)]
                            polygon = QPolygonF(lst)
                            coords.append(polygon)
                        first_car = False

                    train.draw(qp, coords, compact=abs(self.real_to_window_x(X[0]) - self.real_to_window_x(X[-1])) / n_cars < 2)

                if x_stop:
                    x_stop = max(x_stop)
                    yup = yup[0]
                    ydown = max(ydown)

                    h = 15
                    font = QFont('consolas', 10)
                    qp.setFont(font)

                    w = QFontMetrics(font).horizontalAdvance(str(num))

                    if yup - h - 5 <= self._y:
                        rect = QRectF(x_stop - w, ydown, w, h)
                    else:
                        rect = QRectF(x_stop - w, yup - h - 5, w, h)
                    if train.dark:
                        qp.setPen(QColor(250, 250, 250))
                    else:
                        qp.setPen(QColor(0, 0, 0))
                    qp.drawText(rect, Qt.AlignmentFlag.AlignRight, str(num))

            if coord_changed:
                self.recalculate_window_coords()

        def manage_semaphores(self):
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

        def recalculate_window_coords(self) -> None:
            super().recalculate_window_coords()
            self.__recalculate_track_data_coords()

        def __recalculate_track_data_coords(self):
            for semphr in self.__track_data.semaphores:
                semphr.x_win = self.real_to_window_x(semphr.x)
                semphr.y_real = self.__profile_data.get_absolute_height(semphr.x)
                semphr.y_win = self.real_to_window_y(semphr.y_real)
            for station in self.__track_data.stations:
                x0 = max(station.x, self._xstart)
                xk = min(station.x + station.l, self._xstop)

                y0 = self.__profile_data.get_absolute_height(x0)
                if not (self._ystart < y0 < self._ystop):
                    continue
                yk = self.__profile_data.get_absolute_height(xk)
                if not (self._ystart < yk < self._ystop):
                    continue

                station.y0_real = y0
                station.yk_real = yk
                x0 = self.real_to_window_x(x0)
                y0 = self.real_to_window_y(y0) - 1
                xk = self.real_to_window_x(xk)
                yk = self.real_to_window_y(yk) - 1

                station.polygon = QPolygonF([
                    QPointF(x0, y0),
                    QPointF(x0, y0 - station.h),
                    QPointF(xk, yk - station.h),
                    QPointF(xk, yk)
                ])

        def __redraw_track_data(self, qp):
            if self.__track_data is None or not self.__draw_track_data:
                return

            for semphr in self.__track_data.semaphores:
                if self._xstart < semphr.x < self._xstop:
                    if not (self._ystart < semphr.y_real < self._ystop):
                        continue
                    semphr.draw(qp, semphr.x_win, semphr.y_win, up=(semphr.y_win - 2*semphr.r - semphr.h) > self._y)


            for station in self.__track_data.stations:
                if not (self._xstart - station.l < station.x < self._xstop):
                    continue

                if not (self._ystart < station.y0_real < self._ystop):
                    continue
                if not (self._ystart < station.yk_real < self._ystop):
                    continue

                station.draw(qp, up_txt=(station.polygon[0].y() - 40 - station.h) > self._y)


        def redraw_plots(self):
            if not self._visible:
                return

            self.check_graph_visibility()
            self.update_extended_window()

            self._qp.begin(self._widget)
            self._qp.setRenderHint(QPainter.RenderHint.Antialiasing)
            self._qp.setRenderHint(QPainter.RenderHint.TextAntialiasing)
            self._qp.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
            self._draw_axes()

            self._redraw_without_qp()
            self.__redraw_track_data(self._qp)
            self.__redraw_train(self._qp)
            self.manage_semaphores()


            self._qp.end()
except ModuleNotFoundError:
    pass