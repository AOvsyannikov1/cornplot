import numpy as np

from .core import plt


__all__ = ['plot', 'hist', 'pie_chart', 'subplot', 'figure', 'show', 'clear']



def plot(x_arr, y_arr=None, x_name="X", y_name="Y", name='', linewidth=2, color="any", link_plots=True, axes=True):
    if y_arr is None:
        X = np.arange(len(x_arr))
        plt.plot(X, x_arr, x_name=x_name, y_name=y_name, name=name, thickness=linewidth,
                 color=color, link_plots=link_plots, axes=axes)
    else:
        plt.plot(x_arr, y_arr, x_name=x_name, y_name=y_name, name=name, thickness=linewidth,
                 color=color, link_plots=link_plots, axes=axes)


def hist(x_arr, categories=None, bins=0, x_name="X", y_name="Y", name='', color="any", link_plots=True):
    plt.hist(x_arr, categories, bins=bins, x_name=x_name, y_name=y_name, name=name,
             color=color, link_plots=link_plots)


def pie_chart():
    plt.pie_chart()


def subplot(rows, cols, number, link_subplots=True, axes=True):
    plt.subplot(rows, cols, number, link_plots=link_subplots, axes=axes)


def figure(num, name=""):
    plt.window(num, name)


def show():
    plt.show()


def clear():
    plt.clear()
