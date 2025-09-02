from PyQt6.QtGui import QColor


def background_color(dark: bool) -> QColor:
    return QColor(24, 24, 24) if dark else QColor(0xFFFFFF)


def text_color(dark: bool):
    return QColor(0xD2D2D2) if dark else QColor(0)


def grid_color(dark: bool):
    return QColor(145, 145, 145)
