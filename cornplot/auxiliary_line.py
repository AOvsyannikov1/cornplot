import re
from array import array

from PyQt6.QtCore import QLineF

class AuxiliaryLine:
    def __init__(self):
        self.X = array("d")
        self.Y = array("d")
        self.line = QLineF(0.0, 0.0, 0.0, 0.0)
        self.__equation = "0"

        self.__xmin = 0.0
        self.__xmax = 10.0

        self.__k = 1
        self.__b = 0

    def set_x_limits(self, xmin: float, xmax: float) -> None:
        if xmin < xmax:
            self.__xmin = xmin
            self.__xmax = xmax

    def set_equation(self, eq: str) -> bool:
        "eq: kx + b, например 4x+3"
        line_eq_pattern = r"^\s*((?:[+-]?(?:\d*\.?\d+)?\s*\*?\s*)?(?:\(\s*[-+]?\s*x\s*(?:[+-]\s*[+-]?\d*\.?\d+)?\s*\)|[-+]?\s*x))?\s*((?:[+-]\s*)?[+-]?\d*\.?\d+)?\s*$"
        if re.match(line_eq_pattern, eq):
            self.__equation = eq
            return True
        return False
        
    def recalculate(self) -> None:
        self.X = array("d", [self.__xmin, self.__xmax])
        self.Y = array("d", [eval(self.__equation) for x in self.X])

