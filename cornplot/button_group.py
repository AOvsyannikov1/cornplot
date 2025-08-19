from time import monotonic

from PyQt6.QtWidgets import QPushButton, QFrame
from PyQt6.QtGui import QFont, QIcon
from .utils import button_style, resource_path

class ButtonGroup:
    def __init__(self, widget: QFrame, w, h):
        self.pause_button = QPushButton(widget)
        self.pause_button.setGeometry(w - 56, 22, 25, 25)
        self.pause_button.setIcon(QIcon(resource_path("cornplot/images/pause.png")))
        self.pause_button.setToolTip("Пауза / Старт")
        self.pause_button.setStyleSheet(button_style(False))
        self.pause_button.show()
        self.pause_button.setVisible(False)

        self.restart_button = QPushButton(widget)
        self.restart_button.setGeometry(w - 28, 22, 25, 25)
        self.restart_button.setIcon(QIcon(resource_path("./cornplot/images/restart.png")))
        self.restart_button.setToolTip("Перезапуск анимации")
        self.restart_button.setStyleSheet(button_style(False))
        self.restart_button.show()
        self.restart_button.setVisible(False)

        self.__button_tmr = monotonic()
        self.__buttons_visible = False

        self.arrow_button = QPushButton(widget)
        self.arrow_button.setIcon(QIcon(resource_path("./cornplot/images/show.png")))
        self.arrow_button.clicked.connect(self.__arrow_btn_proc)
        self.arrow_button.show()
        self.arrow_button.setStyleSheet(button_style(False))
        self.arrow_button.setEnabled(True)
        self.arrow_button.setVisible(False)

        self.more_button = QPushButton(widget)
        self.more_button.show()
        self.more_button.setToolTip("Настройки и анализ графиков")
        self.more_button.setIcon(QIcon(resource_path("./cornplot/images/more.png")))
        self.more_button.setStyleSheet(button_style(False))
        self.more_button.setEnabled(True)
        self.more_button.enterEvent = self.__restart_timer

        self.save_button = QPushButton(widget)
        self.save_button.setIcon(QIcon(resource_path("./cornplot/images/save.png")))
        self.save_button.setToolTip("Сохранить изображение")
        self.save_button.setStyleSheet(button_style(False))
        self.save_button.show()
        self.save_button.setEnabled(True)
        self.save_button.enterEvent = self.__restart_timer

        self.back_button = QPushButton(widget)
        self.back_button.setIcon(QIcon(resource_path("./cornplot/images/cancel.png")))
        self.back_button.show()
        self.back_button.setToolTip("Отменить масштабирование")
        self.back_button.setStyleSheet(button_style(False))
        self.back_button.enterEvent = self.__restart_timer

        self.zoom_button = QPushButton(widget)
        self.zoom_button.setIcon(QIcon(resource_path("./cornplot/images/scale.png")))
        self.zoom_button.setToolTip("Масштабировать")
        self.zoom_button.setStyleSheet(button_style(False))
        self.zoom_button.show()
        self.zoom_button.setEnabled(True)
        self.zoom_button.enterEvent = self.__restart_timer

        self.add_vert_button = QPushButton(widget)
        self.add_vert_button.setIcon(QIcon(resource_path("./cornplot/images/scan.png")))
        self.add_vert_button.show()
        self.add_vert_button.setToolTip("Добавить линию-сканер")
        self.add_vert_button.setStyleSheet(button_style(False))
        self.add_vert_button.enterEvent = self.__restart_timer

        self.clear_button = QPushButton(widget)
        self.clear_button.setIcon(QIcon(resource_path("./cornplot/images/clear.png")))
        self.clear_button.show()
        self.clear_button.setToolTip("Очистить график от вспомогательных линий")
        self.clear_button.setStyleSheet(button_style(False))
        self.clear_button.enterEvent = self.__restart_timer

        self.fix_button = QPushButton(widget)
        self.fix_button.setIcon(QIcon(resource_path("./cornplot/images/fix.png")))
        self.fix_button.show()
        self.fix_button.setToolTip("Закрепить нуль Y")
        self.fix_button.setStyleSheet(button_style(False))
        self.fix_button.enterEvent = self.__restart_timer

        self.__animated = False
        self.__visible = True
        self.__dark = False

        self.set_geometry(0, 0, w, h)

    def set_animated(self, animated: bool):
        self.__animated = animated
        if self.__visible:
            self.pause_button.setVisible(animated)
            self.restart_button.setVisible(animated)

    def set_buttons_visible(self, visible):
        self.__visible = visible
        self.arrow_button.setVisible(visible and not self.__buttons_visible)
        self.more_button.setVisible(visible)
        self.save_button.setVisible(visible)
        self.back_button.setVisible(visible)
        self.zoom_button.setVisible(visible)
        self.add_vert_button.setVisible(visible)
        self.clear_button.setVisible(visible)
        self.fix_button.setVisible(visible)

        self.pause_button.setVisible(visible and self.__animated)
        self.restart_button.setVisible(visible and self.__animated)

    def __arrow_btn_proc(self):
        self.__button_tmr = monotonic()

    def set_geometry(self, offset_x, offset_y, ax_w, ax_h):
        button_x0 = offset_x + ax_w - 28
        button_step = 28
        button_y0 = offset_y + ax_h - 7
        button_size = 25
        self.arrow_button.setGeometry(button_x0, button_y0, button_size, button_size)
        self.more_button.setGeometry(button_x0, button_y0, button_size, button_size)
        self.save_button.setGeometry(button_x0 - button_step, button_y0, button_size, button_size)
        self.back_button.setGeometry(button_x0 - button_step * 2, button_y0, button_size, button_size)
        self.zoom_button.setGeometry(button_x0 - button_step * 3, button_y0, button_size, button_size)
        self.add_vert_button.setGeometry(button_x0 - button_step * 4, button_y0, button_size, button_size)
        self.clear_button.setGeometry(button_x0 - button_step * 5, button_y0, button_size, button_size)
        self.fix_button.setGeometry(button_x0 - button_step * 6, button_y0, button_size, button_size)

        button_y0 = 22
        self.restart_button.setGeometry(button_x0, button_y0, button_size, button_size)
        self.pause_button.setGeometry(button_x0 - button_step, button_y0, button_size, button_size)

    def __restart_timer(self, a0):
        self.__button_tmr = monotonic()

    def process_visibility(self):
        TIMEOUT = 5
        T = monotonic() - self.__button_tmr
        if T <= TIMEOUT and not self.__buttons_visible:
            self.clear_button.setVisible(True)
            self.add_vert_button.setVisible(True)
            self.fix_button.setVisible(True)
            self.back_button.setVisible(True)
            self.save_button.setVisible(True)
            self.zoom_button.setVisible(True)
            self.more_button.setVisible(True)
            self.arrow_button.setVisible(False)

            self.__buttons_visible = True

        elif T > TIMEOUT and self.__buttons_visible:
            self.clear_button.setVisible(False)
            self.add_vert_button.setVisible(False)
            self.fix_button.setVisible(False)
            self.back_button.setVisible(False)
            self.save_button.setVisible(False)
            self.zoom_button.setVisible(False)
            self.more_button.setVisible(False)
            self.arrow_button.setVisible(True)

            self.__buttons_visible = False

    def set_dark(self, dark: bool):
        if self.__dark != dark:
            self.arrow_button.setStyleSheet(button_style(dark))
            self.more_button.setStyleSheet(button_style(dark))
            self.save_button.setStyleSheet(button_style(dark))
            self.back_button.setStyleSheet(button_style(dark))
            self.zoom_button.setStyleSheet(button_style(dark))
            self.add_vert_button.setStyleSheet(button_style(dark))
            self.clear_button.setStyleSheet(button_style(dark))
            self.fix_button.setStyleSheet(button_style(dark))

            self.pause_button.setStyleSheet(button_style(dark))
            self.restart_button.setStyleSheet(button_style(dark))
        self.__dark = dark

    def pause(self, pause: bool):
        if pause:
            self.pause_button.setIcon(QIcon("./cornplot/images/play.png"))
        else:
            self.pause_button.setIcon(QIcon("./cornplot/images/pause.png"))