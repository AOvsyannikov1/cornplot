try:
    from PyQt6.QtCore import QThread
except ImportError:
    from PyQt5.QtCore import QThread


class Plotter(QThread):

    def __init__(self, parent, plot_event_function: callable):
        super(Plotter, self).__init__()
        self.plot_window = parent
        self.plot_event_function = plot_event_function
        self.alive = True

    def __str__(self):
        return f"Plotter thread | Parent window: {self.plot_window} | Event: {self.plot_event_function.__name__}"

    def run(self) -> None:
        while self.alive and self.plot_window:
            if self.plot_event_function():
                self.plot_window.update()
            self.msleep(15)

