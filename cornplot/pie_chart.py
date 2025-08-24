import numpy as np
from PyQt6 import QtCore, QtWidgets, QtGui

from .color_generator import ColorGenerator


class PieCathegory:

    def __init__(self, cat_value, total_value, name, ext_info='', color='blue'):
        self.value = cat_value
        self.total = total_value
        self.name = name
        self.ext_info = ext_info
        self.brush = QtGui.QBrush(QtGui.QColor(color))
        self.start_angle = 0
        self.angle_length = 0
        self.selected = False


class PieChart:

    def __init__(self, widget, x, y, width, name="Круговая диаграмма"):
        self.__x = x
        self.__name = name
        self.__widget = widget
        self.__y = y
        self.__w = width
        self.__h = width
        self.__kd = 0.8
        self.__D = int(self.__kd * width)
        self.__qp = QtGui.QPainter()
        self.__cathegories = list()
        self.__color_generator = ColorGenerator()
        self.__redraw_flag = True
        self.__legend_width = 50

        self.__rect = QtCore.QRect(int(self.__x + (1 - self.__kd) * self.__w // 2),
                                   int(self.__y + (1 - self.__kd) * self.__w // 2) + 10, self.__D, self.__D)

        self.__frame = QtWidgets.QFrame(widget)
        self.__frame.setGeometry(self.__x, self.__y, self.__w, self.__w)
        self.__frame.setMouseTracking(True)
        self.__frame.mouseMoveEvent = self.mouse_move_event
        self.__frame.mousePressEvent = self.mouse_press_event
        self.__frame.mouseReleaseEvent = self.mouse_release_event
        self.__frame.wheelEvent = self.wheel_event
        self.__frame.mouseDoubleClickEvent = self.mouse_double_click_event
        self.__frame.show()

        self.__info_rect_geometry = list()
        self.__info_rect_data = list()
        self.__info_rect_fixed = list()
        self.__info_rect_font = QtGui.QFont("Bahnschrift, Arial", 10)

    def needs_redrawing(self):
        return self.__redraw_flag

    def mouse_in_circle(self, x, y):
        x -= (self.__w - self.__legend_width) // 2
        y -= self.__h // 2 + 10
        return x ** 2 + y ** 2 <= (self.__D // 2) ** 2

    def setGeometry(self, x: int, y: int, w: int, h: int) -> None:
        if x == self.__x and y == self.__y and w == self.__w and self.__h == h:
            return
        old_x = int(self.__x + (self.__w - self.__legend_width) // 2)
        old_y = int(self.__y + self.__h // 2) + 10
        if x > 0:
            self.__x = x
        if y > 0:
            self.__y = y
        if w > 10:
            self.__w = w
        if h > 10:
            self.__h = h
        self.__D = int(self.__kd * (self.__w - self.__legend_width))
        if self.__D >= self.__kd * self.__h:
            self.__D = int(self.__kd * self.__h)

        new_x = int(self.__x + (self.__w - self.__legend_width) // 2)
        new_y = int(self.__y + self.__h // 2) + 10
        self.__rect = QtCore.QRect(new_x - self.__D // 2, new_y - self.__D // 2, self.__D, self.__D)
        self.__frame.setGeometry(self.__x, self.__y, (self.__w - self.__legend_width), self.__h)
        self.__redraw_flag = True
        for i in range(len(self.__info_rect_geometry)):
            if self.__info_rect_geometry[i][0] == -1:
                continue
            self.__info_rect_geometry[i][0] += (new_x - old_x)
            self.__info_rect_geometry[i][1] += (new_y - old_y)

    @staticmethod
    def vector_angle(x, y):
        return np.arctan2(y, x) + (2 * np.pi if y < 0 else 0)

    def mouse_coords_to_angle(self, x, y):
        x -= (self.__w - self.__legend_width) // 2
        y -= self.__h // 2 + 10
        y = -y
        return round(self.vector_angle(x, y) * 180 / np.pi)

    def get_cathegory_index(self, x, y):
        angle = self.mouse_coords_to_angle(x, y)
        for i, cat in enumerate(self.__cathegories):
            if cat.start_angle <= angle <= cat.start_angle + cat.angle_length:
                return i
        return -1

    def mouse_move_event(self, event: QtGui.QMouseEvent):
        x = event.pos().x()
        y = event.pos().y()
        if not self.mouse_in_circle(x, y):
            for cat in self.__cathegories:
                cat.selected = False
            return
        index = self.get_cathegory_index(x, y)
        for i, cat in enumerate(self.__cathegories):
            cat.selected = (i == index)
        self.__redraw_flag = True

    def mouse_press_event(self, event: QtGui.QMouseEvent):
        x = event.pos().x()
        y = event.pos().y()
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            if self.mouse_in_circle(x, y):
                cat_index = self.get_cathegory_index(x, y)
                cathegory = self.__cathegories[cat_index]
                self.__info_rect_geometry[cat_index][0] = x + self.__x
                self.__info_rect_geometry[cat_index][1] = y + self.__y
                self.__info_rect_data[cat_index] = cathegory.name + ' - ' + str(cathegory.value) + '%' + '\n' + \
                    cathegory.ext_info
                qm = QtGui.QFontMetrics(self.__info_rect_font)
                self.__info_rect_geometry[cat_index][2] = qm.size(0,
                                                                  self.__info_rect_data[cat_index]).width() + 10
                self.__info_rect_geometry[cat_index][3] = qm.size(0,
                                                                  self.__info_rect_data[cat_index]).height() + 10
                self.__redraw_flag = True

    def mouse_release_event(self, event: QtGui.QMouseEvent):
        pass

    def wheel_event(self, event: QtGui.QMouseEvent):
        pass

    def mouse_double_click_event(self, event: QtGui.QMouseEvent):
        if event.button() == QtCore.Qt.MouseButton.RightButton:
            for i in range(len(self.__cathegories)):
                self.__info_rect_geometry[i][0] = -1
                self.__info_rect_geometry[i][1] = -1
                self.__info_rect_geometry[i][2] = 0
                self.__info_rect_geometry[i][3] = 0
            self.__redraw_flag = True

    def add_cathegory(self, percentage: float, name: str, extended_info='') -> None:
        max_len = 25
        if len(extended_info) > max_len:
            def make_newlines(s, offset=max_len):
                import re
                iterations = len(s) // offset + 1
                for x in range(1, iterations):
                    chunk = s[x * offset:]
                    replaced = re.sub(r'\s', '\n', chunk, 1)
                    s = s.replace(chunk, replaced)
                return s

            extended_info = make_newlines(extended_info)
        self.__cathegories.append(PieCathegory(percentage, 100, name, extended_info,
                                               self.__color_generator.get_color()))
        if len(self.__cathegories) == 1:
            self.__cathegories[-1].start_angle = 0
        else:
            self.__cathegories[-1].start_angle = (self.__cathegories[-2].start_angle +
                                                  self.__cathegories[-2].angle_length)
        self.__cathegories[-1].angle_length = self.__cathegories[-1].value / self.__cathegories[-1].total * 360
        self.__redraw_flag = True

        self.__info_rect_geometry.append([-1, -1, 0, 0])
        self.__info_rect_data.append("")
        self.__info_rect_fixed.append(False)

    def __draw_legend(self):
        step = self.__h // 20
        x0 = self.__x + (self.__w - self.__legend_width) - round((1 - self.__kd) * (self.__w - self.__legend_width) / 2) + 15
        y0 = round(self.__y + self.__h / 2 + 10 - step * len(self.__cathegories) / 2)

        size = min(self.__w, self.__h) // 40
        metrics = QtGui.QFontMetrics(QtGui.QFont("Bahnschrift, Arial", size))
        text_width = 0

        for i, cat in enumerate(self.__cathegories):
            self.__qp.setPen(QtGui.QColor(0, 0, 0, 0))
            self.__qp.setBrush(cat.brush)
            self.__qp.drawRect(x0, y0 + step * i, size + 3, size + 3)

            self.__qp.setPen(QtGui.QColor(0, 0, 0))
            self.__qp.setFont(QtGui.QFont("Bahnschrift, Arial", size))
            self.__qp.drawText(x0 + size + 7, y0 + step * i + size + 1, cat.name)
            try:
                w = metrics.horizontalAdvance(cat.name)
            except AttributeError:
                w = metrics.width(cat.name)
            if w > text_width:
                text_width = w

        self.__legend_width = text_width + 20
        self.__D = int(self.__kd * (self.__w - self.__legend_width))
        if self.__D >= self.__kd * self.__h:
            self.__D = int(self.__kd * self.__h)
        self.__rect = QtCore.QRect(int(self.__x + (self.__w - self.__legend_width) // 2 - self.__D // 2),
                                   int(self.__y + self.__h // 2 - self.__D // 2) + 10, self.__D, self.__D)
        self.__frame.setGeometry(self.__x, self.__y, (self.__w - self.__legend_width), self.__h)

    def legend_width(self):
        return self.__legend_width

    def redraw_plots(self):
        self.__qp.begin(self.__widget)

        self.__qp.setPen(QtGui.QColor(0, 0, 0, 0))
        self.__qp.setBrush(QtGui.QColor(255, 255, 255))
        self.__qp.drawRect(self.__x, self.__y, self.__w, self.__h)

        self.__qp.setPen(QtGui.QColor(0, 0, 0))
        size = min(self.__w, self.__h) // 25
        self.__qp.setFont(QtGui.QFont("Bahnschrift, Arial", size))
        self.__qp.drawText(self.__x, self.__y, self.__w, int(2 * size),
                           QtCore.Qt.AlignmentFlag.AlignCenter, self.__name)
        self.__draw_legend()
        start_angle = 0
        for i, cat in enumerate(self.__cathegories):
            self.__qp.setPen(QtGui.QColor(0, 0, 0, 0))
            alen = round(cat.angle_length * 16)
            a0 = round(cat.start_angle * 16)

            self.__qp.setBrush(cat.brush if not cat.selected else QtGui.QBrush(cat.brush.color().lighter(120)))
            self.__qp.drawPie(self.__rect, a0, alen)
            start_angle = a0 + alen

        for i, cat in enumerate(self.__cathegories):
            if self.__info_rect_geometry[i][0] > 0:
                self.__qp.setFont(self.__info_rect_font)
                self.__qp.setPen(QtGui.QColor(0, 0, 0))
                self.__qp.setBrush(QtGui.QColor(255, 255, 255, alpha=200))
                self.__qp.drawRoundedRect(*self.__info_rect_geometry[i], 5, 5)
                self.__qp.drawText(*self.__info_rect_geometry[i], QtCore.Qt.AlignmentFlag.AlignCenter,
                                   self.__info_rect_data[i])

        self.__qp.setPen(QtGui.QColor(0, 0, 0, 0))
        if start_angle / 16 < 359.9:
            self.__qp.setBrush(QtGui.QColor(150, 150, 150))
            self.__qp.drawPie(self.__rect, start_angle, 360 * 16 - start_angle)

        self.__qp.end()
        self.__redraw_flag = False
