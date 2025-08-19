from .semaphore import Semaphore, SemaphoreColor
from .station import Station


class TrackData:

    def __init__(self, widget):
        self.semaphores = list()
        self.stations = list()
        self.__w = widget

    def add_semaphore(self, coord, name='', dark=False, four_digit=True):
        self.semaphores.append(Semaphore(self.__w, coord, name, dark=dark, four_digit=four_digit))

    def add_station(self, coord, name, length, dark=False):
        self.stations.append(Station(coord, length, name, dark))

    def clear(self):
        self.semaphores.clear()
        self.stations.clear()

    def set_dark(self, dark: bool):
        for st in self.stations:
            st.dark = dark
        for sem in self.semaphores:
            sem.dark = dark
