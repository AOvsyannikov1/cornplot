from PyQt6.QtGui import QPainter, QColor


class Train:

    def __init__(self, car_lengths, dark=False, colors=None):
        self.L = [l for l in car_lengths]
        self.X = [i * self.L[i] for i in range(len(self.L))]
        self.colors = colors
        self.h = 10
        self.last_len = 0
        self.dark = dark

    def update(self, first_car_coord_meters: float):
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