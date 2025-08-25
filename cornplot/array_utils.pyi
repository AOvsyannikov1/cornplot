def c_window_to_real_x(x: float, win_width: int, real_width: float, xstart: float) -> float:
    ...


def c_window_to_real_x_log(x: float, xstart: float, xstop: float) -> float:
    ...


def c_window_to_real_y(y: float, win_height: int, real_width: float, ystop: float, min_y: int) -> float:
    ...


def c_window_to_real_y_log(y: float, win_height: int, ystart: float, ystop: float, min_y: int) -> float:
    ...


def c_real_to_window_x(x: float, min_x: int, win_width: int, real_width: float, xstart: float) -> float:
    ...


def c_real_to_window_x_log(x: float, min_x: int, win_width: int, xstart: float, xstop: float) -> float:
    ...


def c_real_to_window_y(y: float, min_y: int, win_height: int, real_height: float, ystop: float) -> float:
    ...


def c_real_to_window_y_log(y: float, min_y: int, max_y: int, win_height: int, ystart: float, ystop: float) -> float:
    ...


def c_get_nearest_value(x_array: list[float], x_real: float) -> list[float, int]:
    ...


def c_recalculate_window_x(x: list[float], min_x: int, win_width: int, real_width: float, xstart: float, i0: int, ik: int, step:int) -> list[float]:
    ...


def c_recalculate_window_y(y: list[float], min_y: int, win_height: int, real_height: float, ystop: float, i0: int, ik: int, step:int) -> list[float]:
    ...
