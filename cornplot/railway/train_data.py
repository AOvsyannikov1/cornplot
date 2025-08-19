try:
    from PyQt6.QtCore import QRectF
    from PyQt6.QtGui import QPainter, QColor
except ImportError:
    from PyQt5.QtCore import QRectF
    from PyQt5.QtGui import QPainter, QColor
from .train import Train


class TrainData:

    def __init__(self, dark=False):
        self.trains = dict()
        self.dark = dark

    def add_train(self, number, car_lengths, colors = None):
        self.trains[number] = Train(car_lengths, self.dark, colors)

    def update_train(self, number, coords):
        if number not in self.trains:
            raise ValueError("Поезда с таким номером не существует")
        self.trains[number].update(coords)

    def draw(self, qp: QPainter, rects):
        for i, train in enumerate(self.trains.values()):
            train.draw(qp, rects[i])

    def set_dark(self, dark: bool):
        self.dark = dark
        for t in self.trains.values():
            t.set_dark(dark)
