import csv, sys, os
from statistics import mean
from functools import partial
from enum import Enum
from math import sqrt

import numpy as np
from PyQt6.QtCore import pyqtSignal, pyqtSlot, Qt, QTimer
from PyQt6.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QColorDialog
from PyQt6.QtGui import QIcon, QColor, QFont

from .cornplot_gui import Ui_CornplotGui
from .deriv_window import DerivWindow
from .fft_window import FFTWindow
from .plot_data import Plot
from .equation_enter_window import EquationWindow
from .color_generator import ColorGenerator
from .filters import MovingAverageFilter, ExponentialFilter, MedianFilter
from scipy.optimize import curve_fit
from scipy.fft import fft, fftfreq
from .utils import *


GRID_STYLES = {
    "Штриховая": "dash",
    "Сплошная": "solid",
}


class MathOperation(Enum):
    ONE_POINT_DIFF = 0
    INTERVAL_DIFF = 1
    FOURIER = 2
    INTEGRATION = 3
    APPROX = 4
    MEAN = 5
    CURVE_LENGTH = 6


class CornplotWindow(Ui_CornplotGui, QMainWindow):
    point_selection_signal = pyqtSignal(int, int)

    def __init__(self, dashboard):
        super().__init__()
        self.setupUi(self)
        # print(4)
        self.setWindowIcon(QIcon(resource_path("cornplot/images/more.png")))
        self.tabWidget.setTabIcon(0, QIcon(resource_path("cornplot/images/axles.png")))
        self.tabWidget.setTabIcon(1, QIcon(resource_path("cornplot/images/mathIcon.png")))

        self.tabWidget_2.setTabIcon(0, QIcon(resource_path("cornplot/images/settingsIcon.png")))
        self.tabWidget_2.setTabIcon(1, QIcon(resource_path("cornplot/images/filter.png")))
        self.tabWidget_2.setTabIcon(2, QIcon(resource_path("cornplot/images/derivative.png")))
        self.tabWidget_2.setTabIcon(3, QIcon(resource_path("cornplot/images/integral.png")))
        self.tabWidget_2.setTabIcon(4, QIcon(resource_path("cornplot/images/spectr.png")))
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(0)

        self.__dashboard = dashboard
        self.__plots: list[Plot] = list()
        self.__message_box: QMessageBox | None = None
        self.math_window = None

        self.eqWin = EquationWindow(dashboard)

        self.xName.setText(self.__dashboard.x_name)
        self.xTicks.setChecked(self.__dashboard.x_ticks_enabled)
        self.yName.setText(self.__dashboard.y_name)
        self.yTicks.setChecked(self.__dashboard.y_ticks_enabled)
        self.xTypeNormal.clicked.connect(self.__dashboard.disable_human_time_display)
        self.xTypeTime.clicked.connect(self.__dashboard.enable_human_time_display)
        self.originCheck.setChecked(self.__dashboard.origin_is_drawing)
        self.majorTicksWidth.setValue(self.__dashboard.major_grid_width)
        self.minorTicksWidth.setValue(self.__dashboard.minor_grid_width)
        self.xScaleSelect.setCurrentIndex(self.__dashboard.x_is_logarithmic)
        self.yScaleSelect.setCurrentIndex(self.__dashboard.y_is_logarithmic)

        for key, value in GRID_STYLES.items():
            if self.__dashboard.major_grid_style == value:
                self.majorTicks.setCurrentText(GRID_STYLES[key])
            if self.__dashboard.minor_grid_atyle == value:
                self.minorTicks.setCurrentText(GRID_STYLES[key])

        self.aboutProgramAction.triggered.connect(self.__show_about)
        self.saveGraphAction.triggered.connect(self.__save_plots_to_file)
        self.newGraphJsonAction.triggered.connect(self.__load_plots_from_file)
        self.newGraphEquationAction.triggered.connect(self.eqWin.show)
        self.exitAction.triggered.connect(self.close)
        self.plotName.currentTextChanged.connect(self.display_plot_info)

        self.xName.textChanged.connect(self.__dashboard.set_x_name)
        self.yName.textChanged.connect(self.__dashboard.set_y_name)

        self.xAuto.toggled.connect(self.__dashboard.set_x_autoscale)
        self.yAuto.toggled.connect(self.__dashboard.set_y_autoscale)
        self.xStep.valueChanged.connect(self.__dashboard.set_step_x)
        self.yStep.valueChanged.connect(self.__dashboard.set_step_y)

        self.xMin.valueChanged.connect(self.__dashboard.set_x_start)
        self.yMin.valueChanged.connect(self.__dashboard.set_y_start)
        self.xMax.valueChanged.connect(self.__dashboard.set_x_stop)
        self.yMax.valueChanged.connect(self.__dashboard.set_y_stop)

        self.majorTicksCheck.toggled.connect(self.__dashboard.enable_major_grid)
        self.minorTicksCheck.toggled.connect(self.__dashboard.enable_minor_grid)
        self.originCheck.toggled.connect(self.__origin_enable)
        self.originWidth.valueChanged.connect(self.__origin_enable)

        self.majorTicks.currentTextChanged.connect(self.__major_style_change_event)
        self.majorTicksWidth.valueChanged.connect(self.__major_style_change_event)
        self.minorTicks.currentTextChanged.connect(self.__minor_style_change_event)
        self.minorTicksWidth.valueChanged.connect(self.__minor_style_change_event)
        self.minorTicksStep.valueChanged.connect(self.__minor_style_change_event)

        self.xTicks.toggled.connect(self.__dashboard.enable_x_ticks)
        self.yTicks.toggled.connect(self.__dashboard.enable_y_ticks)

        self.xTypeNormal.clicked.connect(self.__dashboard.disable_human_time_display)
        self.xTypeTime.clicked.connect(self.__dashboard.enable_human_time_display)

        self.__derivWin = DerivWindow()
        self.__fftWindow = FFTWindow()

        self.diffPointSelect.clicked.connect(self.__begin_point_diff)
        self.diffSelectTwoPoints.clicked.connect(self.__begin_interval_diff)
        self.diffSelectAll.clicked.connect(self.__begin_all_diff)

        self.approxButton.clicked.connect(self.__fit)
        self.approxIntervalButton.clicked.connect(self.__begin_interval_approx)
        self.meanSelectInterval.clicked.connect(self.__begin_interval_mean_calculating)
        self.meanCalculateAll.clicked.connect(self.__begin_all_mean_calculating)
        self.equationButton.clicked.connect(self.__show_dialog)

        self.lineWidth.valueChanged.connect(self.__line_width_changed)
        self.markerWidth.valueChanged.connect(self.__marker_width_changed)
        self.drawMarkers.toggled.connect(self.__markers_checked)
        self.drawLine.toggled.connect(self.__line_checked)
        self.markerStyles.currentTextChanged.connect(self.__set_plot_markers)
        self.plotLineStyle.currentTextChanged.connect(self.__set_plot_linestyle)
        self.xScaleSelect.currentIndexChanged.connect(self.__dashboard.set_x_logarithmic)
        self.yScaleSelect.currentIndexChanged.connect(self.__dashboard.set_y_logarithmic)

        self.__equation = "Аппроксимация не выполнялась"

        self.integralSelectInterval.clicked.connect(self.__begin_interval_integral)
        self.integrateAll.clicked.connect(self.__begin_all_integral)
        self.doFiltering.clicked.connect(self.__filter_plot)
        self.fourierIntervalButton.clicked.connect(self.__begin_fourier_transform)
        self.fourierAllButton.clicked.connect(self.__begin_all_fourier_transform)
        self.curveLengthAll.clicked.connect(self.__begin_all_curve_length_calc)
        self.curveLengthInterval.clicked.connect(self.__begin_interval_curve_length_calc)

        self.accurateDrawingCheckbox.toggled.connect(self.__set_plot_accurate)

        self.exportToCSV.triggered.connect(self.__export_plot_to_csv)
        self.importFromCSV.triggered.connect(self.__import_plot_from_csv)

        self.periodicalFft.toggled.connect(self.__start_periodical_fft)

        self.__fft_tmr = QTimer()

        self.__operation = MathOperation.ONE_POINT_DIFF

    @pyqtSlot(str)
    def __set_plot_markers(self, val: str):
        style = Qt.PenCapStyle.RoundCap if (val == "Круглые") else Qt.PenCapStyle.SquareCap
        self.__dashboard.set_plot_markerstyle(self.plotName.currentText(), style)

    @pyqtSlot(bool)
    def __set_plot_accurate(self, val: bool):
        self.__dashboard.set_plot_accurate(self.plotName.currentText(), val)

    @pyqtSlot(float)
    def __line_width_changed(self, val: float):
        self.__dashboard.set_plot_linewidth(self.plotName.currentText(), val)

    @pyqtSlot(bool)
    def __markers_checked(self, val: bool):
        self.__dashboard.plot_draw_markers(self.plotName.currentText(), val)

    @pyqtSlot(bool)
    def __line_checked(self, val: bool):
        self.__dashboard.plot_draw_line(self.plotName.currentText(), val)

    @pyqtSlot(float)
    def __marker_width_changed(self, val: float):
        self.__dashboard.set_plot_markerwidth(self.plotName.currentText(), val)

    def set_plot_picture(self, grab):
        self.pltImage.setPixmap(grab)

    @pyqtSlot()
    def __origin_enable(self):
        self.__dashboard.enable_origin_drawing(self.originCheck.isChecked(), self.originWidth.value())

    @pyqtSlot()
    def __major_style_change_event(self):
        style = self.majorTicks.currentText()
        if style in GRID_STYLES:
            self.__dashboard.set_major_grid_style(GRID_STYLES[style], self.majorTicksWidth.value())
        else:
            self.__dashboard.set_major_grid_style("dot", self.majorTicksWidth.value())

    @pyqtSlot()
    def __minor_style_change_event(self):
        style = self.minorTicks.currentText()
        if style in GRID_STYLES:
            self.__dashboard.set_minor_grid_style(GRID_STYLES[style], self.minorTicksWidth.value(), self.minorTicksStep.value())
        else:
            self.__dashboard.set_minor_grid_style("dot", self.minorTicksWidth.value(), self.minorTicksStep.value())

    @pyqtSlot(str)
    def __set_plot_linestyle(self, style: str):
        plt_name = self.plotName.currentText()
        match style:
            case "Сплошная":
                self.__dashboard.set_plot_linestyle(plt_name, Qt.PenStyle.SolidLine)
            case "Штриховая":
                self.__dashboard.set_plot_linestyle(plt_name, Qt.PenStyle.DashLine)
            case "Штрихпунктирная":
                self.__dashboard.set_plot_linestyle(plt_name, Qt.PenStyle.DashDotLine)
            case "Штрихпунктирная с двумя точками":
                self.__dashboard.set_plot_linestyle(plt_name, Qt.PenStyle.DashDotDotLine)
            case "Пунктирная":
                self.__dashboard.set_plot_linestyle(plt_name, Qt.PenStyle.DotLine)

    @pyqtSlot()
    def __show_about(self):
        self.__message_box = QMessageBox()
        self.__message_box.setIcon(QMessageBox.Icon.Information)
        self.__message_box.setText(f"Время перерисовки: {self.__dashboard.redraw_time * 1000:.2f} мс")
        self.__message_box.setInformativeText("V.3.0 | 15.08.2025")
        self.__message_box.setWindowTitle("О программе")
        self.__message_box.setStandardButtons(QMessageBox.StandardButton.Yes)
        self.__message_box.button(QMessageBox.StandardButton.Yes).setText("Очень рад!")
        self.__message_box.exec()

    def update_plot_info(self, graph_list):
        old_len = len(self.__plots)
        new_len = len(graph_list)

        self.__plots = graph_list
        if self.xAuto.isChecked():
            self.xStep.setValue(self.__dashboard.step_x)
            self.xMin.setValue(self.__dashboard.x_start)
            self.xMax.setValue(self.__dashboard.x_stop)
        if self.yAuto.isChecked():
            self.yStep.setValue(self.__dashboard.step_y)
            self.yMin.setValue(self.__dashboard.y_start)
            self.yMax.setValue(self.__dashboard.y_stop)
        self.majorTicksCheck.setChecked(self.__dashboard.major_ticks_enabled)
        self.minorTicksCheck.setChecked(self.__dashboard.minor_ticks_enabled)

        last_index = self.plotName.currentIndex()

        self.plotName.clear()
        for plt in self.__plots:
            self.plotName.addItem(plt.name)

        if new_len >= old_len and 0 <= last_index < self.plotName.count():
            self.plotName.setCurrentIndex(last_index)

    def __show_dialog(self):
        self.msgBox = QMessageBox()
        self.msgBox.setIcon(QMessageBox.Icon.Information)
        self.msgBox.setFont(QFont('consolas', 12))
        self.msgBox.setText(self.__equation)
        self.msgBox.setWindowTitle("Уравнение")
        self.msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
        self.msgBox.show()

    def display_plot_info(self, plt_name: str = ''):
        if len(self.__plots) == 0:
            return
        
        plot: Plot | None = None
        
        if plt_name == '':
            plot = self.__plots[0]
        else:
            for plt in self.__plots:
                if plt.name == plt_name:
                    plot = plt
                    break

        if plot is None:
            return

        if len(plot.X) < 2:
            min_x = 0
            max_x = 0
            max_y = 0
            min_y = 0
        else:
            min_x = round(min(plot.X), 2)
            max_x = round(max(plot.X), 2)
            min_y = round(min(plot.Y), 2)
            max_y = round(max(plot.Y), 2)

        min_x_str = f"{min_x:.2f}" if min_x < 0 else f"+{min_x:.2f}"
        max_x_str = f"{max_x:.2f}" if max_x < 0 else f"+{max_x:.2f}"

        min_y_str = f"{min_y:.2f}" if min_y < 0 else f"+{min_y:.2f}"
        max_y_str = f"{max_y:.2f}" if max_y < 0 else f"+{max_y:.2f}"
        
        self.pltXmin.setText(min_x_str)
        self.pltXmax.setText(max_x_str)
        self.pltYmin.setText(min_y_str)
        self.pltYmax.setText(max_y_str)

        try:
            self.colorButton.clicked.disconnect()
        except:
            pass
        self.colorButton.clicked.connect(lambda: self.__open_color_dialog(plot))
        self.colorButton.setStyleSheet(f"""QPushButton
                                        {{
                                            background-color : {plot.pen.color().name()};
                                            color: {self.__choose_contrast_color(plot.pen.color()).name()};
                                            border-style : outset;
                                            border-radius : 5px;
                                            border-width : 1px;
                                            border-color : black;
                                            height: 25px;
                                        }}
                                        QPushButton::hover
                                        {{
                                            border-style : outset;
                                            border-radius : 5px;
                                            border-width : 2px;
                                            border-color : black;
                                        }}
                                        QPushButton::pressed
                                        {{
                                            border-style : inset;
                                            border-radius : 5px;
                                            border-width : 3px;
                                            border-color : black;
                                        }}""")

        try:
            self.deletePlotButton.clicked.disconnect()
        except:
            pass
            
        self.nPoints.setText(str(len(plot.X)))
        self.deletePlotButton.clicked.connect(partial(self.__delete_plot, plot.name))
        self.drawLine.setChecked(plot.draw_line)
        self.drawMarkers.setChecked(plot.draw_markers)
        self.markerWidth.setValue(plot.marker_width)
        self.lineWidth.setValue(plot.pen.widthF())
        if plot.pen.capStyle() == Qt.PenCapStyle.RoundCap:
            self.markerStyles.setCurrentText("Круглые")
        else:
            self.markerStyles.setCurrentText("Квадратные")
            
        self.tabWidget_2.setTabEnabled(2, not plot.is_hist)
        self.tabWidget_2.setTabEnabled(3, not plot.is_hist)
        self.tabWidget_2.setTabEnabled(4, not plot.is_hist)
        self.filterGroup.setEnabled(not plot.is_hist)

        # screen = self.__dashboard.take_plot_screenshot(self.plotName.currentText())
        # self.pltImage.setPixmap(screen.scaledToWidth(self.deletePlotButton.width()))

    @pyqtSlot()
    def __delete_plot(self, plt_name):
        self.__message_box = QMessageBox()
        self.__message_box.setIcon(QMessageBox.Icon.Question)
        self.__message_box.setText("Вы действительно хотите удалить график? Отменить это действие будет нельзя.")
        self.__message_box.setWindowTitle("Подтвердите операцию")
        self.__message_box.setStandardButtons(QMessageBox.StandardButton.Yes |
                                       QMessageBox.StandardButton.No)
        self.__message_box.button(QMessageBox.StandardButton.Yes).setText("Да")
        self.__message_box.button(QMessageBox.StandardButton.No).setText("Нет")

        button = self.__message_box.exec()
        if button == QMessageBox.StandardButton.Yes:
            self.__dashboard.delete_plot(plt_name)
            self.__message(f"График {plt_name} удалён.")

    @pyqtSlot(Plot)
    def __open_color_dialog(self, plt: Plot):
        dlg = QColorDialog(self)
        dlg.setWindowTitle(f"{plt.name}: выбор цвета")
        dlg.setCurrentColor(plt.pen.color())

        for i, color in enumerate(ColorGenerator.COLORS):
            dlg.setCustomColor(i, QColor(color))

        if dlg.exec():
            plt.pen.setColor(QColor(dlg.currentColor().name()))
            self.colorButton.setStyleSheet(f"""QPushButton
                                            {{
                                                background-color: '{plt.pen.color().name()}'; 
                                                color: {self.__choose_contrast_color(plt.pen.color()).name()};
                                                border-style: outset;
                                                border-radius: 5px;
                                                border-width: 1px;
                                                border-color: black;
                                                height: 25px;
                                            }}
                                            QPushButton::hover
                                            {{
                                                border-style: outset;
                                                border-radius: 5px;
                                                border-width: 2px;
                                                border-color: black;
                                            }}
                                            QPushButton::pressed
                                            {{
                                                border-style: inset;
                                                border-radius: 5px;
                                                border-width: 3px;
                                                border-color: black;
                                            }}""")
            self.__dashboard._force_redraw()

    @pyqtSlot()
    def __save_plots_to_file(self):
        fileName, _ = QFileDialog.getSaveFileName(self, "Экспорт в файл", filter="Cornplot Files (*.cplt)")
        if len(fileName) > 0:
            self.__dashboard.export_to_file(fileName)

    @pyqtSlot()
    def __load_plots_from_file(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Импорт из файла", filter="Cornplot Files (*.cplt)")
        self.__dashboard.import_from_file(fileName)

    def set_selected_points(self, points: list[SelectedPoint]):
        plot = self.__plots[self.plotName.currentIndex()]

        if len(points) > 1:
            i0 = min(points[0].i, points[1].i)
            ik = max(points[0].i, points[1].i)
        else:
            i0 = 0
            ik = 1

        match self.__operation:
            case MathOperation.ONE_POINT_DIFF:
                self.__find_derivative_in_point(plot, points[0].i)
            case MathOperation.FOURIER:
                self.__fourier_transform(plot, i0, ik)
            case MathOperation.INTERVAL_DIFF:
                self.__find_derivative_on_interval(plot, i0, ik)
            case MathOperation.INTEGRATION:
                self.__find_integral(plot, i0, ik)
            case MathOperation.APPROX:
                self.__fit(i0, ik)
            case MathOperation.MEAN:
                self.__find_mean_value(plot, i0, ik)
            case MathOperation.CURVE_LENGTH:
                self.__find_curve_length(plot, i0, ik)

    def __find_derivative_in_point(self, plot: Plot, i):
        # if not self.__derivWinFirst:
        #     self.__derivWin.open()

        x_arr = plot.X
        y_arr = plot.Y
        if self.__dashboard.is_animated() and x_arr[0] > 0:
            for i in range(len(x_arr)):
                x_arr[i] -= x_arr[0]

        if i >= 0:
            if i < len(x_arr) - 1:
                i1 = i + 1
            else:
                i1 = i - 1
            x0 = x_arr[min(i, i1)]
            x1 = x_arr[max(i, i1)]
            y0 = y_arr[min(i, i1)]
            y1 = y_arr[max(i, i1)]
            d = (y1 - y0) / (x1 - x0)

            self.xDiff.setText(self.__param_to_string(x_arr[i]))
            self.yDiff.setText(self.__param_to_string(y_arr[i]))
            self.diffResult.setText(self.__param_to_string(d))
            self.__message("Производная в точке вычислена успешно.")
        else:
            self.__message("Ошибка вычисления производной в точке.")
    
    def __find_derivative_on_interval(self, plot: Plot, i0, ik):    
        x_arr = plot.X
        y_arr = plot.Y

        x_to_diff = list(np.array(x_arr[i0:(ik + 1)]))
        y_to_diff = np.array(y_arr[i0:(ik + 1)])
        y_ret = [y_to_diff[0]] * len(y_to_diff)

        for i in range(len(y_to_diff)):
            if i == 0:
                continue
            y_ret[i] = ((y_to_diff[i] - y_to_diff[i - 1]) / (x_to_diff[i] - x_to_diff[i - 1]))
            if x_to_diff[i] == x_to_diff[i - 1]:
                y_ret[i] = 0
        if len(y_ret) < len(x_to_diff):
            x_to_diff.append(x_to_diff[-1])
            y_ret.append(0.0)
        color = plot.pen.color()
        color = color.darker(150).name()

        y_ret[0] = y_ret[1]

        if self.diffNewWindow.isChecked():
            self.__derivWin.dashboard.delete_all_plots()
            self.__derivWin.dashboard.add_plot(x_to_diff, y_ret, name=f"{self.plotName.currentText()} (производная)")
            self.__derivWin.setWindowTitle(f"{self.plotName.currentText()} (производная)")

            if self.__dashboard.human_time_display_enabled():
                self.__derivWin.dashboard.enable_human_time_display()
            else:
                self.__derivWin.dashboard.disable_human_time_display()
            self.__derivWin.dashboard.set_initial_timestamp(x_to_diff[0] + self.__dashboard.get_initial_timestamp())
            self.__derivWin.open()
            self.__derivWinFirst = False
        else:
            self.__dashboard.delete_plot(f"{self.plotName.currentText()} (производная)")
            self.__dashboard.add_plot(x_to_diff, y_ret, name=f"{self.plotName.currentText()} (производная)", color=color, linestyle="dash-dot-dot")
            self.__dashboard._force_redraw()

        self.xDiffBegin.setText(self.__param_to_string(x_to_diff[0]))
        self.xDiffEnd.setText(self.__param_to_string(x_to_diff[-1]))

    def __find_integral(self, plot: Plot, i0, ik):
        x_arr = plot.X[i0:ik]
        y_arr = plot.Y[i0:ik]
        Y = [0.0]

        integral = 0
        for i in range(1, len(x_arr)):
            integral += (x_arr[i] - x_arr[i - 1]) * (y_arr[i] + y_arr[i - 1]) / 2
            Y.append(integral)

        self.xIntegrBegin.setText(self.__param_to_string(x_arr[0]))
        self.xIntegrEnd.setText(self.__param_to_string(x_arr[-1]))
        self.integralResult.setText(self.__param_to_string(integral))

        if self.integralPlot.isChecked():
            if self.integralPlotNewWindow.isChecked():
                self.__derivWin.dashboard.delete_all_plots()
                self.__derivWin.dashboard.add_plot(x_arr, Y, name=f"{self.plotName.currentText()} (интеграл)")
                self.__derivWin.setWindowTitle(f"{self.plotName.currentText()} (интеграл)")

                if self.__dashboard.human_time_display_enabled():
                    self.__derivWin.dashboard.enable_human_time_display()
                else:
                    self.__derivWin.dashboard.disable_human_time_display()
                self.__derivWin.dashboard.set_initial_timestamp(x_arr[0] + self.__dashboard.get_initial_timestamp())
                self.__derivWin.open()
                self.__derivWinFirst = False
            else:
                color = plot.pen.color().darker(160).name()
                self.__dashboard.delete_plot(f"{self.plotName.currentText()} (интеграл)")
                self.__dashboard.add_plot(x_arr, Y, name=f"{self.plotName.currentText()} (интеграл)", color=color, linestyle="dash-dot-dot")
                self.__dashboard._force_redraw()
        else:
            self.__message("Интеграл вычислен успешно.")

    def __find_mean_value(self, plot: Plot, i0, ik):
        result = mean(plot.Y[i0:ik])

        self.xMeanBegin.setText(self.__param_to_string(plot.X[i0]))
        self.xMeanEnd.setText(self.__param_to_string(plot.X[ik]))
        self.meanResult.setText(self.__param_to_string(result))
        self.__message("Среднее значение вычислено успешно.")

    def __find_curve_length(self, plot: Plot, i0, ik):
        length = 0

        x_arr = plot.X[i0:ik]
        y_arr = plot.Y[i0:ik]
        prev_under_integral = 0

        for i in range(len(x_arr)):
            if i == 0:
                continue

            derivative = (y_arr[i] - y_arr[i - 1]) / (x_arr[i] - x_arr[i - 1])
            under_integral = sqrt(1 + derivative * derivative)

            length += (x_arr[i] - x_arr[i - 1]) * (under_integral + prev_under_integral) / 2
            prev_under_integral = under_integral
        
        self.xLengthBegin.setText(self.__param_to_string(x_arr[0]))
        self.xLengthEnd.setText(self.__param_to_string(plot.X[ik]))
        self.lengthResult.setText(self.__param_to_string(length))

        self.__message("Длина дуги кривой вычислена успешно.")

    @pyqtSlot(bool)
    def __start_periodical_fft(self, start: bool):
        if start:
            self.__fftWindow.show()
            self.__fft_tmr.timeout.connect(self.__periodical_fft)
            self.__fft_tmr.start(250)
        else:
            self.__fftWindow.close()
            self.__fft_tmr.stop()
            self.__fft_tmr.timeout.disconnect()

    @pyqtSlot()
    def __periodical_fft(self):
        if self.__fftWindow.isVisible() and not self.__dashboard.is_paused() and self.periodicalFft.isChecked():
            plot = self.__plots[self.plotName.currentIndex()]
            self.__fourier_transform(plot)

    @pyqtSlot()
    def __begin_all_fourier_transform(self):
        plot = self.__plots[self.plotName.currentIndex()]
        self.__fourier_transform(plot)

    @pyqtSlot()
    def __begin_fourier_transform(self):
        if self.__dashboard.is_animated() and not self.__dashboard.is_paused():
            self.__message("Действие не может быть выполнено.")
            return
        self.point_selection_signal.emit(self.plotName.currentIndex(), 2)
        self.hide()
        self.__operation = MathOperation.FOURIER

    @pyqtSlot()
    def __begin_point_diff(self):
        if self.__dashboard.is_animated() and not self.__dashboard.is_paused():
            self.__message("Действие не может быть выполнено.")
            return
        self.point_selection_signal.emit(self.plotName.currentIndex(), 1)
        self.hide()
        self.__operation = MathOperation.ONE_POINT_DIFF

    @pyqtSlot()
    def __begin_interval_diff(self):
        if self.__dashboard.is_animated() and not self.__dashboard.is_paused():
            self.__message("Действие не может быть выполнено.")
            return
        self.point_selection_signal.emit(self.plotName.currentIndex(), 2)
        self.hide()
        self.__operation = MathOperation.INTERVAL_DIFF

    @pyqtSlot()
    def __begin_all_diff(self):
        plot = self.__plots[self.plotName.currentIndex()]
        i0 = 0
        ik = len(plot.X) - 1
        self.__find_derivative_on_interval(plot, i0, ik)

    @pyqtSlot()
    def __begin_all_integral(self):
        plot = self.__plots[self.plotName.currentIndex()]
        i0 = 0
        ik = len(plot.X)
        self.__find_integral(plot, i0, ik)

    @pyqtSlot()
    def __begin_interval_integral(self):
        if self.__dashboard.is_animated() and not self.__dashboard.is_paused():
            self.__message("Действие не может быть выполнено.")
            return
        self.point_selection_signal.emit(self.plotName.currentIndex(), 2)
        self.hide()
        self.__operation = MathOperation.INTEGRATION

    @pyqtSlot()
    def __begin_interval_approx(self):
        if self.__dashboard.is_animated() and not self.__dashboard.is_paused():
            self.__message("Действие не может быть выполнено.")
            return
        self.point_selection_signal.emit(self.plotName.currentIndex(), 2)
        self.hide()
        self.__operation = MathOperation.APPROX

    @pyqtSlot()
    def __begin_interval_mean_calculating(self):
        if self.__dashboard.is_animated() and not self.__dashboard.is_paused():
            self.__message("Действие не может быть выполнено.")
            return
        self.point_selection_signal.emit(self.plotName.currentIndex(), 2)
        self.hide()
        self.__operation = MathOperation.MEAN

    @pyqtSlot()
    def __begin_all_mean_calculating(self):
        plot = self.__plots[self.plotName.currentIndex()]
        i0 = 0
        ik = len(plot.X) - 1
        self.__find_mean_value(plot, i0, ik)

    @pyqtSlot()
    def __begin_all_curve_length_calc(self):
        plot = self.__plots[self.plotName.currentIndex()]
        i0 = 0
        ik = len(plot.X) - 1
        self.__find_curve_length(plot, i0, ik)

    @pyqtSlot()
    def __begin_interval_curve_length_calc(self):
        if self.__dashboard.is_animated() and not self.__dashboard.is_paused():
            self.__message("Действие не может быть выполнено.")
            return
        self.point_selection_signal.emit(self.plotName.currentIndex(), 2)
        self.hide()
        self.__operation = MathOperation.CURVE_LENGTH

    def __fourier_transform(self, plot: Plot, i0=None, ik=None):
        x_arr = [x for x in plot.X]
        y_arr = [y for y in plot.Y]

        if i0 is not None and ik is not None:
            x_arr = x_arr[i0:ik + 1]
            y_arr = y_arr[i0:ik + 1]

        if self.deleteConstantCheckbox.isChecked():
            coeffs = np.polyfit(x_arr, y_arr, self.deleteConstantPolynomOrder.value())
            for i, x in enumerate(x_arr):
                y_arr[i] -= polynom(x, *coeffs)

        N = len(x_arr)
        T = (x_arr[0] - x_arr[1])
        spectr = fft(y_arr)
        freq = fftfreq(N, T)
        right_freq = list(np.flip(freq[N // 2 + 1:]))
        right_freq.insert(0, 0.0)
        A = list(np.flip(np.abs(spectr)[N // 2 + 1:]) / (N / 2))
        A.insert(0, np.abs(spectr[0]) / (N / 2))

        F = list(np.rad2deg(np.flip(np.angle(spectr)[N // 2 + 1:])))
        F.insert(0, np.rad2deg(np.angle(spectr[0])))

        self.__fftWindow.dashboard_a.delete_all_plots()
        self.__fftWindow.dashboard_f.delete_all_plots()
        self.__fftWindow.dashboard_source.delete_all_plots()

        self.__fftWindow.dashboard_a.add_plot(right_freq, A, name='Амплитудный спектр', color="#f64a46", accurate=True)
        self.__fftWindow.dashboard_f.add_plot(right_freq, F, name='Фазовый спектр', color="#1560bd", accurate=True)
        self.__fftWindow.dashboard_source.add_plot(x_arr, y_arr, name='Оригинал', color="#1560bd")
        self.__fftWindow.setWindowTitle(f"Преобразование Фурье {plot.name}")
        self.__fftWindow.open()

    @pyqtSlot()
    def __filter_plot(self):
        plot = self.__plots[self.plotName.currentIndex()]
        x_arr = plot.X
        y_arr = plot.Y
        y_filtered = [y for y in y_arr]

        if self.movingAverageFilterBox.isChecked():
            mav = MovingAverageFilter(self.meanOrder.value())
            y_filtered = [mav.filter_data(y) for y in y_filtered]
        if self.expFilterBox.isChecked():
            filt = ExponentialFilter(self.expFilterCoeff.value())
            y_filtered = [filt.filter_data(y) for y in y_filtered]
        if self.medianFilterBox.isChecked():
            med = MedianFilter(self.medianFilterOrder.value())
            y_filtered = [med.filter_data(y) for y in y_filtered]

        self.__dashboard.delete_plot(f"{self.plotName.currentText()} (фильтрация)")
        self.__dashboard.add_plot(np.array(x_arr), y_filtered,
                                name=f"{self.plotName.currentText()} (фильтрация)")
        self.__dashboard._force_redraw()

    @pyqtSlot()
    def __fit(self, i0=None, ik=None):
        plot = self.__plots[self.plotName.currentIndex()]

        X_array = plot.X
        Y_array = plot.Y
        if i0 is not None and ik is not None:
            X_array = X_array[i0:ik + 1]
            Y_array = Y_array[i0:ik + 1]

        approximation_successful = False
        X = []
        Y = []

        # линейная аппроскимация
        if self.linearApprox.isChecked():
            coeffs = np.polyfit(X_array, Y_array, 1)
            X = np.arange(X_array[0], X_array[-1], 0.1)
            Y = [polynom(x, *coeffs) for x in X]
            approximation_successful = True
            self.__equation = f"y(x) = {coeffs[0]:.3f}x + {coeffs[1]:.3f}"

        # полиномиальная аппроксимация
        elif self.polyApprox.isChecked():
            coeffs = np.polyfit(X_array, Y_array, self.polyPower.value())
            X = np.arange(X_array[0], X_array[-1], 0.1)
            Y = [polynom(x, *coeffs) for x in X]
            approximation_successful = True

            self.__equation = "y(x) ="
            for i, a in enumerate(coeffs):
                if a > 0 and i > 0:
                    self.__equation += '+'
                else:
                    self.__equation += '-'
                if i == len(coeffs) - 1:
                    if abs(a) < 0.01 or abs(a) >= 1000:
                        self.__equation += f" {abs(a):.3E}"
                    else:
                        self.__equation += f" {abs(a):.3f}"
                elif i == len(coeffs) - 2:
                    if abs(a) < 0.01 or abs(a) >= 1000:
                        self.__equation += f" {abs(a):.3E}x "
                    else:
                        self.__equation += f" {abs(a):.3f}x "
                else:
                    if abs(a) < 0.01 or abs(a) >= 1000:
                        self.__equation += f" {abs(a):.3E}x{get_upper_index(len(coeffs) - i - 1)} "
                    else:
                        self.__equation += f" {abs(a):.3f}x{get_upper_index(len(coeffs) - i - 1)} "

        # логарифмическая аппроксимация
        elif self.logApprox.isChecked():
            if any(x <= 0 for x in X_array):
                self.__show_error("Логарифм определён только для положительных чисел!")
                return
            try:
                params = curve_fit(logatirhmic_curve, X_array, Y_array)[0]
            except RuntimeError:
                self.__show_error("Логарифмическая аппроксимация не может быть выполнена!")
                return
            X = np.arange(X_array[0], X_array[-1], 0.1)

            Y = [logatirhmic_curve(x, *params) for x in X]
            approximation_successful = True

            a = self.__param_to_string(params[0], use_abs=False)
            b = self.__param_to_string(params[1], use_abs=True)
            self.__equation = f"y(x) = {a}ln x"
            if params[1] >= 0:
                self.__equation += " + "
            else:
                self.__equation += " - "
            self.__equation += b

        # экспоненциальная аппроксимация
        elif self.expApprox.isChecked():
            try:
                params = curve_fit(exp_curve, X_array, Y_array)[0]
            except RuntimeError:
                self.__show_error("Экспоненциальная аппроксимация не может быть выполнена!")
                return
            X = np.arange(X_array[0], X_array[-1], 0.1)
            Y = [exp_curve(x, *params) for x in X]
            if float("inf") in Y:
                self.__show_error("Экспоненциальная аппроксимация не может быть выполнена!")
                return
            approximation_successful = True

            a = self.__param_to_string(params[0], use_abs=False)
            b = self.__param_to_string(params[1], use_abs=False)
            c = self.__param_to_string(params[2], use_abs=True)
            self.__equation = f"{a} ∙ exp({b}x)"
            if params[2] > 0:
                self.__equation += f" + {c}"
            elif params[2] < 0:
                self.__equation += f" - {c}"

        # степенная аппроксимация
        elif self.powerApprox.isChecked():
            try:
                params = curve_fit(exponential_curve, X_array, Y_array)[0]
            except RuntimeError:
                self.__show_error("Степенная аппроксимация не может быть выполнена!")
                return
            X = np.arange(X_array[0], X_array[-1], 0.1)
            Y = [exponential_curve(x, *params) for x in X]
            approximation_successful = True

            a = self.__param_to_string(params[0], use_abs=False)
            b = self.__param_to_string(params[1], use_abs=False)
            c = self.__param_to_string(params[2], use_abs=False)
            d = self.__param_to_string(params[3], use_abs=True)
            self.__equation = f"{a} ∙ {b} ^ ({c}x)"
            if params[3] > 0:
                self.__equation += f" + {d}"
            elif params[3] < 0:
                self.__equation += f" - {d}"
        # скользящее среднее
        elif self.meanApprox.isChecked():
            mav = MovingAverageFilter(self.meanPeriods.value())
            Y = []
            for y in Y_array:
                Y.append(mav.filter_data(y))
            X = np.array(X_array)
            approximation_successful = True

        if approximation_successful:
            color = plot.pen.color()
            color = color.lighter(150).name()
            self.__dashboard.delete_plot(f"{self.plotName.currentText()} (тренд)")
            self.__dashboard.add_plot(X, Y, name=f"{self.plotName.currentText()} (тренд)", color=color, linestyle="dash-dot")

        if approximation_successful:
            self.__message("Аппроксимация выполнена успешно.")
        else:
            self.__message("Ошибка аппроксимации.")

    @staticmethod
    def __param_to_string(value, use_abs=False):
        if value == 0:
            return "0.000"
        if use_abs:
            return f"{abs(value):.3E}" if abs(value) < 0.01 or abs(value) >= 1000 else f"{abs(value):.3f}"
        else:
            return f"{value:.3E}" if abs(value) < 0.01 or abs(value) >= 1000 else f"{value:.3f}"
        
    @staticmethod
    def __choose_contrast_color(color: QColor):
        if mean((color.red(), color.green(), color.blue())) >= 128:
            return QColor(0, 0, 0)
        else:
            return QColor(255, 255, 255)
    
    @pyqtSlot()
    def __export_plot_to_csv(self):
        plt = self.__plots[self.plotName.currentIndex()]
        fileName, _ = QFileDialog.getSaveFileName(self, "Экспорт в файл", directory=plt.name, filter="CSV files (*.csv)")
        if len(fileName) > 0:
            with open(fileName, "w", newline='') as f:
                writer = csv.writer(f)
                writer.writerow([self.__dashboard.x_name, self.__dashboard.y_name])
                for x, y in zip(plt.X, plt.Y):
                    writer.writerow([x, y])

    @pyqtSlot()
    def __import_plot_from_csv(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Импорт из файла", filter="CSV files (*.csv)")
        if len(fileName) > 0:
            try:
                with open(fileName, "r") as f:
                    reader = csv.reader(f)
                    x_arr = list()
                    y_arrays = list()
                    for i, row in enumerate(reader):
                        if i == 0:
                            for j in range(len(row) - 1):
                                y_arrays.append(list())
                        try:
                            values = list(map(float, row))     
                        except:
                            continue
                        x_arr.append(values[0])
                        for j in range(len(values) - 1):
                            y_arrays[j].append(values[j + 1])
            except FileNotFoundError:
                self.__show_error("Файл не найден!")
            
            for i, y_arr in enumerate(y_arrays):
                self.__dashboard.add_plot(x_arr, y_arr, name=f"CSV_{i + 1}")
        
    def __show_error(self, error: str):
        self.errBox = QMessageBox()
        self.errBox.setIcon(QMessageBox.Icon.Warning)
        self.errBox.setWindowTitle("Ошибка!")
        self.errBox.setText(error)
        self.errBox.show()

    def __message(self, msg: str):
        self.statusbar.showMessage(msg, 5000)

    def closeEvent(self, a0):
        self.__derivWin.close()
        self.__fftWindow.close()