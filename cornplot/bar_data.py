from PyQt6.QtCore import QRectF

class BarData:
    def __init__(self):
        self.categories = list()
        self.values: dict[str, list[float]] = dict()
        self.colors = list()
        self.rects: list[list[QRectF]] = list()
        self.n_values = 0
        