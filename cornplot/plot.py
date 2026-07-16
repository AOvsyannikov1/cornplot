from time import time

from PyQt6.QtWidgets import QCheckBox
from PyQt6.QtGui import QPen, QPalette, QFont, QFontMetrics, QColor
from PyQt6.QtCore import QObject, pyqtSignal as Signal, QLineF, QPointF, QRectF

from .array_utils import *
from array import array
from .utils import SelectedPoint


class Plot(QObject):
    redraw_signal = Signal()

    def __init__(self, widget, x_arr, y_arr, pen: QPen, is_dotted=False, name="", accurate=False, hist=False, heatmap=False, animated=False, 
                 x_size=10, checkbox_x: int | None=None, hist_data=None, limited=True, save_data=False, real_time=False):
        super().__init__()
        self.pen = pen
        self.__animated = animated

        self.lines: list[QLineF] = list()
        self.points: list[QPointF] = list()
        self.rects: list[QRectF] = list()

        self.__limited = limited
        self.__save_data = save_data
        self.__real_time = real_time
        self.__dark = False
        self.__first_point = True

        if self.__animated:
            self.X: array = array("d")
            self.Y: array = array("d")
            self.x_size = x_size
            self.__x0 = 0
            self.length = 0
        else:
            self.X: array = x_arr
            self.Y: array = y_arr
            self.__x0 = x_arr[0]
            self.x_size = 0
            self.length = len(x_arr)

        self.visible = True
        self.draw_line = True
        self.draw_markers = is_dotted

        self.hist_data = hist_data

        self.heatmap = heatmap
        self.__marker_width = 5

        self.name = name
        self.index0 = 0
        self.index1 = len(self.X) - 1
        self.accurate = accurate
        self.selectedPoints: list[SelectedPoint] = list()

        self.x_ascending = self.__check_if_x_accending()
        self.is_hist = hist

        self.__maximums = [0.0, 0.0]
        self.__minimums = [0.0, 0.0]
        if not animated and len(x_arr) > 0 and len(y_arr) > 0:
            self.__maximums = [max(x_arr), max(y_arr)]
            self.__minimums = [min(x_arr), min(y_arr)]

        font = QFont("Consolas, Courier New", 12)
        font.setBold(False)
        self.__chb_width = QFontMetrics(font).horizontalAdvance(self.name) + 30

        self.__checkbox: QCheckBox | None = None
        if checkbox_x is not None:
            self.__checkbox = QCheckBox(widget)
            self.__checkbox.setText(self.name)
            self.__checkbox.setChecked(True)
            self.__checkbox.setGeometry(checkbox_x, 0, self.__chb_width, 20)
            self.__checkbox.setFont(font)
            self.__checkbox.toggled["bool"].connect(self.set_visible)

        self.__fill_with_index: int = -1

        self.set_dark(False)
        if self.__checkbox:
            palette = self.__checkbox.palette()
            palette.setColor(QPalette.ColorRole.WindowText, pen.color())
            self.__checkbox.setPalette(palette)
            self.__checkbox.show()

    @property
    def animated(self):
        return self.__animated
    
    @property
    def limited(self):
        return self.__limited
    
    @property
    def save_data(self):
        return self.__save_data
    
    def set_color(self, clr_name):
        self.pen.setColor(QColor(clr_name))
        self.set_dark(self.__dark)

    def set_dark(self, dark: bool):
        if not self.__checkbox:
            return
        self.__dark = dark
        rgb = self.pen.color().getRgb()
        self.__checkbox.setStyleSheet(f"""
                                    QCheckBox {{
                                        spacing: 5px;
                                        color: {'rgb(210, 210, 210)' if dark else 'black'};
                                    }}
                                    QCheckBox::indicator {{
                                        border: 2px solid {'#ccc' if dark else '#333'};
                                        border-radius: 6px;
                                        background-color: white;
                                    }}
                                      QCheckBox::indicator:checked {{
                                        background-color: {self.pen.color().name()};
                                    }}
                                    QCheckBox::indicator:hover {{
                                        background-color: rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, 0.5);
                                    }}
                                """)
        
    def set_filling_with(self, index):
        self.__fill_with_index = index

    def is_filling_between(self) -> bool:
        return self.__fill_with_index >= 0
    
    def filling_between_with(self) -> int:
        return self.__fill_with_index

    def set_checkbox_x(self, x: int):
        if self.__checkbox:
            self.__checkbox.setGeometry(x, self.__checkbox.y(), self.__checkbox.width(), self.__checkbox.height())

    def __len__(self):
        return len(self.X)
    
    def set_checkbox_state(self, state: bool):
        if self.__checkbox:
            self.__checkbox.setChecked(state)

    def set_visible(self, visible: bool):
        if visible != self.visible:
            self.visible = visible
            self.redraw_signal.emit()

    def get_checkbox_width(self):
        if not self.__checkbox:
            return 0
        return self.__chb_width

    @property
    def marker_width(self):
        return self.__marker_width

    def set_marker_width(self, w):
        if w >= 0:
            self.__marker_width = w

    def __check_if_x_accending(self):
        """Анализ, является ли Х возрастающей последовательностью"""
        if len(self.X) == 0:
            return True
        max_x = self.X[0]
        for x in self.X:
            if x > max_x:
                max_x = x
            if x < max_x:
                return False
        return True

    def set_x_size(self, size):
        if self.__animated:
            self.x_size = size

    def add_element(self, x: float, y: float) -> tuple[float, float, bool]:
        if not self.__animated:
            return 0.0, 0.0, False
        
        if self.__real_time:
            x = time()

        if self.__first_point:
            self.__x0 = x
            self.__first_point = False
            self.__maximums[0] = x
            self.__maximums[1] = y
            self.__minimums[0] = x
            self.__minimums[1] = y
            first = True
        else:
            first = False

        if self.__real_time:
            self.X.append(x)
        else:
            self.X.append(x - self.__x0)
        self.Y.append(y)

        if self.__limited and len(self.X) >= 2 and self.X[-1] - self.X[0] >= self.x_size:
            if not self.__save_data:
                self.X.pop(0)
                self.Y.pop(0)
            self.__maximums[1] = max(self.Y)
            self.__minimums[1] = min(self.Y)
            self.__minimums[0] = self.X[0]
            self.__maximums[0] = x
        else:
            self.length += 1

            if self.__maximums[0] < x:
                self.__maximums[0] = x
            elif self.__minimums[0] > x:
                self.__minimums[0] = x
            if self.__maximums[1] < y:
                self.__maximums[1] = y
            elif self.__minimums[1] > y:
                self.__minimums[1] = y
        
        self.index0 = 0
        self.index1 = self.length - 1
        return self.X[-1], self.Y[-1], first

    def get_element(self, index):
        if len(self.X) == 0:
            return 0, 0
        if index >= len(self.X):
            index = len(self.X) - 1
        return self.X[index], self.Y[index]

    def get_nearest(self, x_real):
        if self.x_ascending:
            x, indx = c_get_nearest_value(self.X, x_real, self.index0, self.index1 + 1)
            return [x, indx],

        X = self.X[self.index0:self.index1+1]
        accuracy = max([abs(self.X[i] - self.X[i - 1]) for i in range(1, len(X))])

        ascending = self.X[1] - self.X[0] > 0
        ret = tuple()
        nearest_x = self.X[0]
        nearest_i = 0
        for i, x in enumerate(X):
            if i == 0:
                continue
            if abs(x - x_real) < abs(nearest_x - x_real):
                nearest_x = x
                nearest_i = i
            if (self.X[i] - self.X[i - 1] > 0) != ascending:
                if abs(nearest_x - x_real) <= accuracy:
                    if len(ret) == 0:
                        ret += [nearest_x, nearest_i],
                    elif ret[-1][1] != nearest_i - 1:
                        ret += [nearest_x, nearest_i],
                nearest_x = x
                nearest_i = i
                ascending = not ascending
        if abs(nearest_x - x_real) <= accuracy and nearest_i != len(X) - 1:
            ret += [nearest_x, nearest_i],
        return ret

    def remove_all_points(self):
        self.__first_point = True
        self.X = array("d")
        self.Y = array("d")
        self.length = 0

    def update_x_array(self, x):
        self.X = x
        self.__maximums[0] = max(x)
        self.__minimums[0] = min(x)

    def update_y_array(self, y):
        self.Y = y
        self.__maximums[1] = max(y)
        self.__minimums[1] = min(y)

    def min(self, axis: int) -> float:
        return self.__minimums[axis] if not self.is_hist else 0

    def max(self, axis: int) -> float:
        return self.__maximums[axis]
    
    def get_real_width(self) -> float:
        if not self.__save_data:
            return self.x_size
        else:
            return self.X[-1] - self.X[0]
    
    def __del__(self):
        try:
            if self.__checkbox:
                self.__checkbox.hide()
                self.__checkbox.deleteLater()
        except (RuntimeError, AttributeError):
            pass
