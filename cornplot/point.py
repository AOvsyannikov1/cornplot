from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtGui import QColor, QPen


class Point(QPointF):
    def __init__(self, name: str, color: QColor, size=5.0, shape="round"):
        super().__init__(0, 0)
        self.name = name
        self.text = ""
        self.pen = QPen(color, size, Qt.PenStyle.SolidLine, Qt.PenCapStyle.SquareCap if shape == "square" else Qt.PenCapStyle.RoundCap)
