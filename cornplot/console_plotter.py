import sys, uuid

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtGui import QIcon

import numpy as np

from .dashboard import Dashboard
from .polar_dashboard import DashboardPolar
from .pie_chart import PieChart
from .plot_updater import PlotUpdater
from .utils import get_image_path


class PlotWindow(QWidget):

    def __init__(self, width=1000, height=600, x=50, y=50):
        super().__init__()
        self.setGeometry(x, y, width, height)
        self.setWindowIcon(QIcon(get_image_path("icon.png")))
        self.setMinimumSize(800, 600)
        self.dashboards: list[Dashboard | DashboardPolar] = list()
        self.pie_charts = list()
        self.dashboard_locations = list()
        self.dashboard_sizes = list()
        self.__plt_updaters: list[PlotUpdater] = list()
        self.__datasets: dict[str, int] = dict()
        self.axles_num = 0

        self.n_rows = 1
        self.n_cols = 1

        self.y0 = 50
        self.x0 = 100
        self.step_y = (self.height() - 100) // self.n_rows
        self.step_x = (self.width() - 200) // self.n_cols

        self.__group_id = str(uuid.uuid4())

    def add_dashboard(self, row=1, col=1, rows=1, cols=1, x_name='X', y_name='Y', link_plots=True, draw_axes=False):
        if self.__add_axes(row, col, rows, cols):
            dashboard = Dashboard(self, 0, 0, self.width() - 200, self.height() - 100)
            dashboard.set_y_name(y_name)
            dashboard.set_x_name(x_name)
            dashboard.enable_origin_drawing_x(draw_axes)
            dashboard.enable_origin_drawing_y(draw_axes)
            if link_plots:
                dashboard.move_to_group(self.__group_id)
            self.dashboards.append(dashboard)

    def add_pie_chart_axes(self, row=1, col=1, rows=1, cols=1):
        if self.__add_axes(row, col, rows, cols):
            self.dashboards.append(PieChart(self, 100, 100, 500, name="Содержание газов в воздухе"))

    def add_polar_axes(self, row=1, col=1, rows=1, cols=1):
        if self.__add_axes(row, col, rows, cols):
            self.dashboards.append(DashboardPolar(self, 0, 0, self.width() - 200))

    def __add_axes(self, row, col, rows, cols):
        if self.n_cols < cols:
            self.n_cols = cols
        if self.n_rows < rows:
            self.n_rows = rows
        if (row, col) in self.dashboard_locations:
            return False
        self.axles_num += 1
        self.dashboard_locations.append((row, col))
        self.dashboard_sizes.append((rows, cols))
        return True

    def add_plot(self, row, col, x_arr, y_arr, name='', linewidth=2.0, linestyle='solid', color='any', scatter=False, markerwidth=5.0):
        index = self.dashboard_locations.index((row, col))
        plt_name = self.dashboards[index].add_plot(x_arr, y_arr, name=name, linewidth=linewidth,
                                        color=color, linestyle=linestyle)
        self.dashboards[index].plot_draw_markers(plt_name, scatter)
        self.dashboards[index].set_plot_markerstyle(plt_name, Qt.PenCapStyle.RoundCap)
        self.dashboards[index].set_plot_markerwidth(plt_name, markerwidth)
        self.dashboards[index].plot_draw_line(plt_name, not scatter)

    def add_polar_plot(self, row, col, amplitudes, angles, color="any", linewidth=2, linestyle="solid", scatter=False):
        index = self.dashboard_locations.index((row, col))
        self.dashboards[index].add_plot(amplitudes, angles, color=color, linewidth=linewidth, linestyle=linestyle, scatter=scatter)

    def add_animated_plot(self, row, col, name='', x_size=20, linewidth=2, linestyle='solid', color='any'):
        index = self.dashboard_locations.index((row, col))
        self.__datasets[name] = index
        self.dashboards[index].add_animated_plot(name, x_size=x_size, linewidth=linewidth, linestyle=linestyle, color=color)

    def add_animated_plot_updater(self, updater: PlotUpdater):
        self.__plt_updaters.append(updater)

    def add_point_to_dataset(self, name, x, y):
        index = self.__datasets[name]
        self.dashboards[index].add_point_to_animated_plot(name, x, y)

    def add_histogram(self, row, col, data, intervals_count=0, name="", color="any", probabilities=False):
        index = self.dashboard_locations.index((row, col))
        self.dashboards[index].add_histogram(data, name=name, color=color, interval_count=intervals_count, probabilities=probabilities)

    def add_density_histogram(self, row, col, data, intervals_count=0, name="", color="any"):
        index = self.dashboard_locations.index((row, col))
        self.dashboards[index].add_density_histogram(data, name=name, color=color, interval_count=intervals_count)

    def add_pie_chart(self, row, col, percentages, category_names, category_descriprions=None):
        index = self.dashboard_locations.index((row, col))

        if len(category_names) != len(percentages):
            return
        elif category_descriprions and len(category_descriprions) != len(category_names):
            return
        for i in range(len(percentages)):
            descr = category_descriprions[i] if category_descriprions else ''
            self.dashboards[index].add_cathegory(percentages[i], category_names[i], descr)

    def resizeEvent(self, a0) -> None:
        self.step_y = (self.height() - 80) // self.n_rows
        self.step_x = (self.width() - 150) // self.n_cols
        for dash, loc, size in zip(self.dashboards, self.dashboard_locations, self.dashboard_sizes):
            x = self.x0 + int((loc[1] - 1) * self.step_x)
            y = self.y0 + int((loc[0] - 1) * self.step_y)
            col_size = self.n_cols // size[1]
            row_size = self.n_rows // size[0]
            if self.n_rows > 1:
                h = int(0.85 * self.step_y * row_size + 0.15 * self.step_y * (row_size - 1))
            else:
                h = self.height() - 100
            if self.n_cols > 1:
                w = int(0.92 * (self.step_x * col_size) + 0.08 * self.step_x * (col_size - 1))
            else:
                w = self.width() - 200

            if type(dash) == Dashboard:
                dash.setGeometry(x, y, w, h)
            elif type(dash) == DashboardPolar:
                dash.setGeometry(x, y, min(w, h))

        for pc, loc, size in zip(self.pie_charts, self.dashboard_locations, self.dashboard_sizes):
            step_x = self.step_x
            x = self.x0 + int((loc[1] - 1) * step_x)
            y = self.y0 + int((loc[0] - 1) * self.step_y)
            col_size = self.n_cols // size[1]
            row_size = self.n_rows // size[0]
            if self.n_rows > 1:
                h = int(0.85 * self.step_y * row_size + 0.15 * self.step_y * (row_size - 1))
            else:
                h = self.height() - 100
            if self.n_cols > 1:
                w = int(0.92 * (step_x * col_size) + 0.08 * step_x * (col_size - 1))
            else:
                w = self.width() - 250
            pc.setGeometry(x, y, w, h)

    def showEvent(self, a0):
        for updater in self.__plt_updaters:
            if not updater.isRunning():
                updater.start()

    def closeEvent(self, a0):
        for updater in self.__plt_updaters:
            updater.alive = False

