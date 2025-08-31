from time import monotonic
from PyQt6.QtGui import QPainter, QColor

from ..filters import MovingAverageFilter


class Train:

    def __init__(self, car_lengths: list[float], dark: bool = False, colors: list[QColor] | None = None) -> None:
        self.L = [l for l in car_lengths]
        self.X = [i * self.L[i] for i in range(len(self.L))]
        self.__speed: float = 0
        if colors:
            self.colors = [QColor(color) for color in colors]
        else:
            self.colors = [QColor("blue") for _ in range(len(self.L))]
        self.h = 10
        self.last_len = 0
        self.dark = dark
        self.__speed_tmr = monotonic()
        self.__speed_filter = MovingAverageFilter(20)

    def update(self, first_car_coord_meters: float):
        dx = first_car_coord_meters - self.X[0]
        self.__speed = self.__speed_filter.filter_data(3.6 * dx / (monotonic() - self.__speed_tmr))
        self.__speed_tmr = monotonic()

        self.X[0] = first_car_coord_meters
        for i in range(1, len(self.X)):
            self.X[i] = self.X[i - 1] - self.L[i - 1]

    def draw(self, qp: QPainter, rects, compact=False):
        if self.dark:
            if compact:
                qp.setPen(QColor(250, 250, 250, 0))
            else:
                qp.setPen(QColor(200, 200, 200))
            qp.setBrush(QColor(0, 83, 166))
        else:
            if compact:
                qp.setPen(QColor(0, 0, 0, 0))
            else:
                qp.setPen(QColor(0, 0, 0))
            qp.setBrush(QColor(0, 83, 166))

        for i, r in enumerate(rects):
            if self.colors is not None:
                qp.setBrush(QColor(self.colors[i]))
            qp.drawPolygon(r)

    def set_dark(self, dark: bool):
        self.dark = dark

    @property
    def speed(self) -> float:
        return self.__speed
    