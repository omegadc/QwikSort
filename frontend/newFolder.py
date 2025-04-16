# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'newFolder.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(316, 156)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QSize(315, 150))
        Form.setMaximumSize(QSize(350, 200))
        self.verticalLayout_3 = QVBoxLayout(Form)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.labelNewFolder = QLabel(Form)
        self.labelNewFolder.setObjectName(u"labelNewFolder")
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setPointSize(12)
        self.labelNewFolder.setFont(font)

        self.verticalLayout.addWidget(self.labelNewFolder)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lineEditFolderName = QLineEdit(Form)
        self.lineEditFolderName.setObjectName(u"lineEditFolderName")
        font1 = QFont()
        font1.setPointSize(12)
        self.lineEditFolderName.setFont(font1)

        self.horizontalLayout.addWidget(self.lineEditFolderName)

        self.buttonEnter = QPushButton(Form)
        self.buttonEnter.setObjectName(u"buttonEnter")

        self.horizontalLayout.addWidget(self.buttonEnter)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.verticalLayout_3.addLayout(self.verticalLayout)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.labelNewFolder.setText(QCoreApplication.translate("Form", u"Creating New Folder", None))
        self.lineEditFolderName.setText("")
        self.lineEditFolderName.setPlaceholderText(QCoreApplication.translate("Form", u"Name of Folder", None))
        self.buttonEnter.setText(QCoreApplication.translate("Form", u"Enter", None))
    # retranslateUi

