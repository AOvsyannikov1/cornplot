from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget
from .utils import get_image_path


class PlotterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon(get_image_path("icon.png")))
    