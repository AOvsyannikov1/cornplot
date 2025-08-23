from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPen, QColor


class CoordinateAx:

    def __init__(self):
        self.pen_major = QPen(QColor(145, 145, 145), 0.5)
        self.pen_major.setStyle(Qt.PenStyle.SolidLine)
        self.pen_minor = QPen(QColor(145, 145, 145), 0.25)
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
        self.met_size = 50

        self.name = ""
