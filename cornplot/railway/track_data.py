from .semaphore import Semaphore
from .station import Station


class TrackData:
    __slots__ = ("semaphores", "stations")

    def __init__(self):
        self.semaphores: list[Semaphore] = list()
        self.stations: list[Station] = list()

    def add_semaphore(self, coord, name='', dark=False, four_digit=True):
        self.semaphores.append(Semaphore(coord, name, dark=dark, four_digit=four_digit))

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
