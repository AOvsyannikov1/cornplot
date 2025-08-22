import numpy as np
from .console_plotter import _plotter
from .plot_updater import PlotUpdater


__all__ = ['plot', 'animated_plot', 'add_point_to_animated_plot', 'add_plot_updater',
           'histogram', 'pie_chart', 'subplot', 'window', 'show', 'clear']


def plot(x_arr, y_arr=None, x_name="X", y_name="Y", name='', linewidth=2, color="any", link_plots=True, axes=True):
    if y_arr is None:
        X = np.arange(len(x_arr))
        _plotter.plot(X, x_arr, x_name=x_name, y_name=y_name, name=name, linewidth=linewidth,
                 color=color, link_plots=link_plots, axes=axes)
    else:
        _plotter.plot(x_arr, y_arr, x_name=x_name, y_name=y_name, name=name, linewidth=linewidth,
                 color=color, link_plots=link_plots, axes=axes)
        

def animated_plot(name: str, x_size=30, x_name="T", y_name="Y", linewidth=2, color="any", link_plots=True, axes=True):
    _plotter.animated_plot(name, x_size, x_name, y_name, linewidth, color=color, link_plots=link_plots, axes=axes)


def add_plot_updater(updater: PlotUpdater):
    _plotter.add_plot_updater(updater)


def add_point_to_animated_plot(name, x, y):
    _plotter.add_point_to_animated_plot(name, x, y)


def histogram(x_arr, intervals_count=0, x_name="X", y_name="Y", name='', color="any", link_plots=True):
    _plotter.histogram(x_arr, intervals_count=intervals_count, x_name=x_name, y_name=y_name, name=name,
             color=color, link_plots=link_plots)


def pie_chart():
    _plotter.pie_chart()


def subplot(rows, cols, number, link_subplots=True, axes=True):
    _plotter.subplot(rows, cols, number, link_subplots=link_subplots, axes=axes)


def window(num, name="", x=100, y=100):
    _plotter.window(num, name, x, y)


def show():
    _plotter.show()


def clear():
    _plotter.clear()
