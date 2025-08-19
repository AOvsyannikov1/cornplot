from .dashboard import Dashboard
try:
    from PyQt6 import QtCore, QtWidgets, QtGui
except ImportError:
    from PyQt5 import QtCore, QtWidgets, QtGui
import numpy as np
import sys
from .plotter import Plotter
from .pie_chart import PieChart
import multiprocessing as mp

class PlotWindow(QtWidgets.QWidget):

    def __init__(self, width=1000, height=600, x=50, y=50):
        super(PlotWindow, self).__init__()
        self.setGeometry(x, y, width, height)
        self.setWindowIcon(QtGui.QIcon("cornplot/images/icon.png"))
        self.setMinimumSize(800, 600)
        self.dashboards = list()
        self.pie_charts = list()
        self.dashboard_locations = list()
        self.dashboard_sizes = list()
        self.axles_num = 0

        self.n_rows = 1
        self.n_cols = 1

        self.y0 = 50
        self.x0 = 100
        self.step_y = (self.height() - 100) // self.n_rows
        self.step_x = (self.width() - 200) // self.n_cols

        self.__pie_chart_only = False

        self.plotter = Plotter(self, self.plots_need_redrawing)
        self.plotter.start()

    def add_axes(self, row=1, col=1, rows=1, cols=1, x_name='X', y_name='Y', animated=False, link_plots=True,
                 draw_axes=False, pie_chart=False):
        if self.__pie_chart_only:
            return
        if self.n_cols < cols:
            self.n_cols = cols
        if self.n_rows < rows:
            self.n_rows = rows
        if (row, col) in self.dashboard_locations:
            return
        self.axles_num += 1
        if pie_chart:
            self.dashboards.append(PieChart(self, 100, 100, 500, name="Содержание газов в воздухе"))
        else:
            if self.axles_num == 1 or not link_plots:
                master = None
            else:
                master = self.dashboards[0]
            self.dashboards.append(Dashboard(self, self.x0, self.y0, self.height() - 100, self.width() - 200, y_name=y_name,
                                             animated=animated, x_name=x_name, master=master, draw_origin=draw_axes))
        self.dashboard_locations.append((row, col))
        self.dashboard_sizes.append((rows, cols))

    def add_plot(self, row, col, x_arr, y_arr, name='', thickness=2, linestyle='solid', color='any'):
        index = self.dashboard_locations.index((row, col))
        self.dashboards[index].add_plot(x_arr, y_arr, name=name, thickness=thickness,
                                        color=color, linestyle=linestyle)

    def add_dataset(self, row, col, name='', x_size=20, thickness=2, linestyle='solid', color='any'):
        index = self.dashboard_locations.index((row, col))
        self.dashboards[index].add_dataset(name, x_size, thickness, linestyle, color)

    def add_point_to_dataset(self, row, col, name, x, y):
        index = self.dashboard_locations.index((row, col))
        self.dashboards[index].add_point_to_dataset(name, x, y)

    def add_hist(self, row, col, data, categories=None, bins=0, name="", color="any"):
        index = self.dashboard_locations.index((row, col))
        self.dashboards[index].add_hist(data, categories, name=name, color=color, bins=bins)

    def add_pie_chart(self, row, col, percentages, category_names, category_descriprions=None):
        index = self.dashboard_locations.index((row, col))

        if len(category_names) != len(percentages):
            return
        elif category_descriprions and len(category_descriprions) != len(category_names):
            return
        for i in range(len(percentages)):
            descr = category_descriprions[i] if category_descriprions else ''
            self.dashboards[index].add_cathegory(percentages[i], category_names[i], descr)

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        for dash in self.dashboards:
            dash.redraw_plots()
        for pc in self.pie_charts:
            pc.redraw_plots()

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
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

            dash.set_geometry(x, y, w, h)

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
            pc.set_geometry(x, y, w, h)

    def plots_need_redrawing(self) -> bool:
        return any([dash.needs_redrawing() for dash in self.dashboards]) or any([pc.needs_redrawing() for pc in self.pie_charts])

    def stop(self):
        del self.plotter


class CornPlotter:

    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.__app_running = False
        self.__windows = list()
        self.__current_window_index = 0
        self.__current_row = 1
        self.__current_col = 1

    def window(self, num, name=""):
        self.__current_window_index = num - 1
        if len(self.__windows) < num:
            self.__windows.append(PlotWindow())
            if name == "":
                name = f"Окно {len(self.__windows)}"
            self.__windows[-1].setWindowTitle(name)
        self.__current_row = 1
        self.__current_col = 1

    def subplot(self, rows, cols, number, link_plots=False, axes=False, pie_chart=False):
        if len(self.__windows) == 0:
            self.__windows.append(PlotWindow())
            self.__windows[-1].setWindowTitle(f"Окно {len(self.__windows)}")
        self.__current_col = np.ceil(number / rows)
        self.__current_row = number - (self.__current_col - 1) * rows
        self.__windows[self.__current_window_index].add_axes(self.__current_row, self.__current_col, rows, cols,
                                                             link_plots=link_plots, draw_axes=axes, pie_chart=pie_chart)


    def plot(self, x_arr, y_arr, x_name="X", y_name="Y", name='',
             thickness=2, linestyle='solid', color='any', animated=False, link_plots=True, axes=False, x_size=20):
        if len(self.__windows) == 0:
            self.__windows.append(PlotWindow())
            self.__windows[-1].setWindowTitle(f"Окно {len(self.__windows)}")
        self.__windows[self.__current_window_index].add_axes(self.__current_row, self.__current_col, 1, 1,
                                                             x_name, y_name, animated, link_plots, draw_axes=axes)
        self.__windows[self.__current_window_index].dashboards[-1].set_x_name(x_name)
        self.__windows[self.__current_window_index].dashboards[-1].set_y_name(y_name)
        self.__windows[self.__current_window_index].add_plot(self.__current_row, self.__current_col, x_arr, y_arr,
                                                             name, thickness, linestyle, color)

    def hist(self, data, categories=None, bins=0, x_name="X", y_name="Y", name="", color='any', link_plots=False):
        if len(self.__windows) == 0:
            self.__windows.append(PlotWindow())
            self.__windows[-1].setWindowTitle(f"Окно {len(self.__windows)}")
        self.__windows[self.__current_window_index].add_axes(self.__current_row, self.__current_col, 1, 1,
                                                             x_name, y_name, False, link_plots, draw_axes=False)
        self.__windows[self.__current_window_index].dashboards[-1].set_x_name(x_name)
        self.__windows[self.__current_window_index].dashboards[-1].set_y_name(y_name)
        self.__windows[self.__current_window_index].add_hist(self.__current_row, self.__current_col, data,
                                                             categories=categories, bins=bins, name=name, color=color)

    def pie_chart(self, percentages, category_names, category_descriptions=None):
        if len(self.__windows) == 0:
            self.__windows.append(PlotWindow())
            self.__windows[-1].setWindowTitle(f"Окно {len(self.__windows)}")
        self.__windows[self.__current_window_index].add_axes(self.__current_row, self.__current_col, 1, 1,
                                                             pie_chart=True)
        self.__windows[self.__current_window_index].add_pie_chart(self.__current_row, self.__current_col,
                                                                  percentages, category_names, category_descriptions)

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


plt = CornPlotter()
