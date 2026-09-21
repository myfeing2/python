# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLayout,
    QLineEdit, QPushButton, QSizePolicy, QToolButton,
    QWidget)

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(440, 80)
        self.horizontalLayoutWidget = QWidget(Widget)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(10, 10, 421, 31))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SizeConstraint.SetNoConstraint)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.horizontalLayoutWidget)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.lineEdit = QLineEdit(self.horizontalLayoutWidget)
        self.lineEdit.setObjectName(u"lineEdit")

        self.horizontalLayout.addWidget(self.lineEdit)

        self.toolBtn = QToolButton(self.horizontalLayoutWidget)
        self.toolBtn.setObjectName(u"toolBtn")

        self.horizontalLayout.addWidget(self.toolBtn)

        self.okBtn = QPushButton(Widget)
        self.okBtn.setObjectName(u"okBtn")
        self.okBtn.setGeometry(QRect(360, 43, 71, 31))

        self.retranslateUi(Widget)

        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Internet Archive Audio Segment Data File Convert to cue", None))
        self.label.setText(QCoreApplication.translate("Widget", u"Audio Segment Data File", None))
        self.toolBtn.setText(QCoreApplication.translate("Widget", u"...", None))
        self.okBtn.setText(QCoreApplication.translate("Widget", u"Convert", None))
    # retranslateUi

