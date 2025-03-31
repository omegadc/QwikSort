# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ruleset.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QHBoxLayout, QLabel, QListView, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(492, 390)
        self.horizontalLayout_2 = QHBoxLayout(Dialog)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalWidget_3 = QWidget(Dialog)
        self.verticalWidget_3.setObjectName(u"verticalWidget_3")
        self.verticalLayout_3 = QVBoxLayout(self.verticalWidget_3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_rules = QLabel(self.verticalWidget_3)
        self.label_rules.setObjectName(u"label_rules")
        font = QFont()
        font.setPointSize(13)
        self.label_rules.setFont(font)

        self.verticalLayout.addWidget(self.label_rules)

        self.listView = QListView(self.verticalWidget_3)
        self.listView.setObjectName(u"listView")

        self.verticalLayout.addWidget(self.listView)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_sets = QLabel(self.verticalWidget_3)
        self.label_sets.setObjectName(u"label_sets")
        self.label_sets.setFont(font)

        self.verticalLayout_2.addWidget(self.label_sets)

        self.listView_2 = QListView(self.verticalWidget_3)
        self.listView_2.setObjectName(u"listView_2")

        self.verticalLayout_2.addWidget(self.listView_2)


        self.horizontalLayout.addLayout(self.verticalLayout_2)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.buttonBox = QDialogButtonBox(self.verticalWidget_3)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout_3.addWidget(self.buttonBox)


        self.horizontalLayout_2.addWidget(self.verticalWidget_3)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label_rules.setText(QCoreApplication.translate("Dialog", u"Rules", None))
        self.label_sets.setText(QCoreApplication.translate("Dialog", u"Sets", None))
    # retranslateUi

