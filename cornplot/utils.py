import dataclasses
from math import log, exp, pow
from array import array
from datetime import datetime, timezone
import importlib.resources as pkg_resources
from pathlib import Path

from PyQt6.QtGui import QColor
import numpy as np


UPPER_INDEXES = ('⁰', '¹', '²', '³', '⁴', '⁵', '⁶', '⁷', '⁸', '⁹')
LOWER_INDEXES = ('₀', '₁', '₂', '₃', '₄', '₅', '₆', '₇', '₈', '₉')


def interpolate(x, x_arr, y_arr):
    if x_arr[1] - x_arr[0] == 0:
        return y_arr[0]
    return y_arr[0] + (x - x_arr[0]) / (x_arr[1] - x_arr[0]) * (y_arr[1] - y_arr[0])


def arange(x0, xk, dx):
    length = int((xk - x0) / dx)
    ret = array("d", [x0] * length)

    for i in range(1, length):
        ret[i] = ret[i - 1] + dx
    return ret


def get_upper_index(number):
    dozens = abs(number) // 10
    ones = abs(number) % 10
    if dozens == 0:
        return ("⁻" if number < 0 else "") + UPPER_INDEXES[ones]
    else:
        return ("⁻" if number < 0 else "") + UPPER_INDEXES[dozens] + UPPER_INDEXES[ones]


def arabic_to_romanian(number):
    romanian_numbers = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]
    if 0 < number < 11:
        return romanian_numbers[number - 1]


def get_nearest_value(iterable, value):
    try:
        return min(iterable, key=lambda x: abs(x - value))
    except ValueError:
        return 0


def convert_timestamp_to_human_time(timestamp, millis=False):
    if millis:
        return datetime.fromtimestamp(timestamp, timezone.utc).time().strftime("%H:%M:%S.%f")[:-3]
    else:
        return datetime.fromtimestamp(int(timestamp), timezone.utc).time().strftime("%H:%M:%S")


def round_custom(num, step):
    return round(num / step) * step


class Gradient:

    def __init__(self, start_color: QColor, stop_color: QColor):
        self.colors = dict()
        self.colors[0.0] = start_color
        self.colors[1.0] = stop_color

    def set_color_at(self, pos: float, color: QColor):
        self.colors[pos] = color

    def get_color(self, pos: float):
        if pos < 0:
            pos = 0
        if pos > 1:
            pos = 1

        if pos <= 0.5:
            red = round(self.colors[0].red() * (1 - pos * 2) + self.colors[0.5].red() * pos * 2)
            green = round(self.colors[0].green() * (1 - pos * 2) + self.colors[0.5].green() * pos * 2)
            blue = round(self.colors[0].blue() * (1 - pos * 2) + self.colors[0.5].blue() * pos * 2)
        else:
            red = round(self.colors[0.5].red() * (1 - (pos - 0.5) * 2) + self.colors[1].red() * (pos - 0.5) * 2)
            green = round(self.colors[0.5].green() * (1 - (pos - 0.5) * 2) + self.colors[1].green() * (pos - 0.5) * 2)
            blue = round(self.colors[0.5].blue() * (1 - (pos - 0.5) * 2) + self.colors[1].blue() * (pos - 0.5) * 2)

        return QColor(red, green, blue)


@dataclasses.dataclass
class SelectedPoint:
    x: float
    y: float
    i: int


def get_image_path(filename: str) -> str:
    """Получить путь к изображению из пакета"""
    try:
        return str(pkg_resources.files("cornplot.images") / filename)
    except AttributeError:
        with pkg_resources.path("cornplot.images", filename) as path:
            return str(Path(path))
    except:
        return filename
    

def get_digit_count_after_dot(num: float):
    num = round(num, 12)
    num_st = str(num)
    if '.' in num_st:
        return len(num_st.split('.')[-1])
    return 0


def round_value(num: float, digit_count=-1) -> str:
    st = str(num)

    if 'e' in st or 'E' in st:
        if 'e' in st:
            val, power = st.split('e')
        else:
            val, power = st.split('E')
        val = float(val)
        power = int(power)
        return f"{val:.3f}×10{get_upper_index(int(power))}"
    
    if '.' in st:
        int_part, frac_part = st.split('.')
        if '-' in int_part:
            int_part = int_part[1:]
        if len(int_part) > 4:
            tmp_str = f"{num:.3E}"
            val, power = tuple(map(float, tmp_str.split('E')))
            return f"{val}×10{get_upper_index(int(power))}"

        if digit_count < 0:
            digit_count = len(frac_part)

        if digit_count <= 4:
            return f"{num:.{digit_count}f}"
        else:
            if num == 0:
                return f"{num:.{digit_count}f}"
            return f"{num:.3e}"
    else:
        return st