from .plotter_window import PlotterWindow


class FFTWindow(PlotterWindow):
    __slots__ = "dashboard_a", "dashboard_f", "dashboard_source",

    def __init__(self):
        super().__init__()
        self.setGeometry(50, 50, 1530, 900)
        self.setMinimumSize(700, 600)

        from .dashboard import Dashboard
        self.dashboard_a = Dashboard(self, 90, 30, 1400, 400)
        self.dashboard_f = Dashboard(self, 90, 450, 1400, 400)
        self.dashboard_a.set_y_name("Амплитуда")
        self.dashboard_a.enable_x_ticks(False)
        self.dashboard_f.set_x_name("f, Гц")
        self.dashboard_f.set_y_name("Угол, °")

        self.dashboard_a.move_to_group("__fftWindowGroup")
        self.dashboard_f.move_to_group("__fftWindowGroup")

        self.dashboard_source = Dashboard(self, 90, 450, 1400, 400)

    def resizeEvent(self, a0) -> None:
        h = (self.height() - 150) // 3
        self.dashboard_a.set_geometry(90, 30, self.width() - 140, h)
        self.dashboard_f.set_geometry(90, h + 70, self.width() - 140, h)
        self.dashboard_source.set_geometry(90, 2 * h + 100, self.width() - 140, h)
