# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'cornplot_gui.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QCheckBox, QComboBox,
    QDoubleSpinBox, QFrame, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QLayout, QLineEdit,
    QMainWindow, QMenu, QMenuBar, QPushButton,
    QRadioButton, QSizePolicy, QSpacerItem, QSpinBox,
    QStatusBar, QTabWidget, QVBoxLayout, QWidget)

class Ui_CornplotGui(object):
    def setupUi(self, CornplotGui):
        if not CornplotGui.objectName():
            CornplotGui.setObjectName(u"CornplotGui")
        CornplotGui.resize(795, 610)
        self.newGraphEquationAction = QAction(CornplotGui)
        self.newGraphEquationAction.setObjectName(u"newGraphEquationAction")
        self.saveGraphAction = QAction(CornplotGui)
        self.saveGraphAction.setObjectName(u"saveGraphAction")
        self.openGraphAction = QAction(CornplotGui)
        self.openGraphAction.setObjectName(u"openGraphAction")
        self.aboutProgramAction = QAction(CornplotGui)
        self.aboutProgramAction.setObjectName(u"aboutProgramAction")
        self.exitAction = QAction(CornplotGui)
        self.exitAction.setObjectName(u"exitAction")
        self.exportToCSV = QAction(CornplotGui)
        self.exportToCSV.setObjectName(u"exportToCSV")
        self.importFromCSV = QAction(CornplotGui)
        self.importFromCSV.setObjectName(u"importFromCSV")
        self.deletePlotAction = QAction(CornplotGui)
        self.deletePlotAction.setObjectName(u"deletePlotAction")
        self.backgroundColorAction = QAction(CornplotGui)
        self.backgroundColorAction.setObjectName(u"backgroundColorAction")
        self.drawOriginAction = QAction(CornplotGui)
        self.drawOriginAction.setObjectName(u"drawOriginAction")
        self.drawOriginAction.setCheckable(True)
        self.drawTicksAction = QAction(CornplotGui)
        self.drawTicksAction.setObjectName(u"drawTicksAction")
        self.drawTicksAction.setCheckable(True)
        self.drawLabelsAction = QAction(CornplotGui)
        self.drawLabelsAction.setObjectName(u"drawLabelsAction")
        self.drawLabelsAction.setCheckable(True)
        self.fontAction = QAction(CornplotGui)
        self.fontAction.setObjectName(u"fontAction")
        self.minorGridAction = QAction(CornplotGui)
        self.minorGridAction.setObjectName(u"minorGridAction")
        self.minorGridAction.setCheckable(True)
        self.gridSolidAction = QAction(CornplotGui)
        self.gridSolidAction.setObjectName(u"gridSolidAction")
        self.gridSolidAction.setCheckable(True)
        self.dotGridAction = QAction(CornplotGui)
        self.dotGridAction.setObjectName(u"dotGridAction")
        self.dotGridAction.setCheckable(True)
        self.dotGridAction.setChecked(True)
        self.dashGridAction = QAction(CornplotGui)
        self.dashGridAction.setObjectName(u"dashGridAction")
        self.dashGridAction.setCheckable(True)
        self.majorGridAction = QAction(CornplotGui)
        self.majorGridAction.setObjectName(u"majorGridAction")
        self.majorGridAction.setCheckable(True)
        self.majorGridAction.setChecked(True)
        self.digitsAuto = QAction(CornplotGui)
        self.digitsAuto.setObjectName(u"digitsAuto")
        self.digitsAuto.setCheckable(True)
        self.digitsAuto.setChecked(True)
        self.action0 = QAction(CornplotGui)
        self.action0.setObjectName(u"action0")
        self.action0.setCheckable(True)
        self.action1 = QAction(CornplotGui)
        self.action1.setObjectName(u"action1")
        self.action1.setCheckable(True)
        self.action2 = QAction(CornplotGui)
        self.action2.setObjectName(u"action2")
        self.action2.setCheckable(True)
        self.action3 = QAction(CornplotGui)
        self.action3.setObjectName(u"action3")
        self.action3.setCheckable(True)
        self.action4 = QAction(CornplotGui)
        self.action4.setObjectName(u"action4")
        self.action4.setCheckable(True)
        self.action5 = QAction(CornplotGui)
        self.action5.setObjectName(u"action5")
        self.action5.setCheckable(True)
        self.action6 = QAction(CornplotGui)
        self.action6.setObjectName(u"action6")
        self.action6.setCheckable(True)
        self.centralwidget = QWidget(CornplotGui)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout_42 = QHBoxLayout()
        self.horizontalLayout_42.setObjectName(u"horizontalLayout_42")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_42.addItem(self.horizontalSpacer_2)

        self.okButton = QPushButton(self.centralwidget)
        self.okButton.setObjectName(u"okButton")

        self.horizontalLayout_42.addWidget(self.okButton)


        self.gridLayout.addLayout(self.horizontalLayout_42, 1, 1, 1, 1)

        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setAutoFillBackground(False)
        self.tabWidget.setTabShape(QTabWidget.Rounded)
        self.axlesTab = QWidget()
        self.axlesTab.setObjectName(u"axlesTab")
        self.axlesTab.setAutoFillBackground(True)
        self.gridLayout_25 = QGridLayout(self.axlesTab)
        self.gridLayout_25.setObjectName(u"gridLayout_25")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.groupBox_2 = QGroupBox(self.axlesTab)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.gridLayout_3 = QGridLayout(self.groupBox_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.xScaleSelect = QComboBox(self.groupBox_2)
        self.xScaleSelect.addItem("")
        self.xScaleSelect.addItem("")
        self.xScaleSelect.setObjectName(u"xScaleSelect")

        self.gridLayout_3.addWidget(self.xScaleSelect, 6, 0, 1, 1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_4 = QLabel(self.groupBox_2)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_4.addWidget(self.label_4)

        self.xMax = QDoubleSpinBox(self.groupBox_2)
        self.xMax.setObjectName(u"xMax")
        self.xMax.setEnabled(False)
        self.xMax.setMinimum(-2000000000.000000000000000)
        self.xMax.setMaximum(2000000000.000000000000000)
        self.xMax.setValue(10.000000000000000)

        self.horizontalLayout_4.addWidget(self.xMax)


        self.gridLayout_3.addLayout(self.horizontalLayout_4, 4, 0, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_3 = QLabel(self.groupBox_2)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_3.addWidget(self.label_3)

        self.xMin = QDoubleSpinBox(self.groupBox_2)
        self.xMin.setObjectName(u"xMin")
        self.xMin.setEnabled(False)
        self.xMin.setMinimum(-2000000000.000000000000000)
        self.xMin.setMaximum(2000000000.000000000000000)
        self.xMin.setValue(0.000000000000000)

        self.horizontalLayout_3.addWidget(self.xMin)


        self.gridLayout_3.addLayout(self.horizontalLayout_3, 3, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(self.groupBox_2)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.xStep = QDoubleSpinBox(self.groupBox_2)
        self.xStep.setObjectName(u"xStep")
        self.xStep.setEnabled(False)
        self.xStep.setMaximum(2000000000.000000000000000)
        self.xStep.setValue(1.000000000000000)

        self.horizontalLayout_2.addWidget(self.xStep)


        self.gridLayout_3.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.groupBox_2)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.xName = QLineEdit(self.groupBox_2)
        self.xName.setObjectName(u"xName")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.xName.sizePolicy().hasHeightForWidth())
        self.xName.setSizePolicy(sizePolicy)
        self.xName.setMaxLength(10)

        self.horizontalLayout.addWidget(self.xName)


        self.gridLayout_3.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.xAuto = QCheckBox(self.groupBox_2)
        self.xAuto.setObjectName(u"xAuto")
        self.xAuto.setLayoutDirection(Qt.LeftToRight)
        self.xAuto.setChecked(True)

        self.horizontalLayout_12.addWidget(self.xAuto)

        self.xTicks = QCheckBox(self.groupBox_2)
        self.xTicks.setObjectName(u"xTicks")
        self.xTicks.setLayoutDirection(Qt.LeftToRight)

        self.horizontalLayout_12.addWidget(self.xTicks)

        self.xLabelCheck = QCheckBox(self.groupBox_2)
        self.xLabelCheck.setObjectName(u"xLabelCheck")

        self.horizontalLayout_12.addWidget(self.xLabelCheck)


        self.gridLayout_3.addLayout(self.horizontalLayout_12, 1, 0, 1, 1)

        self.groupBox = QGroupBox(self.groupBox_2)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_4 = QGridLayout(self.groupBox)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.xTypeNormal = QRadioButton(self.groupBox)
        self.xTypeNormal.setObjectName(u"xTypeNormal")
        self.xTypeNormal.setChecked(True)

        self.gridLayout_4.addWidget(self.xTypeNormal, 0, 0, 1, 1)

        self.xTypeTime = QRadioButton(self.groupBox)
        self.xTypeTime.setObjectName(u"xTypeTime")

        self.gridLayout_4.addWidget(self.xTypeTime, 1, 0, 1, 1)


        self.gridLayout_3.addWidget(self.groupBox, 8, 0, 1, 1)

        self.gridGroup = QGroupBox(self.groupBox_2)
        self.gridGroup.setObjectName(u"gridGroup")
        self.gridLayout_2 = QGridLayout(self.gridGroup)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label_10 = QLabel(self.gridGroup)
        self.label_10.setObjectName(u"label_10")

        self.horizontalLayout_11.addWidget(self.label_10)

        self.label_11 = QLabel(self.gridGroup)
        self.label_11.setObjectName(u"label_11")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy1)
        self.label_11.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_11.addWidget(self.label_11)

        self.label_12 = QLabel(self.gridGroup)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_11.addWidget(self.label_12)

        self.label_13 = QLabel(self.gridGroup)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_11.addWidget(self.label_13)


        self.verticalLayout_3.addLayout(self.horizontalLayout_11)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.majorTicksCheckX = QCheckBox(self.gridGroup)
        self.majorTicksCheckX.setObjectName(u"majorTicksCheckX")
        self.majorTicksCheckX.setChecked(True)

        self.horizontalLayout_9.addWidget(self.majorTicksCheckX)

        self.majorTicksX = QComboBox(self.gridGroup)
        self.majorTicksX.addItem("")
        self.majorTicksX.addItem("")
        self.majorTicksX.addItem("")
        self.majorTicksX.setObjectName(u"majorTicksX")

        self.horizontalLayout_9.addWidget(self.majorTicksX)

        self.majorTicksWidthX = QDoubleSpinBox(self.gridGroup)
        self.majorTicksWidthX.setObjectName(u"majorTicksWidthX")
        self.majorTicksWidthX.setWrapping(False)
        self.majorTicksWidthX.setFrame(True)
        self.majorTicksWidthX.setMinimum(0.250000000000000)
        self.majorTicksWidthX.setMaximum(10.000000000000000)
        self.majorTicksWidthX.setSingleStep(0.250000000000000)
        self.majorTicksWidthX.setValue(1.000000000000000)

        self.horizontalLayout_9.addWidget(self.majorTicksWidthX)

        self.label_9 = QLabel(self.gridGroup)
        self.label_9.setObjectName(u"label_9")

        self.horizontalLayout_9.addWidget(self.label_9)


        self.verticalLayout_3.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.minorTicksCheckX = QCheckBox(self.gridGroup)
        self.minorTicksCheckX.setObjectName(u"minorTicksCheckX")

        self.horizontalLayout_10.addWidget(self.minorTicksCheckX)

        self.minorTicksX = QComboBox(self.gridGroup)
        self.minorTicksX.addItem("")
        self.minorTicksX.addItem("")
        self.minorTicksX.addItem("")
        self.minorTicksX.setObjectName(u"minorTicksX")
        self.minorTicksX.setEnabled(False)

        self.horizontalLayout_10.addWidget(self.minorTicksX)

        self.minorTicksWidthX = QDoubleSpinBox(self.gridGroup)
        self.minorTicksWidthX.setObjectName(u"minorTicksWidthX")
        self.minorTicksWidthX.setEnabled(False)
        self.minorTicksWidthX.setWrapping(False)
        self.minorTicksWidthX.setFrame(True)
        self.minorTicksWidthX.setMinimum(0.250000000000000)
        self.minorTicksWidthX.setMaximum(10.000000000000000)
        self.minorTicksWidthX.setSingleStep(0.250000000000000)
        self.minorTicksWidthX.setValue(0.500000000000000)

        self.horizontalLayout_10.addWidget(self.minorTicksWidthX)

        self.minorTicksStepX = QSpinBox(self.gridGroup)
        self.minorTicksStepX.setObjectName(u"minorTicksStepX")
        self.minorTicksStepX.setEnabled(False)
        self.minorTicksStepX.setWrapping(False)
        self.minorTicksStepX.setFrame(True)
        self.minorTicksStepX.setMinimum(2)
        self.minorTicksStepX.setMaximum(10)
        self.minorTicksStepX.setValue(5)

        self.horizontalLayout_10.addWidget(self.minorTicksStepX)


        self.verticalLayout_3.addLayout(self.horizontalLayout_10)


        self.gridLayout_2.addLayout(self.verticalLayout_3, 0, 0, 1, 1)

        self.originCheckX = QCheckBox(self.gridGroup)
        self.originCheckX.setObjectName(u"originCheckX")
        font = QFont()
        font.setKerning(False)
        self.originCheckX.setFont(font)
        self.originCheckX.setLayoutDirection(Qt.LeftToRight)
        self.originCheckX.setChecked(False)
        self.originCheckX.setTristate(False)

        self.gridLayout_2.addWidget(self.originCheckX, 1, 0, 1, 1)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.label_14 = QLabel(self.gridGroup)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setEnabled(False)

        self.horizontalLayout_13.addWidget(self.label_14)

        self.originWidthX = QDoubleSpinBox(self.gridGroup)
        self.originWidthX.setObjectName(u"originWidthX")
        self.originWidthX.setEnabled(False)
        self.originWidthX.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.originWidthX.setCorrectionMode(QAbstractSpinBox.CorrectToPreviousValue)
        self.originWidthX.setProperty(u"showGroupSeparator", False)
        self.originWidthX.setMinimum(0.250000000000000)
        self.originWidthX.setMaximum(10.000000000000000)
        self.originWidthX.setSingleStep(0.250000000000000)
        self.originWidthX.setValue(1.000000000000000)

        self.horizontalLayout_13.addWidget(self.originWidthX)


        self.gridLayout_2.addLayout(self.horizontalLayout_13, 2, 0, 1, 1)


        self.gridLayout_3.addWidget(self.gridGroup, 7, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_3.addItem(self.verticalSpacer, 9, 0, 1, 1)

        self.horizontalLayout_56 = QHBoxLayout()
        self.horizontalLayout_56.setObjectName(u"horizontalLayout_56")
        self.label_65 = QLabel(self.groupBox_2)
        self.label_65.setObjectName(u"label_65")

        self.horizontalLayout_56.addWidget(self.label_65)

        self.horizontalLayout_59 = QHBoxLayout()
        self.horizontalLayout_59.setObjectName(u"horizontalLayout_59")
        self.xDivisor = QSpinBox(self.groupBox_2)
        self.xDivisor.setObjectName(u"xDivisor")
        self.xDivisor.setMinimum(1)
        self.xDivisor.setMaximum(1000000000)

        self.horizontalLayout_59.addWidget(self.xDivisor)

        self.acceptXdivisor = QPushButton(self.groupBox_2)
        self.acceptXdivisor.setObjectName(u"acceptXdivisor")

        self.horizontalLayout_59.addWidget(self.acceptXdivisor)


        self.horizontalLayout_56.addLayout(self.horizontalLayout_59)


        self.gridLayout_3.addLayout(self.horizontalLayout_56, 5, 0, 1, 1)


        self.horizontalLayout_16.addWidget(self.groupBox_2)

        self.groupBox_3 = QGroupBox(self.axlesTab)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.gridLayout_5 = QGridLayout(self.groupBox_3)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.yScaleSelect = QComboBox(self.groupBox_3)
        self.yScaleSelect.addItem("")
        self.yScaleSelect.addItem("")
        self.yScaleSelect.setObjectName(u"yScaleSelect")

        self.gridLayout_5.addWidget(self.yScaleSelect, 6, 0, 1, 1)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_8 = QLabel(self.groupBox_3)
        self.label_8.setObjectName(u"label_8")

        self.horizontalLayout_8.addWidget(self.label_8)

        self.yMax = QDoubleSpinBox(self.groupBox_3)
        self.yMax.setObjectName(u"yMax")
        self.yMax.setEnabled(False)
        self.yMax.setMinimum(-2000000000.000000000000000)
        self.yMax.setMaximum(2000000000.000000000000000)
        self.yMax.setValue(1.000000000000000)

        self.horizontalLayout_8.addWidget(self.yMax)


        self.gridLayout_5.addLayout(self.horizontalLayout_8, 4, 0, 1, 1)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_5 = QLabel(self.groupBox_3)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_5.addWidget(self.label_5)

        self.yName = QLineEdit(self.groupBox_3)
        self.yName.setObjectName(u"yName")
        sizePolicy.setHeightForWidth(self.yName.sizePolicy().hasHeightForWidth())
        self.yName.setSizePolicy(sizePolicy)
        self.yName.setMaxLength(10)

        self.horizontalLayout_5.addWidget(self.yName)


        self.gridLayout_5.addLayout(self.horizontalLayout_5, 0, 0, 1, 1)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_7 = QLabel(self.groupBox_3)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_7.addWidget(self.label_7)

        self.yMin = QDoubleSpinBox(self.groupBox_3)
        self.yMin.setObjectName(u"yMin")
        self.yMin.setEnabled(False)
        self.yMin.setMinimum(-2000000000.000000000000000)
        self.yMin.setMaximum(2000000000.000000000000000)
        self.yMin.setValue(0.000000000000000)

        self.horizontalLayout_7.addWidget(self.yMin)


        self.gridLayout_5.addLayout(self.horizontalLayout_7, 3, 0, 1, 1)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.yAuto = QCheckBox(self.groupBox_3)
        self.yAuto.setObjectName(u"yAuto")
        self.yAuto.setLayoutDirection(Qt.LeftToRight)
        self.yAuto.setChecked(True)

        self.horizontalLayout_14.addWidget(self.yAuto)

        self.yTicks = QCheckBox(self.groupBox_3)
        self.yTicks.setObjectName(u"yTicks")
        self.yTicks.setLayoutDirection(Qt.LeftToRight)

        self.horizontalLayout_14.addWidget(self.yTicks)

        self.yLabelCheck = QCheckBox(self.groupBox_3)
        self.yLabelCheck.setObjectName(u"yLabelCheck")

        self.horizontalLayout_14.addWidget(self.yLabelCheck)


        self.gridLayout_5.addLayout(self.horizontalLayout_14, 1, 0, 1, 1)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_6 = QLabel(self.groupBox_3)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_6.addWidget(self.label_6)

        self.yStep = QDoubleSpinBox(self.groupBox_3)
        self.yStep.setObjectName(u"yStep")
        self.yStep.setEnabled(False)
        self.yStep.setMaximum(2000000000.000000000000000)
        self.yStep.setSingleStep(0.500000000000000)
        self.yStep.setValue(0.250000000000000)

        self.horizontalLayout_6.addWidget(self.yStep)


        self.gridLayout_5.addLayout(self.horizontalLayout_6, 2, 0, 1, 1)

        self.gridGroup_2 = QGroupBox(self.groupBox_3)
        self.gridGroup_2.setObjectName(u"gridGroup_2")
        self.gridLayout_7 = QGridLayout(self.gridGroup_2)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.verticalLayout_14 = QVBoxLayout()
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.label_27 = QLabel(self.gridGroup_2)
        self.label_27.setObjectName(u"label_27")

        self.horizontalLayout_15.addWidget(self.label_27)

        self.label_28 = QLabel(self.gridGroup_2)
        self.label_28.setObjectName(u"label_28")
        sizePolicy1.setHeightForWidth(self.label_28.sizePolicy().hasHeightForWidth())
        self.label_28.setSizePolicy(sizePolicy1)
        self.label_28.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_15.addWidget(self.label_28)

        self.label_29 = QLabel(self.gridGroup_2)
        self.label_29.setObjectName(u"label_29")
        self.label_29.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_15.addWidget(self.label_29)

        self.label_60 = QLabel(self.gridGroup_2)
        self.label_60.setObjectName(u"label_60")
        self.label_60.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_15.addWidget(self.label_60)


        self.verticalLayout_14.addLayout(self.horizontalLayout_15)

        self.horizontalLayout_51 = QHBoxLayout()
        self.horizontalLayout_51.setObjectName(u"horizontalLayout_51")
        self.majorTicksCheckY = QCheckBox(self.gridGroup_2)
        self.majorTicksCheckY.setObjectName(u"majorTicksCheckY")
        self.majorTicksCheckY.setChecked(True)

        self.horizontalLayout_51.addWidget(self.majorTicksCheckY)

        self.majorTicksY = QComboBox(self.gridGroup_2)
        self.majorTicksY.addItem("")
        self.majorTicksY.addItem("")
        self.majorTicksY.addItem("")
        self.majorTicksY.setObjectName(u"majorTicksY")

        self.horizontalLayout_51.addWidget(self.majorTicksY)

        self.majorTicksWidthY = QDoubleSpinBox(self.gridGroup_2)
        self.majorTicksWidthY.setObjectName(u"majorTicksWidthY")
        self.majorTicksWidthY.setWrapping(False)
        self.majorTicksWidthY.setFrame(True)
        self.majorTicksWidthY.setMinimum(0.250000000000000)
        self.majorTicksWidthY.setMaximum(10.000000000000000)
        self.majorTicksWidthY.setSingleStep(0.250000000000000)
        self.majorTicksWidthY.setValue(1.000000000000000)

        self.horizontalLayout_51.addWidget(self.majorTicksWidthY)

        self.label_61 = QLabel(self.gridGroup_2)
        self.label_61.setObjectName(u"label_61")

        self.horizontalLayout_51.addWidget(self.label_61)


        self.verticalLayout_14.addLayout(self.horizontalLayout_51)

        self.horizontalLayout_52 = QHBoxLayout()
        self.horizontalLayout_52.setObjectName(u"horizontalLayout_52")
        self.minorTicksCheckY = QCheckBox(self.gridGroup_2)
        self.minorTicksCheckY.setObjectName(u"minorTicksCheckY")

        self.horizontalLayout_52.addWidget(self.minorTicksCheckY)

        self.minorTicksY = QComboBox(self.gridGroup_2)
        self.minorTicksY.addItem("")
        self.minorTicksY.addItem("")
        self.minorTicksY.addItem("")
        self.minorTicksY.setObjectName(u"minorTicksY")
        self.minorTicksY.setEnabled(False)

        self.horizontalLayout_52.addWidget(self.minorTicksY)

        self.minorTicksWidthY = QDoubleSpinBox(self.gridGroup_2)
        self.minorTicksWidthY.setObjectName(u"minorTicksWidthY")
        self.minorTicksWidthY.setEnabled(False)
        self.minorTicksWidthY.setWrapping(False)
        self.minorTicksWidthY.setFrame(True)
        self.minorTicksWidthY.setMinimum(0.250000000000000)
        self.minorTicksWidthY.setMaximum(10.000000000000000)
        self.minorTicksWidthY.setSingleStep(0.250000000000000)
        self.minorTicksWidthY.setValue(0.500000000000000)

        self.horizontalLayout_52.addWidget(self.minorTicksWidthY)

        self.minorTicksStepY = QSpinBox(self.gridGroup_2)
        self.minorTicksStepY.setObjectName(u"minorTicksStepY")
        self.minorTicksStepY.setEnabled(False)
        self.minorTicksStepY.setWrapping(False)
        self.minorTicksStepY.setFrame(True)
        self.minorTicksStepY.setMinimum(2)
        self.minorTicksStepY.setMaximum(10)
        self.minorTicksStepY.setValue(5)

        self.horizontalLayout_52.addWidget(self.minorTicksStepY)


        self.verticalLayout_14.addLayout(self.horizontalLayout_52)


        self.gridLayout_7.addLayout(self.verticalLayout_14, 0, 0, 1, 1)

        self.originCheckY = QCheckBox(self.gridGroup_2)
        self.originCheckY.setObjectName(u"originCheckY")
        self.originCheckY.setFont(font)
        self.originCheckY.setLayoutDirection(Qt.LeftToRight)
        self.originCheckY.setChecked(False)
        self.originCheckY.setTristate(False)

        self.gridLayout_7.addWidget(self.originCheckY, 1, 0, 1, 1)

        self.horizontalLayout_53 = QHBoxLayout()
        self.horizontalLayout_53.setObjectName(u"horizontalLayout_53")
        self.label_62 = QLabel(self.gridGroup_2)
        self.label_62.setObjectName(u"label_62")
        self.label_62.setEnabled(False)

        self.horizontalLayout_53.addWidget(self.label_62)

        self.originWidthY = QDoubleSpinBox(self.gridGroup_2)
        self.originWidthY.setObjectName(u"originWidthY")
        self.originWidthY.setEnabled(False)
        self.originWidthY.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.originWidthY.setCorrectionMode(QAbstractSpinBox.CorrectToPreviousValue)
        self.originWidthY.setProperty(u"showGroupSeparator", False)
        self.originWidthY.setMinimum(0.250000000000000)
        self.originWidthY.setMaximum(10.000000000000000)
        self.originWidthY.setSingleStep(0.250000000000000)
        self.originWidthY.setValue(1.000000000000000)

        self.horizontalLayout_53.addWidget(self.originWidthY)


        self.gridLayout_7.addLayout(self.horizontalLayout_53, 2, 0, 1, 1)


        self.gridLayout_5.addWidget(self.gridGroup_2, 7, 0, 1, 1)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_5.addItem(self.verticalSpacer_6, 8, 0, 1, 1)

        self.horizontalLayout_60 = QHBoxLayout()
        self.horizontalLayout_60.setObjectName(u"horizontalLayout_60")
        self.label_66 = QLabel(self.groupBox_3)
        self.label_66.setObjectName(u"label_66")

        self.horizontalLayout_60.addWidget(self.label_66)

        self.horizontalLayout_61 = QHBoxLayout()
        self.horizontalLayout_61.setObjectName(u"horizontalLayout_61")
        self.yDivisor = QSpinBox(self.groupBox_3)
        self.yDivisor.setObjectName(u"yDivisor")
        self.yDivisor.setMinimum(1)
        self.yDivisor.setMaximum(1000000000)

        self.horizontalLayout_61.addWidget(self.yDivisor)

        self.acceptYdivisor = QPushButton(self.groupBox_3)
        self.acceptYdivisor.setObjectName(u"acceptYdivisor")

        self.horizontalLayout_61.addWidget(self.acceptYdivisor)


        self.horizontalLayout_60.addLayout(self.horizontalLayout_61)


        self.gridLayout_5.addLayout(self.horizontalLayout_60, 5, 0, 1, 1)


        self.horizontalLayout_16.addWidget(self.groupBox_3)


        self.verticalLayout.addLayout(self.horizontalLayout_16)


        self.gridLayout_25.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.tabWidget.addTab(self.axlesTab, "")
        self.plotTab = QWidget()
        self.plotTab.setObjectName(u"plotTab")
        self.plotTab.setAutoFillBackground(True)
        self.gridLayout_23 = QGridLayout(self.plotTab)
        self.gridLayout_23.setObjectName(u"gridLayout_23")
        self.verticalLayout_10 = QVBoxLayout()
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.horizontalLayout_32 = QHBoxLayout()
        self.horizontalLayout_32.setObjectName(u"horizontalLayout_32")
        self.label_36 = QLabel(self.plotTab)
        self.label_36.setObjectName(u"label_36")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_36.sizePolicy().hasHeightForWidth())
        self.label_36.setSizePolicy(sizePolicy2)
        font1 = QFont()
        font1.setPointSize(10)
        self.label_36.setFont(font1)

        self.horizontalLayout_32.addWidget(self.label_36)

        self.pltImage = QLabel(self.plotTab)
        self.pltImage.setObjectName(u"pltImage")
        sizePolicy1.setHeightForWidth(self.pltImage.sizePolicy().hasHeightForWidth())
        self.pltImage.setSizePolicy(sizePolicy1)
        self.pltImage.setMinimumSize(QSize(0, 0))

        self.horizontalLayout_32.addWidget(self.pltImage)

        self.plotName = QComboBox(self.plotTab)
        self.plotName.setObjectName(u"plotName")
        font2 = QFont()
        font2.setFamilies([u"Bahnschrift"])
        font2.setPointSize(11)
        self.plotName.setFont(font2)

        self.horizontalLayout_32.addWidget(self.plotName)


        self.verticalLayout_10.addLayout(self.horizontalLayout_32)

        self.tabWidget_2 = QTabWidget(self.plotTab)
        self.tabWidget_2.setObjectName(u"tabWidget_2")
        self.tabWidget_2.setAutoFillBackground(True)
        self.tabWidget_2.setTabPosition(QTabWidget.North)
        self.tabWidget_2.setTabShape(QTabWidget.Rounded)
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.tab.setAutoFillBackground(False)
        self.gridLayout_22 = QGridLayout(self.tab)
        self.gridLayout_22.setObjectName(u"gridLayout_22")
        self.groupBox_5 = QGroupBox(self.tab)
        self.groupBox_5.setObjectName(u"groupBox_5")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.groupBox_5.sizePolicy().hasHeightForWidth())
        self.groupBox_5.setSizePolicy(sizePolicy3)
        self.gridLayout_8 = QGridLayout(self.groupBox_5)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.accurateDrawingCheckbox = QCheckBox(self.groupBox_5)
        self.accurateDrawingCheckbox.setObjectName(u"accurateDrawingCheckbox")

        self.gridLayout_8.addWidget(self.accurateDrawingCheckbox, 7, 0, 1, 1)

        self.line = QFrame(self.groupBox_5)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_8.addWidget(self.line, 2, 0, 1, 1)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.drawLine = QCheckBox(self.groupBox_5)
        self.drawLine.setObjectName(u"drawLine")
        self.drawLine.setEnabled(False)
        self.drawLine.setChecked(True)

        self.verticalLayout_6.addWidget(self.drawLine)

        self.plotLineStyle = QComboBox(self.groupBox_5)
        self.plotLineStyle.addItem("")
        self.plotLineStyle.addItem("")
        self.plotLineStyle.addItem("")
        self.plotLineStyle.addItem("")
        self.plotLineStyle.addItem("")
        self.plotLineStyle.setObjectName(u"plotLineStyle")

        self.verticalLayout_6.addWidget(self.plotLineStyle)

        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.label_16 = QLabel(self.groupBox_5)
        self.label_16.setObjectName(u"label_16")

        self.horizontalLayout_19.addWidget(self.label_16)

        self.lineWidth = QDoubleSpinBox(self.groupBox_5)
        self.lineWidth.setObjectName(u"lineWidth")
        self.lineWidth.setMinimum(0.250000000000000)
        self.lineWidth.setMaximum(8.000000000000000)
        self.lineWidth.setSingleStep(0.250000000000000)
        self.lineWidth.setValue(2.000000000000000)

        self.horizontalLayout_19.addWidget(self.lineWidth)


        self.verticalLayout_6.addLayout(self.horizontalLayout_19)


        self.gridLayout_8.addLayout(self.verticalLayout_6, 1, 0, 1, 1)

        self.line_2 = QFrame(self.groupBox_5)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_8.addWidget(self.line_2, 5, 0, 1, 1)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.drawMarkers = QCheckBox(self.groupBox_5)
        self.drawMarkers.setObjectName(u"drawMarkers")

        self.verticalLayout_5.addWidget(self.drawMarkers)

        self.markerStyles = QComboBox(self.groupBox_5)
        self.markerStyles.addItem("")
        self.markerStyles.addItem("")
        self.markerStyles.setObjectName(u"markerStyles")

        self.verticalLayout_5.addWidget(self.markerStyles)

        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.label_15 = QLabel(self.groupBox_5)
        self.label_15.setObjectName(u"label_15")

        self.horizontalLayout_18.addWidget(self.label_15)

        self.markerWidth = QDoubleSpinBox(self.groupBox_5)
        self.markerWidth.setObjectName(u"markerWidth")
        self.markerWidth.setDecimals(0)
        self.markerWidth.setMinimum(1.000000000000000)
        self.markerWidth.setMaximum(20.000000000000000)
        self.markerWidth.setSingleStep(1.000000000000000)
        self.markerWidth.setValue(5.000000000000000)

        self.horizontalLayout_18.addWidget(self.markerWidth)


        self.verticalLayout_5.addLayout(self.horizontalLayout_18)


        self.gridLayout_8.addLayout(self.verticalLayout_5, 3, 0, 1, 1)

        self.colorButton = QPushButton(self.groupBox_5)
        self.colorButton.setObjectName(u"colorButton")

        self.gridLayout_8.addWidget(self.colorButton, 6, 0, 1, 1)


        self.gridLayout_22.addWidget(self.groupBox_5, 0, 0, 1, 1)

        self.verticalLayout_13 = QVBoxLayout()
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_13.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.verticalLayout_11 = QVBoxLayout()
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.horizontalLayout_44 = QHBoxLayout()
        self.horizontalLayout_44.setObjectName(u"horizontalLayout_44")
        self.label_41 = QLabel(self.tab)
        self.label_41.setObjectName(u"label_41")
        self.label_41.setFont(font1)

        self.horizontalLayout_44.addWidget(self.label_41)

        self.label_42 = QLabel(self.tab)
        self.label_42.setObjectName(u"label_42")
        self.label_42.setFont(font1)

        self.horizontalLayout_44.addWidget(self.label_42)

        self.pltXmin = QLineEdit(self.tab)
        self.pltXmin.setObjectName(u"pltXmin")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.pltXmin.sizePolicy().hasHeightForWidth())
        self.pltXmin.setSizePolicy(sizePolicy4)
        self.pltXmin.setFont(font1)
        self.pltXmin.setFrame(False)
        self.pltXmin.setAlignment(Qt.AlignCenter)
        self.pltXmin.setReadOnly(True)

        self.horizontalLayout_44.addWidget(self.pltXmin)

        self.label_43 = QLabel(self.tab)
        self.label_43.setObjectName(u"label_43")
        self.label_43.setFont(font1)

        self.horizontalLayout_44.addWidget(self.label_43)

        self.pltXmax = QLineEdit(self.tab)
        self.pltXmax.setObjectName(u"pltXmax")
        sizePolicy4.setHeightForWidth(self.pltXmax.sizePolicy().hasHeightForWidth())
        self.pltXmax.setSizePolicy(sizePolicy4)
        self.pltXmax.setFont(font1)
        self.pltXmax.setFrame(False)
        self.pltXmax.setAlignment(Qt.AlignCenter)
        self.pltXmax.setReadOnly(True)

        self.horizontalLayout_44.addWidget(self.pltXmax)

        self.label_44 = QLabel(self.tab)
        self.label_44.setObjectName(u"label_44")
        self.label_44.setFont(font1)

        self.horizontalLayout_44.addWidget(self.label_44)


        self.verticalLayout_11.addLayout(self.horizontalLayout_44)

        self.horizontalLayout_45 = QHBoxLayout()
        self.horizontalLayout_45.setObjectName(u"horizontalLayout_45")
        self.label_45 = QLabel(self.tab)
        self.label_45.setObjectName(u"label_45")
        self.label_45.setFont(font1)

        self.horizontalLayout_45.addWidget(self.label_45)

        self.label_46 = QLabel(self.tab)
        self.label_46.setObjectName(u"label_46")
        self.label_46.setFont(font1)

        self.horizontalLayout_45.addWidget(self.label_46)

        self.pltYmin = QLineEdit(self.tab)
        self.pltYmin.setObjectName(u"pltYmin")
        sizePolicy4.setHeightForWidth(self.pltYmin.sizePolicy().hasHeightForWidth())
        self.pltYmin.setSizePolicy(sizePolicy4)
        self.pltYmin.setFont(font1)
        self.pltYmin.setFrame(False)
        self.pltYmin.setAlignment(Qt.AlignCenter)
        self.pltYmin.setReadOnly(True)

        self.horizontalLayout_45.addWidget(self.pltYmin)

        self.label_47 = QLabel(self.tab)
        self.label_47.setObjectName(u"label_47")

        self.horizontalLayout_45.addWidget(self.label_47)

        self.pltYmax = QLineEdit(self.tab)
        self.pltYmax.setObjectName(u"pltYmax")
        sizePolicy4.setHeightForWidth(self.pltYmax.sizePolicy().hasHeightForWidth())
        self.pltYmax.setSizePolicy(sizePolicy4)
        self.pltYmax.setFont(font1)
        self.pltYmax.setFrame(False)
        self.pltYmax.setAlignment(Qt.AlignCenter)
        self.pltYmax.setReadOnly(True)

        self.horizontalLayout_45.addWidget(self.pltYmax)

        self.label_48 = QLabel(self.tab)
        self.label_48.setObjectName(u"label_48")
        self.label_48.setFont(font1)

        self.horizontalLayout_45.addWidget(self.label_48)


        self.verticalLayout_11.addLayout(self.horizontalLayout_45)


        self.verticalLayout_13.addLayout(self.verticalLayout_11)

        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.label_23 = QLabel(self.tab)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setFont(font1)

        self.horizontalLayout_17.addWidget(self.label_23)

        self.nPoints = QLineEdit(self.tab)
        self.nPoints.setObjectName(u"nPoints")
        sizePolicy.setHeightForWidth(self.nPoints.sizePolicy().hasHeightForWidth())
        self.nPoints.setSizePolicy(sizePolicy)
        self.nPoints.setFont(font1)
        self.nPoints.setFrame(False)
        self.nPoints.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.nPoints.setReadOnly(True)
        self.nPoints.setClearButtonEnabled(False)

        self.horizontalLayout_17.addWidget(self.nPoints)


        self.verticalLayout_13.addLayout(self.horizontalLayout_17)

        self.verticalSpacer_11 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_13.addItem(self.verticalSpacer_11)

        self.deletePlotButton = QPushButton(self.tab)
        self.deletePlotButton.setObjectName(u"deletePlotButton")

        self.verticalLayout_13.addWidget(self.deletePlotButton)


        self.gridLayout_22.addLayout(self.verticalLayout_13, 0, 1, 1, 1)

        self.verticalSpacer_12 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_22.addItem(self.verticalSpacer_12, 1, 0, 1, 1)

        self.tabWidget_2.addTab(self.tab, "")
        self.tab_5 = QWidget()
        self.tab_5.setObjectName(u"tab_5")
        self.gridLayout_16 = QGridLayout(self.tab_5)
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.approxGroup = QGroupBox(self.tab_5)
        self.approxGroup.setObjectName(u"approxGroup")
        self.gridLayout_9 = QGridLayout(self.approxGroup)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.horizontalLayout_20 = QHBoxLayout()
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.approxIntervalButton = QPushButton(self.approxGroup)
        self.approxIntervalButton.setObjectName(u"approxIntervalButton")

        self.horizontalLayout_20.addWidget(self.approxIntervalButton)

        self.approxButton = QPushButton(self.approxGroup)
        self.approxButton.setObjectName(u"approxButton")

        self.horizontalLayout_20.addWidget(self.approxButton)


        self.gridLayout_9.addLayout(self.horizontalLayout_20, 7, 0, 1, 1)

        self.powerApprox = QRadioButton(self.approxGroup)
        self.powerApprox.setObjectName(u"powerApprox")

        self.gridLayout_9.addWidget(self.powerApprox, 4, 0, 1, 1)

        self.logApprox = QRadioButton(self.approxGroup)
        self.logApprox.setObjectName(u"logApprox")

        self.gridLayout_9.addWidget(self.logApprox, 2, 0, 1, 1)

        self.linearApprox = QRadioButton(self.approxGroup)
        self.linearApprox.setObjectName(u"linearApprox")
        self.linearApprox.setChecked(True)

        self.gridLayout_9.addWidget(self.linearApprox, 0, 0, 1, 1)

        self.expApprox = QRadioButton(self.approxGroup)
        self.expApprox.setObjectName(u"expApprox")

        self.gridLayout_9.addWidget(self.expApprox, 3, 0, 1, 1)

        self.horizontalLayout_23 = QHBoxLayout()
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.meanApprox = QRadioButton(self.approxGroup)
        self.meanApprox.setObjectName(u"meanApprox")

        self.horizontalLayout_23.addWidget(self.meanApprox)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_23.addItem(self.horizontalSpacer_4)

        self.label_18 = QLabel(self.approxGroup)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setEnabled(False)

        self.horizontalLayout_23.addWidget(self.label_18)

        self.meanPeriods = QSpinBox(self.approxGroup)
        self.meanPeriods.setObjectName(u"meanPeriods")
        self.meanPeriods.setEnabled(False)
        font3 = QFont()
        font3.setBold(False)
        self.meanPeriods.setFont(font3)
        self.meanPeriods.setMinimum(2)
        self.meanPeriods.setValue(2)

        self.horizontalLayout_23.addWidget(self.meanPeriods)


        self.gridLayout_9.addLayout(self.horizontalLayout_23, 5, 0, 1, 1)

        self.horizontalLayout_21 = QHBoxLayout()
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.polyApprox = QRadioButton(self.approxGroup)
        self.polyApprox.setObjectName(u"polyApprox")

        self.horizontalLayout_21.addWidget(self.polyApprox)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_21.addItem(self.horizontalSpacer)

        self.label_17 = QLabel(self.approxGroup)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setEnabled(False)

        self.horizontalLayout_21.addWidget(self.label_17)

        self.polyPower = QSpinBox(self.approxGroup)
        self.polyPower.setObjectName(u"polyPower")
        self.polyPower.setEnabled(False)
        self.polyPower.setMinimum(2)
        self.polyPower.setValue(2)

        self.horizontalLayout_21.addWidget(self.polyPower)


        self.gridLayout_9.addLayout(self.horizontalLayout_21, 1, 0, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_9.addItem(self.verticalSpacer_3, 6, 0, 1, 1)

        self.equationButton = QPushButton(self.approxGroup)
        self.equationButton.setObjectName(u"equationButton")

        self.gridLayout_9.addWidget(self.equationButton, 8, 0, 1, 1)


        self.gridLayout_16.addWidget(self.approxGroup, 0, 1, 1, 1)

        self.filterGroup = QGroupBox(self.tab_5)
        self.filterGroup.setObjectName(u"filterGroup")
        self.gridLayout_15 = QGridLayout(self.filterGroup)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.doFiltering = QPushButton(self.filterGroup)
        self.doFiltering.setObjectName(u"doFiltering")

        self.gridLayout_15.addWidget(self.doFiltering, 4, 0, 1, 1)

        self.horizontalLayout_35 = QHBoxLayout()
        self.horizontalLayout_35.setObjectName(u"horizontalLayout_35")
        self.movingAverageFilterBox = QCheckBox(self.filterGroup)
        self.movingAverageFilterBox.setObjectName(u"movingAverageFilterBox")
        self.movingAverageFilterBox.setChecked(True)

        self.horizontalLayout_35.addWidget(self.movingAverageFilterBox)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_35.addItem(self.horizontalSpacer_3)

        self.horizontalLayout_36 = QHBoxLayout()
        self.horizontalLayout_36.setObjectName(u"horizontalLayout_36")
        self.label_38 = QLabel(self.filterGroup)
        self.label_38.setObjectName(u"label_38")

        self.horizontalLayout_36.addWidget(self.label_38)

        self.meanOrder = QSpinBox(self.filterGroup)
        self.meanOrder.setObjectName(u"meanOrder")
        self.meanOrder.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.meanOrder.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.meanOrder.setMinimum(2)
        self.meanOrder.setMaximum(999)
        self.meanOrder.setValue(10)

        self.horizontalLayout_36.addWidget(self.meanOrder)


        self.horizontalLayout_35.addLayout(self.horizontalLayout_36)


        self.gridLayout_15.addLayout(self.horizontalLayout_35, 0, 0, 1, 1)

        self.horizontalLayout_37 = QHBoxLayout()
        self.horizontalLayout_37.setObjectName(u"horizontalLayout_37")
        self.medianFilterBox = QCheckBox(self.filterGroup)
        self.medianFilterBox.setObjectName(u"medianFilterBox")

        self.horizontalLayout_37.addWidget(self.medianFilterBox)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_37.addItem(self.horizontalSpacer_6)

        self.horizontalLayout_38 = QHBoxLayout()
        self.horizontalLayout_38.setObjectName(u"horizontalLayout_38")
        self.label_39 = QLabel(self.filterGroup)
        self.label_39.setObjectName(u"label_39")

        self.horizontalLayout_38.addWidget(self.label_39)

        self.medianFilterOrder = QSpinBox(self.filterGroup)
        self.medianFilterOrder.setObjectName(u"medianFilterOrder")
        self.medianFilterOrder.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.medianFilterOrder.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.medianFilterOrder.setMinimum(3)
        self.medianFilterOrder.setMaximum(999)

        self.horizontalLayout_38.addWidget(self.medianFilterOrder)


        self.horizontalLayout_37.addLayout(self.horizontalLayout_38)


        self.gridLayout_15.addLayout(self.horizontalLayout_37, 2, 0, 1, 1)

        self.horizontalLayout_33 = QHBoxLayout()
        self.horizontalLayout_33.setObjectName(u"horizontalLayout_33")
        self.expFilterBox = QCheckBox(self.filterGroup)
        self.expFilterBox.setObjectName(u"expFilterBox")

        self.horizontalLayout_33.addWidget(self.expFilterBox)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_33.addItem(self.horizontalSpacer_5)

        self.horizontalLayout_34 = QHBoxLayout()
        self.horizontalLayout_34.setObjectName(u"horizontalLayout_34")
        self.label_37 = QLabel(self.filterGroup)
        self.label_37.setObjectName(u"label_37")

        self.horizontalLayout_34.addWidget(self.label_37)

        self.expFilterCoeff = QDoubleSpinBox(self.filterGroup)
        self.expFilterCoeff.setObjectName(u"expFilterCoeff")
        self.expFilterCoeff.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.expFilterCoeff.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.expFilterCoeff.setDecimals(2)
        self.expFilterCoeff.setMinimum(0.010000000000000)
        self.expFilterCoeff.setMaximum(1.000000000000000)
        self.expFilterCoeff.setSingleStep(0.010000000000000)
        self.expFilterCoeff.setValue(0.500000000000000)

        self.horizontalLayout_34.addWidget(self.expFilterCoeff)


        self.horizontalLayout_33.addLayout(self.horizontalLayout_34)


        self.gridLayout_15.addLayout(self.horizontalLayout_33, 1, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_15.addItem(self.verticalSpacer_2, 3, 0, 1, 1)


        self.gridLayout_16.addWidget(self.filterGroup, 0, 0, 1, 1)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_16.addItem(self.verticalSpacer_5, 1, 1, 1, 1)

        self.tabWidget_2.addTab(self.tab_5, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.gridLayout_18 = QGridLayout(self.tab_2)
        self.gridLayout_18.setObjectName(u"gridLayout_18")
        self.groupBox_7 = QGroupBox(self.tab_2)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.gridLayout_13 = QGridLayout(self.groupBox_7)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.groupBox_8 = QGroupBox(self.groupBox_7)
        self.groupBox_8.setObjectName(u"groupBox_8")
        self.gridLayout_10 = QGridLayout(self.groupBox_8)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.horizontalLayout_24 = QHBoxLayout()
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.label_20 = QLabel(self.groupBox_8)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setFont(font1)

        self.horizontalLayout_24.addWidget(self.label_20)

        self.yDiff = QLineEdit(self.groupBox_8)
        self.yDiff.setObjectName(u"yDiff")
        sizePolicy4.setHeightForWidth(self.yDiff.sizePolicy().hasHeightForWidth())
        self.yDiff.setSizePolicy(sizePolicy4)
        self.yDiff.setFont(font1)
        self.yDiff.setFrame(False)
        self.yDiff.setReadOnly(True)

        self.horizontalLayout_24.addWidget(self.yDiff)


        self.gridLayout_10.addLayout(self.horizontalLayout_24, 1, 0, 1, 1)

        self.horizontalLayout_22 = QHBoxLayout()
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.label_19 = QLabel(self.groupBox_8)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setFont(font1)

        self.horizontalLayout_22.addWidget(self.label_19)

        self.xDiff = QLineEdit(self.groupBox_8)
        self.xDiff.setObjectName(u"xDiff")
        sizePolicy4.setHeightForWidth(self.xDiff.sizePolicy().hasHeightForWidth())
        self.xDiff.setSizePolicy(sizePolicy4)
        self.xDiff.setFont(font1)
        self.xDiff.setFrame(False)
        self.xDiff.setReadOnly(True)

        self.horizontalLayout_22.addWidget(self.xDiff)


        self.gridLayout_10.addLayout(self.horizontalLayout_22, 0, 0, 1, 1)


        self.verticalLayout_8.addWidget(self.groupBox_8)

        self.groupBox_9 = QGroupBox(self.groupBox_7)
        self.groupBox_9.setObjectName(u"groupBox_9")
        self.gridLayout_11 = QGridLayout(self.groupBox_9)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.horizontalLayout_26 = QHBoxLayout()
        self.horizontalLayout_26.setObjectName(u"horizontalLayout_26")
        self.label_21 = QLabel(self.groupBox_9)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setFont(font1)

        self.horizontalLayout_26.addWidget(self.label_21)

        self.diffResult = QLineEdit(self.groupBox_9)
        self.diffResult.setObjectName(u"diffResult")
        sizePolicy4.setHeightForWidth(self.diffResult.sizePolicy().hasHeightForWidth())
        self.diffResult.setSizePolicy(sizePolicy4)
        self.diffResult.setFont(font1)
        self.diffResult.setFrame(False)
        self.diffResult.setReadOnly(True)

        self.horizontalLayout_26.addWidget(self.diffResult)


        self.gridLayout_11.addLayout(self.horizontalLayout_26, 0, 0, 1, 1)

        self.verticalSpacer_9 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_11.addItem(self.verticalSpacer_9, 1, 0, 1, 1)


        self.verticalLayout_8.addWidget(self.groupBox_9)


        self.gridLayout_13.addLayout(self.verticalLayout_8, 0, 0, 1, 1)

        self.horizontalLayout_25 = QHBoxLayout()
        self.horizontalLayout_25.setObjectName(u"horizontalLayout_25")
        self.diffPointSelect = QPushButton(self.groupBox_7)
        self.diffPointSelect.setObjectName(u"diffPointSelect")

        self.horizontalLayout_25.addWidget(self.diffPointSelect)

        self.diffSelectTwoPoints = QPushButton(self.groupBox_7)
        self.diffSelectTwoPoints.setObjectName(u"diffSelectTwoPoints")

        self.horizontalLayout_25.addWidget(self.diffSelectTwoPoints)

        self.diffSelectAll = QPushButton(self.groupBox_7)
        self.diffSelectAll.setObjectName(u"diffSelectAll")

        self.horizontalLayout_25.addWidget(self.diffSelectAll)


        self.gridLayout_13.addLayout(self.horizontalLayout_25, 2, 0, 1, 2)

        self.groupBox_10 = QGroupBox(self.groupBox_7)
        self.groupBox_10.setObjectName(u"groupBox_10")
        self.gridLayout_12 = QGridLayout(self.groupBox_10)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.horizontalLayout_27 = QHBoxLayout()
        self.horizontalLayout_27.setObjectName(u"horizontalLayout_27")
        self.label_53 = QLabel(self.groupBox_10)
        self.label_53.setObjectName(u"label_53")
        self.label_53.setFont(font1)

        self.horizontalLayout_27.addWidget(self.label_53)

        self.label_24 = QLabel(self.groupBox_10)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setFont(font1)

        self.horizontalLayout_27.addWidget(self.label_24)

        self.xDiffBegin = QLineEdit(self.groupBox_10)
        self.xDiffBegin.setObjectName(u"xDiffBegin")
        self.xDiffBegin.setFont(font1)
        self.xDiffBegin.setFrame(False)
        self.xDiffBegin.setAlignment(Qt.AlignCenter)
        self.xDiffBegin.setReadOnly(True)

        self.horizontalLayout_27.addWidget(self.xDiffBegin)

        self.label_26 = QLabel(self.groupBox_10)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setFont(font1)

        self.horizontalLayout_27.addWidget(self.label_26)

        self.xDiffEnd = QLineEdit(self.groupBox_10)
        self.xDiffEnd.setObjectName(u"xDiffEnd")
        self.xDiffEnd.setFont(font1)
        self.xDiffEnd.setFrame(False)
        self.xDiffEnd.setAlignment(Qt.AlignCenter)
        self.xDiffEnd.setReadOnly(True)

        self.horizontalLayout_27.addWidget(self.xDiffEnd)

        self.label_25 = QLabel(self.groupBox_10)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setFont(font1)

        self.horizontalLayout_27.addWidget(self.label_25)


        self.gridLayout_12.addLayout(self.horizontalLayout_27, 0, 0, 1, 1)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_12.addItem(self.verticalSpacer_4, 1, 0, 1, 1)


        self.gridLayout_13.addWidget(self.groupBox_10, 0, 1, 1, 1)

        self.diffNewWindow = QCheckBox(self.groupBox_7)
        self.diffNewWindow.setObjectName(u"diffNewWindow")
        self.diffNewWindow.setChecked(True)

        self.gridLayout_13.addWidget(self.diffNewWindow, 1, 0, 1, 1)


        self.gridLayout_18.addWidget(self.groupBox_7, 0, 0, 1, 1)

        self.verticalSpacer_10 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_18.addItem(self.verticalSpacer_10, 1, 0, 1, 1)

        self.tabWidget_2.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.gridLayout_19 = QGridLayout(self.tab_3)
        self.gridLayout_19.setObjectName(u"gridLayout_19")
        self.groupBox_14 = QGroupBox(self.tab_3)
        self.groupBox_14.setObjectName(u"groupBox_14")

        self.gridLayout_19.addWidget(self.groupBox_14, 1, 1, 1, 1)

        self.integralGroupBox_2 = QGroupBox(self.tab_3)
        self.integralGroupBox_2.setObjectName(u"integralGroupBox_2")
        self.integralGroupBox_2.setLayoutDirection(Qt.LeftToRight)
        self.integralGroupBox_2.setFlat(False)
        self.integralGroupBox_2.setCheckable(False)
        self.gridLayout_17 = QGridLayout(self.integralGroupBox_2)
        self.gridLayout_17.setObjectName(u"gridLayout_17")
        self.verticalLayout_12 = QVBoxLayout()
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.horizontalLayout_41 = QHBoxLayout()
        self.horizontalLayout_41.setObjectName(u"horizontalLayout_41")
        self.label_49 = QLabel(self.integralGroupBox_2)
        self.label_49.setObjectName(u"label_49")
        self.label_49.setFont(font1)

        self.horizontalLayout_41.addWidget(self.label_49)

        self.label_50 = QLabel(self.integralGroupBox_2)
        self.label_50.setObjectName(u"label_50")
        self.label_50.setFont(font1)

        self.horizontalLayout_41.addWidget(self.label_50)

        self.xMeanBegin = QLineEdit(self.integralGroupBox_2)
        self.xMeanBegin.setObjectName(u"xMeanBegin")
        sizePolicy4.setHeightForWidth(self.xMeanBegin.sizePolicy().hasHeightForWidth())
        self.xMeanBegin.setSizePolicy(sizePolicy4)
        self.xMeanBegin.setFont(font1)
        self.xMeanBegin.setFrame(False)
        self.xMeanBegin.setAlignment(Qt.AlignCenter)
        self.xMeanBegin.setReadOnly(True)

        self.horizontalLayout_41.addWidget(self.xMeanBegin)

        self.label_51 = QLabel(self.integralGroupBox_2)
        self.label_51.setObjectName(u"label_51")
        self.label_51.setFont(font1)

        self.horizontalLayout_41.addWidget(self.label_51)

        self.xMeanEnd = QLineEdit(self.integralGroupBox_2)
        self.xMeanEnd.setObjectName(u"xMeanEnd")
        sizePolicy4.setHeightForWidth(self.xMeanEnd.sizePolicy().hasHeightForWidth())
        self.xMeanEnd.setSizePolicy(sizePolicy4)
        self.xMeanEnd.setFont(font1)
        self.xMeanEnd.setFrame(False)
        self.xMeanEnd.setAlignment(Qt.AlignCenter)
        self.xMeanEnd.setReadOnly(True)

        self.horizontalLayout_41.addWidget(self.xMeanEnd)

        self.label_52 = QLabel(self.integralGroupBox_2)
        self.label_52.setObjectName(u"label_52")
        self.label_52.setFont(font1)

        self.horizontalLayout_41.addWidget(self.label_52)


        self.verticalLayout_12.addLayout(self.horizontalLayout_41)

        self.horizontalLayout_46 = QHBoxLayout()
        self.horizontalLayout_46.setObjectName(u"horizontalLayout_46")
        self.label_22 = QLabel(self.integralGroupBox_2)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setFont(font1)

        self.horizontalLayout_46.addWidget(self.label_22)

        self.meanResult = QLineEdit(self.integralGroupBox_2)
        self.meanResult.setObjectName(u"meanResult")
        self.meanResult.setFont(font1)
        self.meanResult.setFrame(False)
        self.meanResult.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.meanResult.setReadOnly(True)

        self.horizontalLayout_46.addWidget(self.meanResult)


        self.verticalLayout_12.addLayout(self.horizontalLayout_46)


        self.gridLayout_17.addLayout(self.verticalLayout_12, 0, 0, 1, 1)

        self.horizontalLayout_47 = QHBoxLayout()
        self.horizontalLayout_47.setObjectName(u"horizontalLayout_47")
        self.meanSelectInterval = QPushButton(self.integralGroupBox_2)
        self.meanSelectInterval.setObjectName(u"meanSelectInterval")

        self.horizontalLayout_47.addWidget(self.meanSelectInterval)

        self.meanCalculateAll = QPushButton(self.integralGroupBox_2)
        self.meanCalculateAll.setObjectName(u"meanCalculateAll")

        self.horizontalLayout_47.addWidget(self.meanCalculateAll)


        self.gridLayout_17.addLayout(self.horizontalLayout_47, 2, 0, 1, 1)

        self.verticalSpacer_8 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_17.addItem(self.verticalSpacer_8, 1, 0, 1, 1)


        self.gridLayout_19.addWidget(self.integralGroupBox_2, 0, 1, 1, 1)

        self.groupBox_13 = QGroupBox(self.tab_3)
        self.groupBox_13.setObjectName(u"groupBox_13")
        self.gridLayout_24 = QGridLayout(self.groupBox_13)
        self.gridLayout_24.setObjectName(u"gridLayout_24")
        self.horizontalLayout_48 = QHBoxLayout()
        self.horizontalLayout_48.setObjectName(u"horizontalLayout_48")
        self.label_54 = QLabel(self.groupBox_13)
        self.label_54.setObjectName(u"label_54")
        self.label_54.setFont(font1)

        self.horizontalLayout_48.addWidget(self.label_54)

        self.label_55 = QLabel(self.groupBox_13)
        self.label_55.setObjectName(u"label_55")
        self.label_55.setFont(font1)

        self.horizontalLayout_48.addWidget(self.label_55)

        self.xLengthBegin = QLineEdit(self.groupBox_13)
        self.xLengthBegin.setObjectName(u"xLengthBegin")
        sizePolicy4.setHeightForWidth(self.xLengthBegin.sizePolicy().hasHeightForWidth())
        self.xLengthBegin.setSizePolicy(sizePolicy4)
        self.xLengthBegin.setFont(font1)
        self.xLengthBegin.setFrame(False)
        self.xLengthBegin.setAlignment(Qt.AlignCenter)
        self.xLengthBegin.setReadOnly(True)

        self.horizontalLayout_48.addWidget(self.xLengthBegin)

        self.label_56 = QLabel(self.groupBox_13)
        self.label_56.setObjectName(u"label_56")
        self.label_56.setFont(font1)

        self.horizontalLayout_48.addWidget(self.label_56)

        self.xLengthEnd = QLineEdit(self.groupBox_13)
        self.xLengthEnd.setObjectName(u"xLengthEnd")
        sizePolicy4.setHeightForWidth(self.xLengthEnd.sizePolicy().hasHeightForWidth())
        self.xLengthEnd.setSizePolicy(sizePolicy4)
        self.xLengthEnd.setFrame(False)
        self.xLengthEnd.setAlignment(Qt.AlignCenter)
        self.xLengthEnd.setReadOnly(True)

        self.horizontalLayout_48.addWidget(self.xLengthEnd)

        self.label_57 = QLabel(self.groupBox_13)
        self.label_57.setObjectName(u"label_57")

        self.horizontalLayout_48.addWidget(self.label_57)


        self.gridLayout_24.addLayout(self.horizontalLayout_48, 0, 0, 1, 1)

        self.horizontalLayout_49 = QHBoxLayout()
        self.horizontalLayout_49.setObjectName(u"horizontalLayout_49")
        self.label_58 = QLabel(self.groupBox_13)
        self.label_58.setObjectName(u"label_58")
        font4 = QFont()
        font4.setPointSize(10)
        font4.setBold(False)
        self.label_58.setFont(font4)

        self.horizontalLayout_49.addWidget(self.label_58)

        self.label_59 = QLabel(self.groupBox_13)
        self.label_59.setObjectName(u"label_59")
        self.label_59.setFont(font1)

        self.horizontalLayout_49.addWidget(self.label_59)

        self.lengthResult = QLineEdit(self.groupBox_13)
        self.lengthResult.setObjectName(u"lengthResult")
        self.lengthResult.setFont(font1)
        self.lengthResult.setFrame(False)
        self.lengthResult.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.lengthResult.setReadOnly(True)

        self.horizontalLayout_49.addWidget(self.lengthResult)


        self.gridLayout_24.addLayout(self.horizontalLayout_49, 1, 0, 1, 1)

        self.horizontalLayout_50 = QHBoxLayout()
        self.horizontalLayout_50.setObjectName(u"horizontalLayout_50")
        self.curveLengthInterval = QPushButton(self.groupBox_13)
        self.curveLengthInterval.setObjectName(u"curveLengthInterval")

        self.horizontalLayout_50.addWidget(self.curveLengthInterval)

        self.curveLengthAll = QPushButton(self.groupBox_13)
        self.curveLengthAll.setObjectName(u"curveLengthAll")

        self.horizontalLayout_50.addWidget(self.curveLengthAll)


        self.gridLayout_24.addLayout(self.horizontalLayout_50, 2, 0, 1, 1)


        self.gridLayout_19.addWidget(self.groupBox_13, 1, 0, 1, 1)

        self.integralGroupBox = QGroupBox(self.tab_3)
        self.integralGroupBox.setObjectName(u"integralGroupBox")
        self.integralGroupBox.setLayoutDirection(Qt.LeftToRight)
        self.integralGroupBox.setFlat(False)
        self.integralGroupBox.setCheckable(False)
        self.gridLayout_14 = QGridLayout(self.integralGroupBox)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.horizontalLayout_29 = QHBoxLayout()
        self.horizontalLayout_29.setObjectName(u"horizontalLayout_29")
        self.integralSelectInterval = QPushButton(self.integralGroupBox)
        self.integralSelectInterval.setObjectName(u"integralSelectInterval")

        self.horizontalLayout_29.addWidget(self.integralSelectInterval)

        self.integrateAll = QPushButton(self.integralGroupBox)
        self.integrateAll.setObjectName(u"integrateAll")

        self.horizontalLayout_29.addWidget(self.integrateAll)


        self.gridLayout_14.addLayout(self.horizontalLayout_29, 3, 0, 1, 1)

        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.horizontalLayout_30 = QHBoxLayout()
        self.horizontalLayout_30.setObjectName(u"horizontalLayout_30")
        self.label_30 = QLabel(self.integralGroupBox)
        self.label_30.setObjectName(u"label_30")
        self.label_30.setFont(font1)

        self.horizontalLayout_30.addWidget(self.label_30)

        self.label_31 = QLabel(self.integralGroupBox)
        self.label_31.setObjectName(u"label_31")
        self.label_31.setFont(font1)

        self.horizontalLayout_30.addWidget(self.label_31)

        self.xIntegrBegin = QLineEdit(self.integralGroupBox)
        self.xIntegrBegin.setObjectName(u"xIntegrBegin")
        sizePolicy4.setHeightForWidth(self.xIntegrBegin.sizePolicy().hasHeightForWidth())
        self.xIntegrBegin.setSizePolicy(sizePolicy4)
        self.xIntegrBegin.setFont(font1)
        self.xIntegrBegin.setFrame(False)
        self.xIntegrBegin.setAlignment(Qt.AlignCenter)
        self.xIntegrBegin.setReadOnly(True)

        self.horizontalLayout_30.addWidget(self.xIntegrBegin)

        self.label_32 = QLabel(self.integralGroupBox)
        self.label_32.setObjectName(u"label_32")
        self.label_32.setFont(font1)

        self.horizontalLayout_30.addWidget(self.label_32)

        self.xIntegrEnd = QLineEdit(self.integralGroupBox)
        self.xIntegrEnd.setObjectName(u"xIntegrEnd")
        sizePolicy4.setHeightForWidth(self.xIntegrEnd.sizePolicy().hasHeightForWidth())
        self.xIntegrEnd.setSizePolicy(sizePolicy4)
        self.xIntegrEnd.setFrame(False)
        self.xIntegrEnd.setAlignment(Qt.AlignCenter)
        self.xIntegrEnd.setReadOnly(True)

        self.horizontalLayout_30.addWidget(self.xIntegrEnd)

        self.label_33 = QLabel(self.integralGroupBox)
        self.label_33.setObjectName(u"label_33")

        self.horizontalLayout_30.addWidget(self.label_33)


        self.verticalLayout_7.addLayout(self.horizontalLayout_30)

        self.horizontalLayout_31 = QHBoxLayout()
        self.horizontalLayout_31.setObjectName(u"horizontalLayout_31")
        self.label_34 = QLabel(self.integralGroupBox)
        self.label_34.setObjectName(u"label_34")
        sizePolicy2.setHeightForWidth(self.label_34.sizePolicy().hasHeightForWidth())
        self.label_34.setSizePolicy(sizePolicy2)
        font5 = QFont()
        font5.setPointSize(16)
        font5.setBold(False)
        self.label_34.setFont(font5)

        self.horizontalLayout_31.addWidget(self.label_34)

        self.label_35 = QLabel(self.integralGroupBox)
        self.label_35.setObjectName(u"label_35")
        self.label_35.setFont(font1)

        self.horizontalLayout_31.addWidget(self.label_35)

        self.integralResult = QLineEdit(self.integralGroupBox)
        self.integralResult.setObjectName(u"integralResult")
        sizePolicy4.setHeightForWidth(self.integralResult.sizePolicy().hasHeightForWidth())
        self.integralResult.setSizePolicy(sizePolicy4)
        self.integralResult.setFont(font1)
        self.integralResult.setFrame(False)
        self.integralResult.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.integralResult.setReadOnly(True)

        self.horizontalLayout_31.addWidget(self.integralResult)


        self.verticalLayout_7.addLayout(self.horizontalLayout_31)


        self.gridLayout_14.addLayout(self.verticalLayout_7, 0, 0, 1, 1)

        self.verticalSpacer_13 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_14.addItem(self.verticalSpacer_13, 1, 0, 1, 1)

        self.horizontalLayout_28 = QHBoxLayout()
        self.horizontalLayout_28.setObjectName(u"horizontalLayout_28")
        self.integralPlot = QCheckBox(self.integralGroupBox)
        self.integralPlot.setObjectName(u"integralPlot")
        self.integralPlot.setChecked(False)

        self.horizontalLayout_28.addWidget(self.integralPlot)

        self.integralPlotNewWindow = QCheckBox(self.integralGroupBox)
        self.integralPlotNewWindow.setObjectName(u"integralPlotNewWindow")
        self.integralPlotNewWindow.setEnabled(False)
        self.integralPlotNewWindow.setLayoutDirection(Qt.RightToLeft)
        self.integralPlotNewWindow.setChecked(True)

        self.horizontalLayout_28.addWidget(self.integralPlotNewWindow)


        self.gridLayout_14.addLayout(self.horizontalLayout_28, 2, 0, 1, 1)


        self.gridLayout_19.addWidget(self.integralGroupBox, 0, 0, 1, 1)

        self.verticalSpacer_14 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_19.addItem(self.verticalSpacer_14, 2, 1, 1, 1)

        self.tabWidget_2.addTab(self.tab_3, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.gridLayout_20 = QGridLayout(self.tab_4)
        self.gridLayout_20.setObjectName(u"gridLayout_20")
        self.groupBox_12 = QGroupBox(self.tab_4)
        self.groupBox_12.setObjectName(u"groupBox_12")
        self.gridLayout_6 = QGridLayout(self.groupBox_12)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.horizontalLayout_40 = QHBoxLayout()
        self.horizontalLayout_40.setObjectName(u"horizontalLayout_40")
        self.label_63 = QLabel(self.groupBox_12)
        self.label_63.setObjectName(u"label_63")

        self.horizontalLayout_40.addWidget(self.label_63)

        self.fftMaximums = QLineEdit(self.groupBox_12)
        self.fftMaximums.setObjectName(u"fftMaximums")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.fftMaximums.sizePolicy().hasHeightForWidth())
        self.fftMaximums.setSizePolicy(sizePolicy5)
        self.fftMaximums.setFrame(False)
        self.fftMaximums.setReadOnly(True)

        self.horizontalLayout_40.addWidget(self.fftMaximums)


        self.gridLayout_6.addLayout(self.horizontalLayout_40, 1, 0, 1, 1)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.deleteConstantCheckbox = QCheckBox(self.groupBox_12)
        self.deleteConstantCheckbox.setObjectName(u"deleteConstantCheckbox")
        self.deleteConstantCheckbox.setLayoutDirection(Qt.LeftToRight)

        self.verticalLayout_2.addWidget(self.deleteConstantCheckbox)

        self.horizontalLayout_39 = QHBoxLayout()
        self.horizontalLayout_39.setObjectName(u"horizontalLayout_39")
        self.label_40 = QLabel(self.groupBox_12)
        self.label_40.setObjectName(u"label_40")
        self.label_40.setEnabled(False)
        self.label_40.setLayoutDirection(Qt.LeftToRight)

        self.horizontalLayout_39.addWidget(self.label_40)

        self.deleteConstantPolynomOrder = QSpinBox(self.groupBox_12)
        self.deleteConstantPolynomOrder.setObjectName(u"deleteConstantPolynomOrder")
        self.deleteConstantPolynomOrder.setEnabled(False)
        self.deleteConstantPolynomOrder.setLayoutDirection(Qt.LeftToRight)
        self.deleteConstantPolynomOrder.setMinimum(1)

        self.horizontalLayout_39.addWidget(self.deleteConstantPolynomOrder)


        self.verticalLayout_2.addLayout(self.horizontalLayout_39)


        self.gridLayout_6.addLayout(self.verticalLayout_2, 0, 0, 1, 1)

        self.horizontalLayout_43 = QHBoxLayout()
        self.horizontalLayout_43.setObjectName(u"horizontalLayout_43")
        self.fourierIntervalButton = QPushButton(self.groupBox_12)
        self.fourierIntervalButton.setObjectName(u"fourierIntervalButton")

        self.horizontalLayout_43.addWidget(self.fourierIntervalButton)

        self.fourierAllButton = QPushButton(self.groupBox_12)
        self.fourierAllButton.setObjectName(u"fourierAllButton")

        self.horizontalLayout_43.addWidget(self.fourierAllButton)

        self.periodicalFft = QPushButton(self.groupBox_12)
        self.periodicalFft.setObjectName(u"periodicalFft")

        self.horizontalLayout_43.addWidget(self.periodicalFft)


        self.gridLayout_6.addLayout(self.horizontalLayout_43, 3, 0, 1, 1)

        self.verticalSpacer_7 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_6.addItem(self.verticalSpacer_7, 2, 0, 1, 1)


        self.gridLayout_20.addWidget(self.groupBox_12, 0, 0, 1, 1)

        self.verticalSpacer_15 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_20.addItem(self.verticalSpacer_15, 1, 0, 1, 1)

        self.tabWidget_2.addTab(self.tab_4, "")

        self.verticalLayout_10.addWidget(self.tabWidget_2)


        self.gridLayout_23.addLayout(self.verticalLayout_10, 0, 0, 1, 1)

        self.tabWidget.addTab(self.plotTab, "")

        self.gridLayout.addWidget(self.tabWidget, 0, 1, 1, 1)

        CornplotGui.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(CornplotGui)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 795, 21))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        self.menu_2 = QMenu(self.menubar)
        self.menu_2.setObjectName(u"menu_2")
        self.menu_3 = QMenu(self.menubar)
        self.menu_3.setObjectName(u"menu_3")
        self.menu_4 = QMenu(self.menubar)
        self.menu_4.setObjectName(u"menu_4")
        self.menu_5 = QMenu(self.menu_4)
        self.menu_5.setObjectName(u"menu_5")
        CornplotGui.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(CornplotGui)
        self.statusbar.setObjectName(u"statusbar")
        CornplotGui.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_4.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menu.addAction(self.openGraphAction)
        self.menu.addAction(self.saveGraphAction)
        self.menu.addSeparator()
        self.menu.addAction(self.exitAction)
        self.menu_2.addAction(self.aboutProgramAction)
        self.menu_3.addAction(self.importFromCSV)
        self.menu_3.addAction(self.exportToCSV)
        self.menu_3.addAction(self.newGraphEquationAction)
        self.menu_3.addSeparator()
        self.menu_3.addAction(self.deletePlotAction)
        self.menu_4.addAction(self.backgroundColorAction)
        self.menu_4.addAction(self.fontAction)
        self.menu_4.addSeparator()
        self.menu_4.addAction(self.drawOriginAction)
        self.menu_4.addAction(self.drawTicksAction)
        self.menu_4.addAction(self.drawLabelsAction)
        self.menu_4.addSeparator()
        self.menu_4.addAction(self.majorGridAction)
        self.menu_4.addAction(self.minorGridAction)
        self.menu_4.addSeparator()
        self.menu_4.addAction(self.menu_5.menuAction())
        self.menu_5.addAction(self.digitsAuto)
        self.menu_5.addAction(self.action0)
        self.menu_5.addAction(self.action1)
        self.menu_5.addAction(self.action2)
        self.menu_5.addAction(self.action3)
        self.menu_5.addAction(self.action4)
        self.menu_5.addAction(self.action5)
        self.menu_5.addAction(self.action6)

        self.retranslateUi(CornplotGui)
        self.yAuto.toggled.connect(self.yStep.setDisabled)
        self.yAuto.toggled.connect(self.yMin.setDisabled)
        self.yAuto.toggled.connect(self.yMax.setDisabled)
        self.xAuto.toggled.connect(self.xStep.setDisabled)
        self.xAuto.toggled.connect(self.xMax.setDisabled)
        self.xAuto.toggled.connect(self.xMin.setDisabled)
        self.drawMarkers.toggled.connect(self.drawLine.setEnabled)
        self.polyApprox.toggled.connect(self.polyPower.setEnabled)
        self.polyApprox.toggled.connect(self.label_17.setEnabled)
        self.meanApprox.toggled.connect(self.label_18.setEnabled)
        self.meanApprox.toggled.connect(self.meanPeriods.setEnabled)
        self.majorTicksCheckX.toggled.connect(self.majorTicksX.setEnabled)
        self.majorTicksCheckX.toggled.connect(self.majorTicksWidthX.setEnabled)
        self.minorTicksCheckX.toggled.connect(self.minorTicksX.setEnabled)
        self.minorTicksCheckX.toggled.connect(self.minorTicksWidthX.setEnabled)
        self.okButton.clicked.connect(CornplotGui.close)
        self.integralPlot.toggled.connect(self.integralPlotNewWindow.setEnabled)
        self.deleteConstantCheckbox.toggled.connect(self.deleteConstantPolynomOrder.setEnabled)
        self.deleteConstantCheckbox.toggled.connect(self.label_40.setEnabled)
        self.majorTicksCheckY.toggled.connect(self.majorTicksY.setEnabled)
        self.majorTicksCheckY.toggled.connect(self.majorTicksWidthY.setEnabled)
        self.minorTicksCheckY.toggled.connect(self.minorTicksY.setEnabled)
        self.minorTicksCheckY.toggled.connect(self.minorTicksWidthY.setEnabled)
        self.originCheckX.toggled.connect(self.originWidthX.setEnabled)
        self.originCheckX.toggled.connect(self.label_14.setEnabled)
        self.originCheckY.toggled.connect(self.label_62.setEnabled)
        self.originCheckY.toggled.connect(self.originWidthY.setEnabled)
        self.drawOriginAction.toggled.connect(self.originCheckX.setChecked)
        self.drawOriginAction.toggled.connect(self.originCheckY.setChecked)
        self.drawTicksAction.toggled.connect(self.xTicks.setChecked)
        self.drawTicksAction.toggled.connect(self.yTicks.setChecked)
        self.drawLabelsAction.toggled.connect(self.xLabelCheck.setChecked)
        self.drawLabelsAction.toggled.connect(self.yLabelCheck.setChecked)
        self.minorGridAction.toggled.connect(self.minorTicksCheckX.setChecked)
        self.minorGridAction.toggled.connect(self.minorTicksCheckY.setChecked)
        self.majorGridAction.toggled.connect(self.majorTicksCheckX.setChecked)
        self.majorGridAction.toggled.connect(self.majorTicksCheckY.setChecked)
        self.minorTicksCheckY.toggled.connect(self.minorTicksStepY.setEnabled)
        self.minorTicksCheckX.toggled.connect(self.minorTicksStepX.setEnabled)

        self.tabWidget.setCurrentIndex(1)
        self.tabWidget_2.setCurrentIndex(4)


        QMetaObject.connectSlotsByName(CornplotGui)
    # setupUi

    def retranslateUi(self, CornplotGui):
        CornplotGui.setWindowTitle(QCoreApplication.translate("CornplotGui", u"Cornplot - \u0434\u0435\u0439\u0441\u0442\u0432\u0438\u044f", None))
        self.newGraphEquationAction.setText(QCoreApplication.translate("CornplotGui", u"\u0412\u0432\u0435\u0441\u0442\u0438 \u0443\u0440\u0430\u0432\u043d\u0435\u043d\u0438\u0435", None))
#if QT_CONFIG(shortcut)
        self.newGraphEquationAction.setShortcut(QCoreApplication.translate("CornplotGui", u"Shift+E", None))
#endif // QT_CONFIG(shortcut)
        self.saveGraphAction.setText(QCoreApplication.translate("CornplotGui", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c", None))
#if QT_CONFIG(shortcut)
        self.saveGraphAction.setShortcut(QCoreApplication.translate("CornplotGui", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.openGraphAction.setText(QCoreApplication.translate("CornplotGui", u"\u041e\u0442\u043a\u0440\u044b\u0442\u044c", None))
#if QT_CONFIG(shortcut)
        self.openGraphAction.setShortcut(QCoreApplication.translate("CornplotGui", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.aboutProgramAction.setText(QCoreApplication.translate("CornplotGui", u"\u041e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0435", None))
        self.exitAction.setText(QCoreApplication.translate("CornplotGui", u"\u0412\u044b\u0445\u043e\u0434", None))
        self.exportToCSV.setText(QCoreApplication.translate("CornplotGui", u"\u042d\u043a\u0441\u043f\u043e\u0440\u0442 \u0432 CSV", None))
#if QT_CONFIG(shortcut)
        self.exportToCSV.setShortcut(QCoreApplication.translate("CornplotGui", u"Shift+S", None))
#endif // QT_CONFIG(shortcut)
        self.importFromCSV.setText(QCoreApplication.translate("CornplotGui", u"\u0418\u043c\u043f\u043e\u0440\u0442 \u0438\u0437 CSV", None))
#if QT_CONFIG(shortcut)
        self.importFromCSV.setShortcut(QCoreApplication.translate("CornplotGui", u"Shift+O", None))
#endif // QT_CONFIG(shortcut)
        self.deletePlotAction.setText(QCoreApplication.translate("CornplotGui", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c \u0442\u0435\u043a\u0443\u0449\u0438\u0439 \u0433\u0440\u0430\u0444\u0438\u043a", None))
#if QT_CONFIG(shortcut)
        self.deletePlotAction.setShortcut(QCoreApplication.translate("CornplotGui", u"Shift+Del", None))
#endif // QT_CONFIG(shortcut)
        self.backgroundColorAction.setText(QCoreApplication.translate("CornplotGui", u"\u0426\u0432\u0435\u0442 \u0444\u043e\u043d\u0430...", None))
        self.drawOriginAction.setText(QCoreApplication.translate("CornplotGui", u"\u0420\u0438\u0441\u043e\u0432\u0430\u0442\u044c \u043e\u0441\u0438", None))
        self.drawTicksAction.setText(QCoreApplication.translate("CornplotGui", u"\u041f\u043e\u0434\u043f\u0438\u0441\u0438 \u043e\u0441\u0435\u0439", None))
        self.drawLabelsAction.setText(QCoreApplication.translate("CornplotGui", u"\u041d\u0430\u0437\u0432\u0430\u0433\u0438\u044f \u043e\u0441\u0435\u0439", None))
        self.fontAction.setText(QCoreApplication.translate("CornplotGui", u"\u0428\u0440\u0438\u0444\u0442...", None))
        self.minorGridAction.setText(QCoreApplication.translate("CornplotGui", u"\u041f\u043e\u0431\u043e\u0447\u043d\u0430\u044f \u0441\u0435\u0442\u043a\u0430", None))
        self.gridSolidAction.setText(QCoreApplication.translate("CornplotGui", u"\u0421\u043f\u043b\u043e\u0448\u043d\u0430\u044f", None))
        self.dotGridAction.setText(QCoreApplication.translate("CornplotGui", u"\u041f\u0443\u043d\u043a\u0442\u0438\u0440\u043d\u0430\u044f", None))
        self.dashGridAction.setText(QCoreApplication.translate("CornplotGui", u"\u0428\u0442\u0440\u0438\u0445\u043e\u0432\u0430\u044f", None))
        self.majorGridAction.setText(QCoreApplication.translate("CornplotGui", u"\u041e\u0441\u043d\u043e\u0432\u043d\u0430\u044f \u0441\u0435\u0442\u043a\u0430", None))
        self.digitsAuto.setText(QCoreApplication.translate("CornplotGui", u"\u0410\u0432\u0442\u043e", None))
        self.action0.setText(QCoreApplication.translate("CornplotGui", u"0", None))
        self.action1.setText(QCoreApplication.translate("CornplotGui", u"1", None))
        self.action2.setText(QCoreApplication.translate("CornplotGui", u"2", None))
        self.action3.setText(QCoreApplication.translate("CornplotGui", u"3", None))
        self.action4.setText(QCoreApplication.translate("CornplotGui", u"4", None))
        self.action5.setText(QCoreApplication.translate("CornplotGui", u"5", None))
        self.action6.setText(QCoreApplication.translate("CornplotGui", u"6", None))
        self.okButton.setText(QCoreApplication.translate("CornplotGui", u"\u041e\u043a", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("CornplotGui", u"\u041e\u0441\u044c \u0425", None))
        self.xScaleSelect.setItemText(0, QCoreApplication.translate("CornplotGui", u"\u041b\u0438\u043d\u0435\u0439\u043d\u0430\u044f", None))
        self.xScaleSelect.setItemText(1, QCoreApplication.translate("CornplotGui", u"\u041b\u043e\u0433\u0430\u0440\u0438\u0444\u043c\u0438\u0447\u0435\u0441\u043a\u0430\u044f", None))

        self.label_4.setText(QCoreApplication.translate("CornplotGui", u"\u041c\u0430\u043a\u0441\u0438\u043c\u0443\u043c:", None))
        self.label_3.setText(QCoreApplication.translate("CornplotGui", u"\u041c\u0438\u043d\u0438\u043c\u0443\u043c:", None))
        self.label_2.setText(QCoreApplication.translate("CornplotGui", u"\u0428\u0430\u0433 \u0441\u0435\u0442\u043a\u0438:", None))
        self.label.setText(QCoreApplication.translate("CornplotGui", u"\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u043e\u0441\u0438:", None))
        self.xAuto.setText(QCoreApplication.translate("CornplotGui", u"\u0410\u0432\u0442\u043e\u043d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0430", None))
        self.xTicks.setText(QCoreApplication.translate("CornplotGui", u"\u0420\u0438\u0441\u043e\u0432\u0430\u0442\u044c \u043f\u043e\u0434\u043f\u0438\u0441\u0438", None))
        self.xLabelCheck.setText(QCoreApplication.translate("CornplotGui", u"\u0420\u0438\u0441\u043e\u0432\u0430\u0442\u044c \u043d\u0430\u0437\u0432\u0430\u043d\u0438\u0435", None))
        self.groupBox.setTitle(QCoreApplication.translate("CornplotGui", u"\u0417\u043d\u0430\u0447\u0435\u043d\u0438\u044f", None))
        self.xTypeNormal.setText(QCoreApplication.translate("CornplotGui", u"\u0427\u0438\u0441\u043b\u0430", None))
        self.xTypeTime.setText(QCoreApplication.translate("CornplotGui", u"\u041c\u0435\u0442\u043a\u0438 \u0432\u0440\u0435\u043c\u0435\u043d\u0438", None))
        self.gridGroup.setTitle(QCoreApplication.translate("CornplotGui", u"\u0421\u0435\u0442\u043a\u0430", None))
        self.label_10.setText("")
        self.label_11.setText(QCoreApplication.translate("CornplotGui", u"\u0421\u0442\u0438\u043b\u044c", None))
        self.label_12.setText(QCoreApplication.translate("CornplotGui", u"\u0422\u043e\u043b\u0449\u0438\u043d\u0430", None))
        self.label_13.setText(QCoreApplication.translate("CornplotGui", u"\u0414\u043e\u043b\u044f \u0448\u0430\u0433\u0430", None))
        self.majorTicksCheckX.setText(QCoreApplication.translate("CornplotGui", u"\u041e\u0441\u043d\u043e\u0432\u043d\u0430\u044f:", None))
        self.majorTicksX.setItemText(0, QCoreApplication.translate("CornplotGui", u"\u0421\u043f\u043b\u043e\u0448\u043d\u0430\u044f", None))
        self.majorTicksX.setItemText(1, QCoreApplication.translate("CornplotGui", u"\u041f\u0443\u043d\u043a\u0442\u0438\u0440\u043d\u0430\u044f", None))
        self.majorTicksX.setItemText(2, QCoreApplication.translate("CornplotGui", u"\u0428\u0442\u0440\u0438\u0445\u043e\u0432\u0430\u044f", None))

        self.label_9.setText("")
        self.minorTicksCheckX.setText(QCoreApplication.translate("CornplotGui", u"\u041f\u043e\u0431\u043e\u0447\u043d\u0430\u044f:", None))
        self.minorTicksX.setItemText(0, QCoreApplication.translate("CornplotGui", u"\u0421\u043f\u043b\u043e\u0448\u043d\u0430\u044f", None))
        self.minorTicksX.setItemText(1, QCoreApplication.translate("CornplotGui", u"\u041f\u0443\u043d\u043a\u0442\u0438\u0440\u043d\u0430\u044f", None))
        self.minorTicksX.setItemText(2, QCoreApplication.translate("CornplotGui", u"\u0428\u0442\u0440\u0438\u0445\u043e\u0432\u0430\u044f", None))

        self.originCheckX.setText(QCoreApplication.translate("CornplotGui", u"\u0420\u0438\u0441\u043e\u0432\u0430\u0442\u044c \u043e\u0441\u044c \u0425", None))
        self.label_14.setText(QCoreApplication.translate("CornplotGui", u"\u0422\u043e\u043b\u0449\u0438\u043d\u0430 \u043e\u0441\u0438:", None))
        self.label_65.setText(QCoreApplication.translate("CornplotGui", u"\u0414\u0435\u043b\u0438\u0442\u0435\u043b\u044c:", None))
        self.acceptXdivisor.setText(QCoreApplication.translate("CornplotGui", u"\u041f\u0440\u0438\u043c\u0435\u043d\u0438\u0442\u044c", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("CornplotGui", u"\u041e\u0441\u044c Y", None))
        self.yScaleSelect.setItemText(0, QCoreApplication.translate("CornplotGui", u"\u041b\u0438\u043d\u0435\u0439\u043d\u0430\u044f", None))
        self.yScaleSelect.setItemText(1, QCoreApplication.translate("CornplotGui", u"\u041b\u043e\u0433\u0430\u0440\u0438\u0444\u043c\u0438\u0447\u0435\u0441\u043a\u0430\u044f", None))

        self.label_8.setText(QCoreApplication.translate("CornplotGui", u"\u041c\u0430\u043a\u0441\u0438\u043c\u0443\u043c:", None))
        self.label_5.setText(QCoreApplication.translate("CornplotGui", u"\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u043e\u0441\u0438:", None))
        self.label_7.setText(QCoreApplication.translate("CornplotGui", u"\u041c\u0438\u043d\u0438\u043c\u0443\u043c:", None))
        self.yAuto.setText(QCoreApplication.translate("CornplotGui", u"\u0410\u0432\u0442\u043e\u043d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0430", None))
        self.yTicks.setText(QCoreApplication.translate("CornplotGui", u"\u0420\u0438\u0441\u043e\u0432\u0430\u0442\u044c \u043f\u043e\u0434\u043f\u0438\u0441\u0438", None))
        self.yLabelCheck.setText(QCoreApplication.translate("CornplotGui", u"\u0420\u0438\u0441\u043e\u0432\u0430\u0442\u044c \u043d\u0430\u0437\u0432\u0430\u043d\u0438\u0435", None))
        self.label_6.setText(QCoreApplication.translate("CornplotGui", u"\u0428\u0430\u0433 \u0441\u0435\u0442\u043a\u0438:", None))
        self.gridGroup_2.setTitle(QCoreApplication.translate("CornplotGui", u"\u0421\u0435\u0442\u043a\u0430", None))
        self.label_27.setText("")
        self.label_28.setText(QCoreApplication.translate("CornplotGui", u"\u0421\u0442\u0438\u043b\u044c", None))
        self.label_29.setText(QCoreApplication.translate("CornplotGui", u"\u0422\u043e\u043b\u0449\u0438\u043d\u0430", None))
        self.label_60.setText(QCoreApplication.translate("CornplotGui", u"\u0414\u043e\u043b\u044f \u0448\u0430\u0433\u0430", None))
        self.majorTicksCheckY.setText(QCoreApplication.translate("CornplotGui", u"\u041e\u0441\u043d\u043e\u0432\u043d\u0430\u044f:", None))
        self.majorTicksY.setItemText(0, QCoreApplication.translate("CornplotGui", u"\u0421\u043f\u043b\u043e\u0448\u043d\u0430\u044f", None))
        self.majorTicksY.setItemText(1, QCoreApplication.translate("CornplotGui", u"\u041f\u0443\u043d\u043a\u0442\u0438\u0440\u043d\u0430\u044f", None))
        self.majorTicksY.setItemText(2, QCoreApplication.translate("CornplotGui", u"\u0428\u0442\u0440\u0438\u0445\u043e\u0432\u0430\u044f", None))

        self.label_61.setText("")
        self.minorTicksCheckY.setText(QCoreApplication.translate("CornplotGui", u"\u041f\u043e\u0431\u043e\u0447\u043d\u0430\u044f:", None))
        self.minorTicksY.setItemText(0, QCoreApplication.translate("CornplotGui", u"\u0421\u043f\u043b\u043e\u0448\u043d\u0430\u044f", None))
        self.minorTicksY.setItemText(1, QCoreApplication.translate("CornplotGui", u"\u041f\u0443\u043d\u043a\u0442\u0438\u0440\u043d\u0430\u044f", None))
        self.minorTicksY.setItemText(2, QCoreApplication.translate("CornplotGui", u"\u0428\u0442\u0440\u0438\u0445\u043e\u0432\u0430\u044f", None))

        self.originCheckY.setText(QCoreApplication.translate("CornplotGui", u"\u0420\u0438\u0441\u043e\u0432\u0430\u0442\u044c \u043e\u0441\u044c Y", None))
        self.label_62.setText(QCoreApplication.translate("CornplotGui", u"\u0422\u043e\u043b\u0449\u0438\u043d\u0430 \u043e\u0441\u0438:", None))
        self.label_66.setText(QCoreApplication.translate("CornplotGui", u"\u0414\u0435\u043b\u0438\u0442\u0435\u043b\u044c:", None))
        self.acceptYdivisor.setText(QCoreApplication.translate("CornplotGui", u"\u041f\u0440\u0438\u043c\u0435\u043d\u0438\u0442\u044c", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.axlesTab), QCoreApplication.translate("CornplotGui", u"\u041e\u0441\u0438 \u0438 \u0441\u0435\u0442\u043a\u0430", None))
        self.label_36.setText(QCoreApplication.translate("CornplotGui", u"\u0412\u044b\u0431\u0440\u0430\u043d\u043d\u044b\u0439 \u0433\u0440\u0430\u0444\u0438\u043a:", None))
        self.pltImage.setText("")
        self.groupBox_5.setTitle(QCoreApplication.translate("CornplotGui", u"\u041b\u0438\u043d\u0438\u044f \u0438 \u043c\u0430\u0440\u043a\u0435\u0440\u044b", None))
        self.accurateDrawingCheckbox.setText(QCoreApplication.translate("CornplotGui", u"\u0422\u043e\u0447\u043d\u043e\u0435 \u043e\u0442\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435", None))
        self.drawLine.setText(QCoreApplication.translate("CornplotGui", u"\u041b\u0438\u043d\u0438\u044f", None))
        self.plotLineStyle.setItemText(0, QCoreApplication.translate("CornplotGui", u"\u0421\u043f\u043b\u043e\u0448\u043d\u0430\u044f", None))
        self.plotLineStyle.setItemText(1, QCoreApplication.translate("CornplotGui", u"\u0428\u0442\u0440\u0438\u0445\u043e\u0432\u0430\u044f", None))
        self.plotLineStyle.setItemText(2, QCoreApplication.translate("CornplotGui", u"\u0428\u0442\u0440\u0438\u0445\u043f\u0443\u043d\u043a\u0442\u0438\u0440\u043d\u0430\u044f", None))
        self.plotLineStyle.setItemText(3, QCoreApplication.translate("CornplotGui", u"\u0428\u0442\u0440\u0438\u0445\u043f\u0443\u043d\u043a\u0442\u0438\u0440\u043d\u0430\u044f \u0441 \u0434\u0432\u0443\u043c\u044f \u0442\u043e\u0447\u043a\u0430\u043c\u0438", None))
        self.plotLineStyle.setItemText(4, QCoreApplication.translate("CornplotGui", u"\u041f\u0443\u043d\u043a\u0442\u0438\u0440\u043d\u0430\u044f", None))

        self.label_16.setText(QCoreApplication.translate("CornplotGui", u"\u0422\u043e\u043b\u0449\u0438\u043d\u0430:", None))
        self.drawMarkers.setText(QCoreApplication.translate("CornplotGui", u"\u041c\u0430\u0440\u043a\u0435\u0440\u044b", None))
        self.markerStyles.setItemText(0, QCoreApplication.translate("CornplotGui", u"\u041a\u0440\u0443\u0433\u043b\u044b\u0435", None))
        self.markerStyles.setItemText(1, QCoreApplication.translate("CornplotGui", u"\u041a\u0432\u0430\u0434\u0440\u0430\u0442\u043d\u044b\u0435", None))

        self.label_15.setText(QCoreApplication.translate("CornplotGui", u"\u0422\u043e\u043b\u0449\u0438\u043d\u0430:", None))
        self.colorButton.setText(QCoreApplication.translate("CornplotGui", u"\u0412\u044b\u0431\u0440\u0430\u0442\u044c \u0446\u0432\u0435\u0442...", None))
        self.label_41.setText(QCoreApplication.translate("CornplotGui", u"X \u2208 ", None))
        self.label_42.setText(QCoreApplication.translate("CornplotGui", u"[", None))
        self.pltXmin.setText(QCoreApplication.translate("CornplotGui", u"?", None))
        self.label_43.setText(QCoreApplication.translate("CornplotGui", u";", None))
        self.pltXmax.setText(QCoreApplication.translate("CornplotGui", u"?", None))
        self.label_44.setText(QCoreApplication.translate("CornplotGui", u"]", None))
        self.label_45.setText(QCoreApplication.translate("CornplotGui", u"Y \u2208 ", None))
        self.label_46.setText(QCoreApplication.translate("CornplotGui", u"[", None))
        self.pltYmin.setText(QCoreApplication.translate("CornplotGui", u"?", None))
        self.label_47.setText(QCoreApplication.translate("CornplotGui", u";", None))
        self.pltYmax.setText(QCoreApplication.translate("CornplotGui", u"?", None))
        self.label_48.setText(QCoreApplication.translate("CornplotGui", u"]", None))
        self.label_23.setText(QCoreApplication.translate("CornplotGui", u"\u0427\u0438\u0441\u043b\u043e \u0442\u043e\u0447\u0435\u043a:", None))
        self.deletePlotButton.setText(QCoreApplication.translate("CornplotGui", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c \u0433\u0440\u0430\u0444\u0438\u043a", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab), QCoreApplication.translate("CornplotGui", u"\u041e\u0431\u0449\u0435\u0435", None))
        self.approxGroup.setTitle(QCoreApplication.translate("CornplotGui", u"\u0410\u043f\u043f\u0440\u043e\u043a\u0441\u0438\u043c\u0430\u0446\u0438\u044f", None))
        self.approxIntervalButton.setText(QCoreApplication.translate("CornplotGui", u"\u0412\u044b\u0431\u0440\u0430\u0442\u044c \u0438\u043d\u0442\u0435\u0440\u0432\u0430\u043b...", None))
        self.approxButton.setText(QCoreApplication.translate("CornplotGui", u"\u041d\u0430 \u0432\u0441\u0451\u043c \u0438\u043d\u0442\u0435\u0440\u0432\u0430\u043b\u0435", None))
        self.powerApprox.setText(QCoreApplication.translate("CornplotGui", u"\u0421\u0442\u0435\u043f\u0435\u043d\u043d\u0430\u044f", None))
        self.logApprox.setText(QCoreApplication.translate("CornplotGui", u"\u041b\u043e\u0433\u0430\u0440\u0438\u0444\u043c\u0438\u0447\u0435\u0441\u043a\u0430\u044f", None))
        self.linearApprox.setText(QCoreApplication.translate("CornplotGui", u"\u041b\u0438\u043d\u0435\u0439\u043d\u0430\u044f", None))
        self.expApprox.setText(QCoreApplication.translate("CornplotGui", u"\u042d\u043a\u0441\u043f\u043e\u043d\u0435\u043d\u0446\u0438\u0430\u043b\u044c\u043d\u0430\u044f", None))
        self.meanApprox.setText(QCoreApplication.translate("CornplotGui", u"\u0421\u043a\u043e\u043b\u044c\u0437\u044f\u0449\u0435\u0435 \u0441\u0440\u0435\u0434\u043d\u0435\u0435", None))
        self.label_18.setText(QCoreApplication.translate("CornplotGui", u"\u041f\u0435\u0440\u0438\u043e\u0434\u044b:", None))
        self.polyApprox.setText(QCoreApplication.translate("CornplotGui", u"\u041f\u043e\u043b\u0438\u043d\u043e\u043c\u0438\u0430\u043b\u044c\u043d\u0430\u044f", None))
        self.label_17.setText(QCoreApplication.translate("CornplotGui", u"\u0421\u0442\u0435\u043f\u0435\u043d\u044c:", None))
        self.equationButton.setText(QCoreApplication.translate("CornplotGui", u"\u041f\u043e\u043a\u0430\u0437\u0430\u0442\u044c \u0443\u0440\u0430\u0432\u043d\u0435\u043d\u0438\u0435", None))
        self.filterGroup.setTitle(QCoreApplication.translate("CornplotGui", u"\u0424\u0438\u043b\u044c\u0442\u0440\u0430\u0446\u0438\u044f", None))
        self.doFiltering.setText(QCoreApplication.translate("CornplotGui", u"\u0412\u044b\u043f\u043e\u043b\u043d\u0438\u0442\u044c", None))
        self.movingAverageFilterBox.setText(QCoreApplication.translate("CornplotGui", u"\u0421\u043a\u043e\u043b\u044c\u0437\u044f\u0449\u0435\u0435 \u0441\u0440\u0435\u0434\u043d\u0435\u0435", None))
        self.label_38.setText(QCoreApplication.translate("CornplotGui", u"\u041f\u043e\u0440\u044f\u0434\u043e\u043a:", None))
        self.medianFilterBox.setText(QCoreApplication.translate("CornplotGui", u"\u041c\u0435\u0434\u0438\u0430\u043d\u043d\u0430\u044f", None))
        self.label_39.setText(QCoreApplication.translate("CornplotGui", u"\u041f\u043e\u0440\u044f\u0434\u043e\u043a:", None))
        self.expFilterBox.setText(QCoreApplication.translate("CornplotGui", u"\u042d\u043a\u0441\u043f\u043e\u043d\u0435\u043d\u0446\u0438\u0430\u043b\u044c\u043d\u0430\u044f", None))
        self.label_37.setText(QCoreApplication.translate("CornplotGui", u"\u041a\u043e\u044d\u0444\u0444.:", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_5), QCoreApplication.translate("CornplotGui", u"\u0424\u0438\u043b\u044c\u0442\u0440\u0430\u0446\u0438\u044f \u0438 \u0430\u043f\u043f\u0440\u043e\u043a\u0441\u0438\u043c\u0430\u0446\u0438\u044f", None))
        self.groupBox_7.setTitle(QCoreApplication.translate("CornplotGui", u"\u0414\u0438\u0444\u0444\u0435\u0440\u0435\u043d\u0446\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435", None))
        self.groupBox_8.setTitle(QCoreApplication.translate("CornplotGui", u"\u0412\u044b\u0431\u0440\u0430\u043d\u043d\u0430\u044f \u0442\u043e\u0447\u043a\u0430", None))
        self.label_20.setText(QCoreApplication.translate("CornplotGui", u"y = ", None))
        self.yDiff.setText(QCoreApplication.translate("CornplotGui", u"?", None))
        self.label_19.setText(QCoreApplication.translate("CornplotGui", u"x = ", None))
        self.xDiff.setText(QCoreApplication.translate("CornplotGui", u"?", None))
        self.groupBox_9.setTitle(QCoreApplication.translate("CornplotGui", u"\u0420\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442", None))
        self.label_21.setText(QCoreApplication.translate("CornplotGui", u"y' = ", None))
        self.diffResult.setText(QCoreApplication.translate("CornplotGui", u"?", None))
        self.diffPointSelect.setText(QCoreApplication.translate("CornplotGui", u"\u0412\u044b\u0431\u0440\u0430\u0442\u044c \u0442\u043e\u0447\u043a\u0443...", None))
        self.diffSelectTwoPoints.setText(QCoreApplication.translate("CornplotGui", u"\u0412\u044b\u0431\u0440\u0430\u0442\u044c \u0438\u043d\u0442\u0435\u0440\u0432\u0430\u043b...", None))
        self.diffSelectAll.setText(QCoreApplication.translate("CornplotGui", u"\u041d\u0430 \u0432\u0441\u0451\u043c \u0438\u043d\u0442\u0435\u0440\u0432\u0430\u043b\u0435", None))
        self.groupBox_10.setTitle(QCoreApplication.translate("CornplotGui", u"\u0412\u044b\u0431\u0440\u0430\u043d\u044b\u0439 \u0438\u043d\u0442\u0435\u0440\u0432\u0430\u043b", None))
        self.label_53.setText(QCoreApplication.translate("CornplotGui", u"X \u2208 ", None))
        self.label_24.setText(QCoreApplication.translate("CornplotGui", u"[", None))
        self.xDiffBegin.setText(QCoreApplication.translate("CornplotGui", u"?", None))
        self.label_26.setText(QCoreApplication.translate("CornplotGui", u";", None))
        self.xDiffEnd.setText(QCoreApplication.translate("CornplotGui", u"?", None))
        self.label_25.setText(QCoreApplication.translate("CornplotGui", u"]", None))
        self.diffNewWindow.setText(QCoreApplication.translate("CornplotGui", u"\u0413\u0440\u0430\u0444\u0438\u043a \u0432 \u043d\u043e\u0432\u043e\u043c \u043e\u043a\u043d\u0435", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_2), QCoreApplication.translate("CornplotGui", u"\u041f\u0440\u043e\u0438\u0437\u0432\u043e\u0434\u043d\u0430\u044f", None))
        self.groupBox_14.setTitle("")
        self.integralGroupBox_2.setTitle(QCoreApplication.translate("CornplotGui", u"\u0421\u0440\u0435\u0434\u043d\u0435\u0435 \u0437\u043d\u0430\u0447\u0435\u043d\u0438\u0435", None))
        self.label_49.setText(QCoreApplication.translate("CornplotGui", u"X \u2208 ", None))
        self.label_50.setText(QCoreApplication.translate("CornplotGui", u"[", None))
        self.xMeanBegin.setText(QCoreApplication.translate("CornplotGui", u"?", None))
        self.label_51.setText(QCoreApplication.translate("CornplotGui", u";", None))
        self.xMeanEnd.setText(QCoreApplication.translate("CornplotGui", u"?", None))
        self.label_52.setText(QCoreApplication.translate("CornplotGui", u"]", None))
        self.label_22.setText(QCoreApplication.translate("CornplotGui", u"\u0421\u0440\u0435\u0434\u043d\u0435\u0435 = ", None))
        self.meanResult.setText(QCoreApplication.translate("CornplotGui", u"?", None))
        self.meanSelectInterval.setText(QCoreApplication.translate("CornplotGui", u"\u0412\u044b\u0431\u0440\u0430\u0442\u044c \u0438\u043d\u0442\u0435\u0440\u0432\u0430\u043b...", None))
        self.meanCalculateAll.setText(QCoreApplication.translate("CornplotGui", u"\u041d\u0430 \u0432\u0441\u0451\u043c \u0438\u043d\u0442\u0435\u0440\u0432\u0430\u043b\u0435", None))
        self.groupBox_13.setTitle(QCoreApplication.translate("CornplotGui", u"\u0414\u043b\u0438\u043d\u0430 \u0434\u0443\u0433\u0438 \u043a\u0440\u0438\u0432\u043e\u0439", None))
        self.label_54.setText(QCoreApplication.translate("CornplotGui", u"X \u2208 ", None))
        self.label_55.setText(QCoreApplication.translate("CornplotGui", u"[", None))
        self.xLengthBegin.setText(QCoreApplication.translate("CornplotGui", u"?", None))
        self.label_56.setText(QCoreApplication.translate("CornplotGui", u";", None))
        self.xLengthEnd.setText(QCoreApplication.translate("CornplotGui", u"?", None))
        self.label_57.setText(QCoreApplication.translate("CornplotGui", u"]", None))
        self.label_58.setText(QCoreApplication.translate("CornplotGui", u"L", None))
        self.label_59.setText(QCoreApplication.translate("CornplotGui", u"=", None))
        self.lengthResult.setText(QCoreApplication.translate("CornplotGui", u"?", None))
        self.curveLengthInterval.setText(QCoreApplication.translate("CornplotGui", u"\u0412\u044b\u0431\u0440\u0430\u0442\u044c \u0438\u043d\u0442\u0435\u0440\u0432\u0430\u043b...", None))
        self.curveLengthAll.setText(QCoreApplication.translate("CornplotGui", u"\u041d\u0430 \u0432\u0441\u0451\u043c \u0438\u043d\u0442\u0435\u0440\u0432\u0430\u043b\u0435", None))
        self.integralGroupBox.setTitle(QCoreApplication.translate("CornplotGui", u"\u0418\u043d\u0442\u0435\u0433\u0440\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435", None))
        self.integralSelectInterval.setText(QCoreApplication.translate("CornplotGui", u"\u0412\u044b\u0431\u0440\u0430\u0442\u044c \u0438\u043d\u0442\u0435\u0440\u0432\u0430\u043b...", None))
        self.integrateAll.setText(QCoreApplication.translate("CornplotGui", u"\u041d\u0430 \u0432\u0441\u0451\u043c \u0438\u043d\u0442\u0435\u0440\u0432\u0430\u043b\u0435", None))
        self.label_30.setText(QCoreApplication.translate("CornplotGui", u"X \u2208 ", None))
        self.label_31.setText(QCoreApplication.translate("CornplotGui", u"[", None))
        self.xIntegrBegin.setText(QCoreApplication.translate("CornplotGui", u"?", None))
        self.label_32.setText(QCoreApplication.translate("CornplotGui", u";", None))
        self.xIntegrEnd.setText(QCoreApplication.translate("CornplotGui", u"?", None))
        self.label_33.setText(QCoreApplication.translate("CornplotGui", u"]", None))
        self.label_34.setText(QCoreApplication.translate("CornplotGui", u"\u222b", None))
        self.label_35.setText(QCoreApplication.translate("CornplotGui", u"f(x)dx =", None))
        self.integralResult.setText(QCoreApplication.translate("CornplotGui", u"?", None))
        self.integralPlot.setText(QCoreApplication.translate("CornplotGui", u"\u041f\u043e\u0441\u0442\u0440\u043e\u0438\u0442\u044c \u0433\u0440\u0430\u0444\u0438\u043a", None))
        self.integralPlotNewWindow.setText(QCoreApplication.translate("CornplotGui", u"\u0412 \u043d\u043e\u0432\u043e\u043c \u043e\u043a\u043d\u0435", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_3), QCoreApplication.translate("CornplotGui", u"\u0418\u043d\u0442\u0435\u0433\u0440\u0430\u043b", None))
        self.groupBox_12.setTitle(QCoreApplication.translate("CornplotGui", u"\u041f\u0440\u0435\u043e\u0431\u0440\u0430\u0437\u043e\u0432\u0430\u043d\u0438\u0435 \u0424\u0443\u0440\u044c\u0435", None))
        self.label_63.setText(QCoreApplication.translate("CornplotGui", u"\u041c\u0430\u043a\u0441\u0438\u043c\u0443\u043c:", None))
        self.deleteConstantCheckbox.setText(QCoreApplication.translate("CornplotGui", u"\u0418\u0441\u043a\u043b\u044e\u0447\u0438\u0442\u044c \u043f\u043e\u0441\u0442\u043e\u044f\u043d\u043d\u0443\u044e \u0441\u043e\u0441\u0442\u0430\u0432\u043b\u044f\u044e\u0449\u0443\u044e", None))
        self.label_40.setText(QCoreApplication.translate("CornplotGui", u"\u041f\u043e\u0440\u044f\u0434\u043e\u043a \u043f\u043e\u043b\u0438\u043d\u043e\u043c\u0430:", None))
        self.fourierIntervalButton.setText(QCoreApplication.translate("CornplotGui", u"\u0412\u044b\u0431\u0440\u0430\u0442\u044c \u0438\u043d\u0442\u0435\u0440\u0432\u0430\u043b...", None))
        self.fourierAllButton.setText(QCoreApplication.translate("CornplotGui", u"\u041d\u0430 \u0432\u0441\u0451\u043c \u0438\u043d\u0442\u0435\u0440\u0432\u0430\u043b\u0435", None))
        self.periodicalFft.setText(QCoreApplication.translate("CornplotGui", u"\u0412 \u0440\u0435\u0430\u043b\u044c\u043d\u043e\u043c \u0432\u0440\u0435\u043c\u0435\u043d\u0438", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_4), QCoreApplication.translate("CornplotGui", u"\u0421\u043f\u0435\u043a\u0442\u0440\u0430\u043b\u044c\u043d\u044b\u0439 \u0430\u043d\u0430\u043b\u0438\u0437", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.plotTab), QCoreApplication.translate("CornplotGui", u"\u0413\u0440\u0430\u0444\u0438\u043a\u0438", None))
        self.menu.setTitle(QCoreApplication.translate("CornplotGui", u"\u0424\u0430\u0439\u043b", None))
        self.menu_2.setTitle(QCoreApplication.translate("CornplotGui", u"\u0421\u043f\u0440\u0430\u0432\u043a\u0430", None))
        self.menu_3.setTitle(QCoreApplication.translate("CornplotGui", u"\u0413\u0440\u0430\u0444\u0438\u043a", None))
        self.menu_4.setTitle(QCoreApplication.translate("CornplotGui", u"\u041e\u0441\u0438", None))
        self.menu_5.setTitle(QCoreApplication.translate("CornplotGui", u"\u0417\u043d\u0430\u043a\u043e\u0432 \u043f\u043e\u0441\u043b\u0435 \u0437\u0430\u043f\u044f\u0442\u043e\u0439", None))
    # retranslateUi

