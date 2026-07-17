from typing import Iterable

from .console_plotter import _plotter
from .plot_updater import PlotUpdater
from .utils import arange


__all__ = ['set_style', 'set_dark', 'plot', 'auxiliary_line', 'scatter', 'polar_plot', 'polar_scatter', 
           'animated_plot', 'add_point_to_animated_plot', 'add_plot_updater',
           'histogram', 'density_histogram', 'bar_chart', 'pie_chart', 'subplot', 'figure', 'show', 'clear',
           "set_font", "reset_font", "fill_between", "hide_buttons", "plot_from_file", "set_legend_font"]


def set_style(style: str):
    _plotter.set_style(style)


def set_dark(dark: bool = True):
    _plotter.set_dark(dark)


def hide_buttons(hide: bool = True):
    _plotter.hide_buttons(hide)


def plot_from_file(file_name, x_label: str="X", y_label: str = "Y", plot_labels: list[str] | None = None, synchronise_plots=True, axes=True):
    """
        Добавить статичные графики из файла csv. Данные должны быть записаны в формате X,Y1,Y2...Yn.

        :param file_name: Путь к csv/cplt файлу.
        :param x_label: Имя оси Х.
        :param y_label: Имя оси У.
        :param plot_labels: Коллекция названий графиков.
        :param synchronise_plots: Синхронизировать ли оси, расположенные в одном окне.
        :param axes: Рисовать ли оси.
    """
    _plotter.plot_from_file(file_name, x_label=x_label, y_label=y_label, plot_labels=plot_labels, link_plots=synchronise_plots, axes=axes)



def plot(x_arr: Iterable[float], y_arr: Iterable[float] | None = None, x_label: str="X", 
         y_label: str = "Y", plot_label: str = '', linewidth: float = 2.0, color="any", synchronise_plots=True, axes=True):
    """
        Добавить статичный график.

        :param x_arr: Массив значений Х.
        :param y_arr: Массив значений У.
        :param x_label: Имя оси Х.
        :param y_label: Имя оси У.
        :param plot_label: Название графика.
        :param linewidth: Толщина линии.
        :param color: Цвет графика. Если равен any, генерируется автоматически.
        :param synchronise_plots: Синхронизировать ли оси, расположенные в одном окне.
        :param axes: Рисовать ли оси.
    """
    if y_arr is None:
        y_arr = list(x_arr)
        x_arr = arange(0, len(x_arr), 1)
    _plotter.plot(x_arr, y_arr, x_label=x_label, y_label=y_label, plot_label=plot_label, linewidth=linewidth,
                color=color, link_plots=synchronise_plots, axes=axes)
    

def fill_between(x_arr: Iterable[float], y_arr1: Iterable[float], y_arr2: Iterable[float], x_label: str="X", 
         y_label: str = "Y", plot_label: str = '', color="any", opacity=128):
    """
        Добавить заливку между графиками.

        :param x_arr: Массив значений Х.
        :param y_arr1: Массив значений У первого графика.
        :param y_arr2: Массив значений У второго графика.
        :param x_label: Имя оси Х.
        :param y_label: Имя оси У.
        :param plot_label: Название заливки.
        :param color: Цвет графика. Если равен any, генерируется автоматически.
        :param opacity: Непрозрачность (0 - 255).
    """
    _plotter.fill_between(x_arr, y_arr1, y_arr2, x_label=x_label, y_label=y_label, plot_label=plot_label, color=color, opacity=opacity)


def auxiliary_line(equation: str):
    """
        Добавить вспомогательную прямую линию на оси. Такая линия "только для чтения", её нельзя анализировать, как обычный график.

        :param equation: Уравнение линии вида kx+b.
    """
    _plotter.auxiliary_line(equation)
        

def scatter(x_arr, y_arr=None, x_name="X", y_name="Y", name='', markerwidth=5, color="any", synchronise_plots=True, axes=True):
    if y_arr is None:
        y_arr = list(x_arr)
        x_arr = arange(0, len(x_arr), 1)
    _plotter.plot(x_arr, y_arr, x_label=x_name, y_label=y_name, plot_label=name, linewidth=2,
                color=color, link_plots=synchronise_plots, axes=axes, scatter=True, markerwidth=markerwidth)
    

def polar_plot(amplitudes, angles, linewidth=2, color="any"):
    """
        Добавляет график в полярных координатах.

        :param amplitudes: Массив амплитуд.
        :param angles: Массив углов (в радианах).
        :param linewidth: Толщина линии.
        :param color: Цвет графика. Если равен any, генерируется автоматически.
    """
    _plotter.polar_plot(amplitudes, angles, color, linewidth)


def polar_scatter(amplitudes, angles, linewidth=2, color="any"):
    """
        Добавляет точечный график в полярных координатах.

        :param amplitudes: Массив амплитуд.
        :param angles: Массив углов (в радианах).
        :param linewidth: Толщина линии.
        :param color: Цвет графика. Если равен any, генерируется автоматически.
    """
    _plotter.polar_plot(amplitudes, angles, color, linewidth, scatter=True)
    

