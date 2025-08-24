from PyQt5.QtGui import QPainter
from .train import Train


class TrainData:

    def __init__(self, dark=False):
        self.trains: dict[str, Train] = dict()
        self.dark = dark

    def add_train(self, number: str, car_lengths, colors = None):
        self.trains[number] = Train(car_lengths, self.dark, colors)

    def update_train(self, number: str, first_car_coord_meters: float):
        if number not in self.trains:
            raise ValueError("Поезда с таким номером не существует")
        self.trains[number].update(first_car_coord_meters)

    def draw(self, qp: QPainter, rects):
        for i, train in enumerate(self.trains.values()):
            train.draw(qp, rects[i])

    def set_dark(self, dark: bool):
        self.dark = dark
        for t in self.trains.values():
            t.set_dark(dark)
