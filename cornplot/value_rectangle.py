from PyQt6.QtCore import QRectF, QPointF
from PyQt6.QtGui import QColor


class ValueRectangle(QRectF):
    
    def __init__(self, x, y, w, h, text: str, color: QColor, point: QPointF):
        super().__init__(x, y, w, h)
        self.__text = text
        self.__color = color
        self.point = point

    def __contains__(self, other):
        return (self.y() >= other.y() and self.y() <= other.y() + other.height()) or (other.y() >= self.y() and other.y() <= self.y() + self.height())
    
    @property
    def text(self):
        return self.__text
    
    @property
    def color(self):
        return self.__color