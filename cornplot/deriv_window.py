from .plotter_window import PlotterWindow


class DerivWindow(PlotterWindow):
    __slots__ = "dashboard"

    def __init__(self):
        from .dashboard import Dashboard

        super().__init__()
        self.setGeometry(50, 50, 1200, 400)
        self.setMinimumSize(500, 300)
        self.dashboard = Dashboard(self, 90, 30, 1100, 720)

    def resizeEvent(self, a0) -> None:
        h = self.height() - 80
        self.dashboard.setGeometry(100, 30, self.width() - 140, h)