class CornPlotter:

    def __init__(self):
        self.app: QApplication | None = None
        self.__windows: list[PlotWindow] = list()
        self.__current_window_index = 0
        self.__current_row = 1
        self.__current_col = 1
        self.__nrows = 1
        self.__ncols = 1
        self.__datasets: dict[str, int] = dict()

    def window(self, num, name="", x=100, y=100):
        self.__create_qapp()
        self.__current_window_index = num - 1
        if len(self.__windows) < num:
            self.__windows.append(PlotWindow(x=x, y=y))
            if name == "":
                name = f"Окно {len(self.__windows)}"
            self.__windows[-1].setWindowTitle(name)

        self.__current_row = 1
        self.__current_col = 1
        self.__nrows = 1
        self.__ncols = 1

    def subplot(self, rows, cols, number):
        self.__create_qapp()
        self.__add_window()
        self.__current_col = np.ceil(number / rows)
        self.__current_row = number - (self.__current_col - 1) * rows

        self.__nrows = rows
        self.__ncols = cols

    def plot(self, x_arr, y_arr, x_name="X", y_name="Y", name='',
             linewidth=2.0, linestyle='solid', color='any', link_plots=True, axes=False, scatter=False, markerwidth=5.0):
        self.__create_qapp()
        win = self.__add_window()
        win.add_dashboard(self.__current_row, self.__current_col, rows=self.__nrows, cols=self.__ncols,
                          x_name=x_name, y_name=y_name, link_plots=link_plots, draw_axes=axes)
        win.dashboards[-1].set_x_name(x_name)
        win.dashboards[-1].set_y_name(y_name)
        win.add_plot(self.__current_row, self.__current_col, x_arr, y_arr,
                                                             name, linewidth, linestyle, color, scatter, markerwidth)
        
    def animated_plot(self, name: str, x_size=30, x_name="X", y_name="Y", linewidth=2, linestyle='solid', color='any', link_plots=True, axes=False):
        self.__create_qapp()
        win = self.__add_window()
        win.add_dashboard(self.__current_row, self.__current_col, rows=self.__nrows, cols=self.__ncols,
                                                             x_name=x_name, y_name=y_name, link_plots=link_plots, draw_axes=axes)
        win.dashboards[-1].set_x_name(x_name)
        win.dashboards[-1].set_y_name(y_name)
        win.add_animated_plot(self.__current_row, self.__current_col,
                                                                        name, x_size, linewidth, linestyle, color)
        self.__datasets[name] = self.__current_window_index
        
    def add_plot_updater(self, updater: PlotUpdater):
        if len(self.__windows) == 0:
            raise AttributeError("Window has not been created.")
        self.__windows[self.__current_window_index].add_animated_plot_updater(updater)
        
    def add_point_to_animated_plot(self, name, x, y):
        self.__create_qapp()
        index = self.__datasets[name]
        self.__windows[index].add_point_to_dataset(name, x, y)

    def histogram(self, data, intervals_count=0, x_name="X", y_name="Y", name="", color='any', link_plots=False, probabilities=False):
        self.__create_qapp()
        win = self.__add_window()
        win.add_dashboard(self.__current_row, self.__current_col, self.__nrows, self.__ncols,
                                                             x_name=x_name, y_name=y_name, link_plots=link_plots, draw_axes=False)
        win.dashboards[-1].set_x_name(x_name)
        win.dashboards[-1].set_y_name(y_name)
        win.add_histogram(self.__current_row, self.__current_col, data, intervals_count=intervals_count, name=name, color=color, probabilities=probabilities)

    def density_histogram(self, data, intervals_count=0, x_name="X", y_name="Y", name="", color='any', link_plots=False):
        self.__create_qapp()
        win = self.__add_window()
        win.add_dashboard(self.__current_row, self.__current_col, self.__nrows, self.__ncols,
                                                             x_name=x_name, y_name=y_name, link_plots=link_plots, draw_axes=False)
        win.dashboards[-1].set_x_name(x_name)
        win.dashboards[-1].set_y_name(y_name)
        win.add_density_histogram(self.__current_row, self.__current_col, data, intervals_count=intervals_count, name=name, color=color)

    def polar_plot(self, amplitudes, angles, color='any', linewidth=2, linestyle='solid', scatter=False):
        self.__create_qapp()
        win = self.__add_window()
        win.add_polar_axes(self.__current_row, self.__current_col, self.__nrows, self.__ncols)
        win.add_polar_plot(self.__current_row, self.__current_col, amplitudes, angles, color, linewidth, linestyle, scatter)

    def pie_chart(self, percentages, category_names, category_descriptions=None):
        self.__create_qapp()
        win = self.__add_window()
        win.add_pie_chart_axes(self.__current_row, self.__current_col, self.__nrows, self.__ncols)
        win.add_pie_chart(self.__current_row, self.__current_col, percentages, category_names, category_descriptions)

    def show(self):
        for win in self.__windows:
            win.show()
        self.app.exec()

    def clear(self):
        for i in range(len(self.__windows)):
            self.__windows[i].stop()
            for j in range(len(self.__windows[i].dashboards)):
                self.__windows[i].dashboards[j].stop()
            while len(self.__windows[i].dashboards):
                del self.__windows[i].dashboards[-1]
            self.__windows[i].deleteLater()
        self.__windows.clear()
        self.__current_window_index = 0
        self.__current_row = 1
        self.__current_col = 1

    def __create_qapp(self):
        if self.app is None:
            self.app = QApplication(sys.argv)

    def __add_window(self):
        if len(self.__windows) == 0:
            self.__windows.append(PlotWindow())
            self.__windows[-1].setWindowTitle(f"Окно {len(self.__windows)}")
        return self.__windows[self.__current_window_index]

_plotter = CornPlotter()
