import warnings
from PyQt5.QtCore import QThread



class PlotUpdater(QThread):

    def __init__(self):
        super().__init__()
        self.alive = True
        self.__delay__ms = 25

    def run(self):
        while self.alive:
            try:
                self.update_plot()
                self.msleep(self.__delay__ms)
            except NotImplementedError:
                warnings.warn("User method 'update_plot()' has not been implemented. Animation stops.", stacklevel=2)
                return
            
    def set_delay_ms(self, delay_ms: int):
        if delay_ms <= 2:
            return
        self.__delay__ms = delay_ms

    def update_plot(self):
        raise NotImplementedError("User method 'update_plot()' must be implemented!")