def animated_plot(plot_label: str, x_size=30, x_label="T", y_label="Y", linewidth=2, 
                  color="any", synchronise_plots=True, axes=True, limit_data=True, save_data=False, real_time=False):
    """
        Добавить анимированный график.

        :param plot_label: Название графика.
        :param x_size: Размер окна отображения при включённой анимации или начальная длина оси Х при limit_data == False.
        :param x_label: Имя оси Х.
        :param y_label: Имя оси У.
        :param linewidth: Толщина линии.
        :param color: Цвет графика. Если равен any, генерируется автоматически.
        :param synchronise_plots: Синхронизировать ли оси, расположенные в одном окне.
        :param axes: Рисовать ли оси.
        :param limit_data: Ограничивать ли размер окна отображения величиной x_size.
        :param save_data: Сохранять ли все предыдущие точки анимированного графика.
        :param real_time: Отображать метки времени компьютера в качестве меток оси Х.
    """
    _plotter.animated_plot(plot_label, x_size, x_label, y_label, linewidth, color=color, link_plots=synchronise_plots, axes=axes,
                           limit_data=limit_data, save_data=save_data, real_time=real_time)


def add_plot_updater(updater: PlotUpdater):
    """
        Задаёт пользовательский класс, который реализует логику обновления данных на анимированном графике.

        :param updater: Созданный пользователем класс, унаследованный от PlotUpdater. 
        Пользователем должен быть реализован метод update_plot().
    """
    _plotter.add_plot_updater(updater)


def add_point_to_animated_plot(plot_label, x, y):
    """
        Добавляет точку в анимированный график.

        :param plot_label: Имя графика.
        :param x: Значение Х. Если при объявлении графика аргумент real_time == True, значение игнорируется.
        :param y: Значение У. 
    """
    _plotter.add_point_to_animated_plot(plot_label, x, y)


def histogram(x_arr, intervals_count=0, x_label="X", y_label="Y", hist_label='', color="any", probabilities=False, synchronise_plots=False):
    """
        Добавляет гистограмму.

        :param x_arr: Одномерный массив с данными, по которым требуется построить гистограмму.
        :param intervals_count: Число интервалов, на который должна быть разбита ось данных. Если меньше или равно нулю, вычисляется по правилу Стерджесса.
        :param x_label: Имя оси Х.
        :param y_label: Имя оси У.
        :param hist_label: Имя гистограммы.
        :param color: Цвет гистограммы. Если равен any, генерируется автоматически.
        :param probabilities: Если равно True, по оси У отображаются не абсолютные частоты, а относительные (вероятность попадания в интервал).
        :param synchronise_plots: Синхронизировать ли оси, расположенные в одном окне.
    """
    _plotter.histogram(x_arr, intervals_count=intervals_count, x_label=x_label, y_label=y_label, hist_label=hist_label,
             color=color, probabilities=probabilities, link_plots=synchronise_plots)
    

def density_histogram(x_arr, intervals_count=0, x_label="X", y_label="Y", hist_label='', color="any", synchronise_plots=False):
    """
        Добавляет гистограмму плотности распределения.

        :param x_arr: Одномерный массив с данными, по которым требуется построить гистограмму.
        :param intervals_count: Число интервалов, на который должна быть разбита ось данных. Если меньше или равно нулю, вычисляется по правилу Стерджесса.
        :param x_label: Имя оси Х.
        :param y_label: Имя оси У.
        :param hist_label: Имя гистограммы.
        :param color: Цвет гистограммы. Если равен any, генерируется автоматически.
        :param synchronise_plots: Синхронизировать ли оси, расположенные в одном окне.
    """
    _plotter.density_histogram(x_arr, intervals_count=intervals_count, x_label=x_label, y_label=y_label, hist_label=hist_label,
             color=color, link_plots=synchronise_plots)
    

def bar_chart(categories: list[str], values: dict[str, list[float]], y_label="Y", value_colors=None, draw_legend=True, legend_loc='left'):
    """
        Добавляет столбчатую диаграмму.

        :param categories: Массив названий категорий (например, месяцы).
        :param values: Словарь, где ключом является название величины, а значением - список значений, соответствующих каждой категории (см пример в tests.py).
        :param y_label: Имя оси У.
        :param value_colors: Список цветов для каждой величины. Если равен None - генерируется автоматически.
        :param draw_legend: Отображать легенду
        :param legend_loc: Расположение легенды (left/right).
    """
    _plotter.bar_chart(categories, values, y_label, value_colors, draw_legend, legend_loc)


def pie_chart(percentages: list[float], category_names: list[str], category_descriptions: list[str] | None = None):
    """
        Добавляет круговую диаграмму.

        :param percentages: Список процентных значений для каждой категории.
        :param category_names: Список имён категорий.
        :param category_descriptions: Список описанй категорий.
    """
    _plotter.pie_chart(percentages, category_names, category_descriptions)


def subplot(rows: int, cols: int, number: int):
    """
        Объявляет положение осей в окне.

        :param rows: Количество осей по вертикали.
        :param cols: Количество осей по горизонтали.
        :param number: Номер осей в окне.
    """
    _plotter.subplot(rows, cols, number)


def figure(num, name="", x=100, y=100):
    """
        Создание окна для отображения осей.

        :param num: Номер окна (начинается с единицы).
        :param name: Имя окна.
        :param x: 
        :param y: Координаты окна в пикселях.
    """
    _plotter.window(num, name, x, y)


def show():
    """
        Отобразить заданные графики.
    """
    _plotter.show()


def clear():
    """
        Очистить все окна от графиков.
    """
    _plotter.clear()


def set_font(font_name: str, font_size: int):
    _plotter.set_font(font_name, font_size)


def set_legend_font(font_name: str, font_size: int):
    _plotter.set_legend_font(font_name, font_size)


def reset_font():
    _plotter.set_font(None)
