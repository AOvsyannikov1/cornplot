from typing import Iterable
from array import array
from math import pi

from PyQt6.QtCore import QLineF, QPointF
from PyQt6.QtGui import QPen


class PolarPlot:

    def __init__(self, r: Iterable[float], a: Iterable[float], pen: QPen):
        self.radiuses: array = array('d', r)
        self.angles: array = array('d', a)
        self.X: array = array('d', [])
        self.Y: array = array('d', [])

        self.pen = pen
        self.points: list[QPointF] = list()
        self.lines: list[QLineF] = list()

        self.draw_line = True
        self.draw_markers = True
        self.accurate = False

    def get_nearest(self, angle):
        X = self.angles
        accuracy = max([abs(X[i] - X[i - 1]) for i in range(1, len(X))])

        ascending = X[1] - X[0] > 0
        ret = tuple()
        nearest_angle = X[0]
        nearest_i = 0
        while angle <= max(self.angles):
            for i, x in enumerate(X):
                if i == 0:
                    continue
                if abs(x - angle) < abs(nearest_angle - angle):
                    nearest_angle = x
                    nearest_i = i
                if (X[i] - X[i - 1] > 0) != ascending:
                    if abs(nearest_angle - angle) <= accuracy:
                        if len(ret) == 0:
                            ret += [nearest_angle, nearest_i],
                        elif ret[-1][1] != nearest_i - 1:
                            ret += [nearest_angle, nearest_i],
                    nearest_angle = x
                    nearest_i = i
                    ascending = not ascending
            if abs(nearest_angle - angle) <= accuracy and nearest_i != len(X) - 1:
                ret += [nearest_angle, nearest_i],
            angle += 2 * pi
        return ret
