from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPen, QColor

from.colors import grid_color

class CoordinateAx:
    __slots__ = ("pen_major", "pen_minor", "origin_pen", "minor_step_ratio",
                 "draw_major_grid", "draw_minor_grid", "draw_ticks", "draw_label",
                 "draw_ax", "logarithmic", "autoscale", "divisor", "label_size",
                 "met_width", "met_height", "name",
                 "start", "stop", "min", "max", "real_size", "grid_step")

    def __init__(self):
        self.pen_major = QPen(grid_color(False), 0.5)
        self.pen_major.setStyle(Qt.PenStyle.SolidLine)
        self.pen_minor = QPen(grid_color(False), 0.25)
        self.pen_minor.setStyle(Qt.PenStyle.SolidLine)
        self.origin_pen = QPen(QColor(0, 0, 0), 1.0)

        self.minor_step_ratio = 5

        self.draw_major_grid = True
        self.draw_minor_grid = False
        self.draw_ticks = True
        self.draw_label = True
        self.draw_ax = False
        self.logarithmic = False
        self.autoscale = True

        self.divisor = 1

        self.label_size = 100
        self.met_width = 50
        self.met_height = 12

        self.start = 0.0
        self.stop = 1.0
        self.min = 0.0
        self.max = 1.0
        self.real_size = 0.0
        self.grid_step = 1.0

        self.name = ""
