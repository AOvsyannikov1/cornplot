from PyQt6.QtCore import QLineF

class PolarScannerLine:

    def __init__(self):
        self.angle = 0
        self.selected = False
        self.visible = False
        self.rotate = False
        self.line = QLineF(0, 0, 0, 0)