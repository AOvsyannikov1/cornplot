from PyQt5.QtCore import QRectF, QPointF
from PyQt5.QtGui import QColor


class ValueRectangle(QRectF):
    
    def __init__(self, x, y, w, h, text: str, color: QColor, point: QPointF, move_left: bool):
        super().__init__(x, y, w, h)
        self.__text = text
        self.__color = color
        self.point = point
        self.move_left = move_left

    def __contains__(self, other):
        return self.intersects(other)
    
    @property
    def text(self):
        return self.__text
    
    @property
    def color(self):
        return self.__color