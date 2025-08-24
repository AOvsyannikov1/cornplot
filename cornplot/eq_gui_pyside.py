# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'eqGui.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDoubleSpinBox, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(413, 217)
        Form.setMaximumSize(QSize(800, 600))
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.eqName = QLineEdit(Form)
        self.eqName.setObjectName(u"eqName")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.eqName.sizePolicy().hasHeightForWidth())
        self.eqName.setSizePolicy(sizePolicy)
        self.eqName.setMaxLength(32)

        self.horizontalLayout_2.addWidget(self.eqName)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.eqLine = QLineEdit(Form)
        self.eqLine.setObjectName(u"eqLine")
        sizePolicy.setHeightForWidth(self.eqLine.sizePolicy().hasHeightForWidth())
        self.eqLine.setSizePolicy(sizePolicy)
        self.eqLine.setMaxLength(64)

        self.horizontalLayout.addWidget(self.eqLine)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.line = QFrame(Form)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_3.addWidget(self.label_3)

        self.xMin = QDoubleSpinBox(Form)
        self.xMin.setObjectName(u"xMin")
        self.xMin.setDecimals(3)
        self.xMin.setMinimum(-2147483647.000000000000000)
        self.xMin.setMaximum(2147483647.000000000000000)

        self.horizontalLayout_3.addWidget(self.xMin)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_4 = QLabel(Form)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_4.addWidget(self.label_4)

        self.xMax = QDoubleSpinBox(Form)
        self.xMax.setObjectName(u"xMax")
        self.xMax.setDecimals(3)
        self.xMax.setMinimum(-2147483647.000000000000000)
        self.xMax.setMaximum(2147483647.000000000000000)

        self.horizontalLayout_4.addWidget(self.xMax)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_5 = QLabel(Form)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_5.addWidget(self.label_5)

        self.xStep = QDoubleSpinBox(Form)
        self.xStep.setObjectName(u"xStep")
        self.xStep.setDecimals(3)
        self.xStep.setMaximum(2147483647.000000000000000)
        self.xStep.setSingleStep(0.010000000000000)
        self.xStep.setValue(0.010000000000000)

        self.horizontalLayout_5.addWidget(self.xStep)


        self.verticalLayout.addLayout(self.horizontalLayout_5)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.button = QPushButton(Form)
        self.button.setObjectName(u"button")

        self.gridLayout.addWidget(self.button, 2, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 1, 0, 1, 1)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"\u0412\u0432\u043e\u0434 \u0443\u0440\u0430\u0432\u043d\u0435\u043d\u0438\u044f", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435:", None))
        self.eqName.setText("")
        self.label.setText(QCoreApplication.translate("Form", u"\u0423\u0440\u0430\u0432\u043d\u0435\u043d\u0438\u0435:", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u041d\u0430\u0447\u0430\u043b\u044c\u043d\u043e\u0435 \u0437\u043d\u0430\u0447\u0435\u043d\u0438\u0435 \u0425:", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"\u041a\u043e\u043d\u0435\u0447\u043d\u043e\u0435 \u0437\u043d\u0430\u0447\u0435\u043d\u0438\u0435 \u0425:", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"\u0428\u0430\u0433:", None))
        self.button.setText(QCoreApplication.translate("Form", u"\u041f\u043e\u0441\u0442\u0440\u043e\u0438\u0442\u044c", None))
    # retranslateUi

