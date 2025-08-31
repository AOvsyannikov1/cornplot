from typing import Iterable

import numpy as np
from .console_plotter import _plotter
from .plot_updater import PlotUpdater


__all__ = ['plot', 'scatter', 'polar_plot', 'polar_scatter', 
           'animated_plot', 'add_point_to_animated_plot', 'add_plot_updater',
           'histogram', 'density_histogram', 'pie_chart', 'subplot', 'window', 'show', 'clear']


def plot(x_arr: Iterable[float], y_arr: Iterable[float] | None = None, x_label: str="X", 
         y_label: str = "Y", plot_label: str = '', linewidth: float = 2.0, color="any", synchronise_plots=True, axes=True):
    if y_arr is None:
        y_arr = list(x_arr)
        x_arr = np.arange(len(x_arr))
    _plotter.plot(x_arr, y_arr, x_name=x_label, y_name=y_label, name=plot_label, linewidth=linewidth,
                color=color, link_plots=synchronise_plots, axes=axes)
        

def scatter(x_arr, y_arr=None, x_name="X", y_name="Y", name='', markerwidth=5, color="any", synchronise_plots=True, axes=True):
    if y_arr is None:
        y_arr = list(x_arr)
        x_arr = np.arange(len(x_arr))
    _plotter.plot(x_arr, y_arr, x_name=x_name, y_name=y_name, name=name, linewidth=2,
                color=color, link_plots=synchronise_plots, axes=axes, scatter=True, markerwidth=markerwidth)
    

def polar_plot(amplitudes, angles, linewidth=2, color="any"):
    _plotter.polar_plot(amplitudes, angles, color, linewidth)


def polar_scatter(amplitudes, angles, linewidth=2, color="any"):
    _plotter.polar_plot(amplitudes, angles, color, linewidth, scatter=True)
    

def animated_plot(name: str, x_size=30, x_name="T", y_name="Y", linewidth=2, color="any", synchronise_plots=True, axes=True):
    _plotter.animated_plot(name, x_size, x_name, y_name, linewidth, color=color, link_plots=synchronise_plots, axes=axes)


def add_plot_updater(updater: PlotUpdater):
    _plotter.add_plot_updater(updater)


def add_point_to_animated_plot(name, x, y):
    _plotter.add_point_to_animated_plot(name, x, y)


def histogram(x_arr, intervals_count=0, x_name="X", y_name="Y", name='', color="any", probabilities=False, synchronise_plots=False):
    _plotter.histogram(x_arr, intervals_count=intervals_count, x_name=x_name, y_name=y_name, name=name,
             color=color, probabilities=probabilities, link_plots=synchronise_plots)
    

def density_histogram(x_arr, intervals_count=0, x_name="X", y_name="Y", name='', color="any", synchronise_plots=False):
    _plotter.density_histogram(x_arr, intervals_count=intervals_count, x_name=x_name, y_name=y_name, name=name,
             color=color, link_plots=synchronise_plots)


def pie_chart():
    _plotter.pie_chart()


def subplot(rows, cols, number):
    _plotter.subplot(rows, cols, number)


def window(num, name="", x=100, y=100):
    _plotter.window(num, name, x, y)


def show():
    _plotter.show()


def clear():
    _plotter.clear()
