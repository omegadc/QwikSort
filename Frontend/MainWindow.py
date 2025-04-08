# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow2.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
    QLineEdit, QListView, QMainWindow, QMenu, QTreeWidget, QTreeView,
    QMenuBar, QPushButton, QSizePolicy, QSpacerItem,
    QStatusBar, QVBoxLayout, QWidget, QRadioButton)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(665, 585)
        # self.actionOpen_Rulesets = QAction(MainWindow)
        # self.actionOpen_Rulesets.setObjectName(u"actionOpen_Rulesets")
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.actionRulesetImport = QAction(MainWindow)
        self.actionRulesetImport.setObjectName(u"actionRulesetImport")
        self.actionExport_Ruleset = QAction(MainWindow)
        self.actionExport_Ruleset.setObjectName(u"actionExport_Ruleset")
        self.actionExport_Ruleset.setIconVisibleInMenu(False)
        self.actionOpen_Folder = QAction(MainWindow)
        self.actionOpen_Folder.setObjectName(u"actionOpen_Folder")
        self.actionOpen_Folder.setShortcutContext(Qt.ShortcutContext.ApplicationShortcut)
        self.actionCreate_New_Folder = QAction(MainWindow)
        self.actionCreate_New_Folder.setObjectName(u"actionCreate_New_Folder")
        self.actionDelete_Folder = QAction(MainWindow)
        self.actionDelete_Folder.setObjectName(u"actionDelete_Folder")
        self.actionCreate_New_Restore_Point = QAction(MainWindow)
        self.actionCreate_New_Restore_Point.setObjectName(u"actionCreate_New_Restore_Point")
        self.actionUndo = QAction(MainWindow)
        self.actionUndo.setObjectName(u"actionUndo")
        self.actionRestore_Back_to_Restore_Point = QAction(MainWindow)
        self.actionRestore_Back_to_Restore_Point.setObjectName(u"actionRestore_Back_to_Restore_Point")
        self.actionTutorial = QAction(MainWindow)
        self.actionTutorial.setObjectName(u"actionTutorial")
        # self.actionUninstall = QAction(MainWindow)
        # self.actionUninstall.setObjectName(u"actionUninstall")
        self.actionLight_Dark_Mode = QAction(MainWindow)
        self.actionLight_Dark_Mode.setObjectName(u"actionLight_Dark_Mode")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_4 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.listFiles = QListView(self.centralwidget)
        self.listFiles.setObjectName(u"listFiles")

        self.verticalLayout_2.addWidget(self.listFiles)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.btnClear = QPushButton(self.centralwidget)
        self.btnClear.setObjectName(u"btnClear")

        self.horizontalLayout_2.addWidget(self.btnClear)

        self.btnPlus = QPushButton(self.centralwidget)
        self.btnPlus.setObjectName(u"btnPlus")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnPlus.sizePolicy().hasHeightForWidth())
        self.btnPlus.setSizePolicy(sizePolicy)
        self.btnPlus.setMaximumSize(QSize(24, 24))

        self.horizontalLayout_2.addWidget(self.btnPlus)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)


        self.gridLayout.addLayout(self.verticalLayout_2, 2, 0, 2, 1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_4.addWidget(self.label_3)

        # self.pushButton_6 = QPushButton(self.centralwidget)
        # self.pushButton_6.setObjectName(u"pushButton_6")

        # self.horizontalLayout_4.addWidget(self.pushButton_6)

        # self.pushButton_7 = QPushButton(self.centralwidget)
        # self.pushButton_7.setObjectName(u"pushButton_7")

        # self.horizontalLayout_4.addWidget(self.pushButton_7)

        self.pushbttn_matchAll = QRadioButton(self.centralwidget)
        self.pushbttn_matchAll.setObjectName(u"pushbttn_matchAll")

        self.horizontalLayout_4.addWidget(self.pushbttn_matchAll)

        self.pushbttn_matchOne = QRadioButton(self.centralwidget)
        self.pushbttn_matchOne.setObjectName(u"pushbttn_matchOne")

        self.horizontalLayout_4.addWidget(self.pushbttn_matchOne)


        self.gridLayout.addLayout(self.horizontalLayout_4, 1, 1, 1, 1)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.listRules = QTreeWidget(self.centralwidget)
        self.listRules.setObjectName(u"listRules")

        self.verticalLayout_3.addWidget(self.listRules)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        # self.pushButton_4 = QPushButton(self.centralwidget)
        # self.pushButton_4.setObjectName(u"pushButton_4")

        # self.horizontalLayout_3.addWidget(self.pushButton_4)

        self.pushButton_5 = QPushButton(self.centralwidget)
        self.pushButton_5.setObjectName(u"SortBttn")
        sizePolicy.setHeightForWidth(self.pushButton_5.sizePolicy().hasHeightForWidth())
        self.pushButton_5.setSizePolicy(sizePolicy)

        self.horizontalLayout_3.addWidget(self.pushButton_5)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)


        self.gridLayout.addLayout(self.verticalLayout_3, 2, 1, 2, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMaximumSize(QSize(16777215, 20))

        self.verticalLayout.addWidget(self.label)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.leTargetDirectory = QLineEdit(self.centralwidget)
        self.leTargetDirectory.setObjectName(u"leTargetDirectory")

        self.horizontalLayout_6.addWidget(self.leTargetDirectory)

        self.pushbtn_Dir = QPushButton(self.centralwidget)
        self.pushbtn_Dir.setObjectName(u"pushbtn_Dir")
        font = QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setItalic(False)
        self.pushbtn_Dir.setFont(font)

        self.horizontalLayout_6.addWidget(self.pushbtn_Dir)


        self.verticalLayout.addLayout(self.horizontalLayout_6)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 2)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy1)
        self.pushButton.setMaximumSize(QSize(50, 16777215))
        self.pushButton.setFlat(True)

        self.horizontalLayout.addWidget(self.pushButton)


        self.verticalLayout_5.addLayout(self.horizontalLayout)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer)

        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        font1 = QFont()
        font1.setFamilies([u"Script MT"])
        font1.setPointSize(12)
        font1.setBold(True)
        font1.setItalic(False)
        font1.setUnderline(False)
        font1.setKerning(False)
        self.pushButton_2.setFont(font1)

        self.horizontalLayout_5.addWidget(self.pushButton_2)

        self.pushButton_3 = QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName(u"pushButton_3")
        font2 = QFont()
        font2.setFamilies([u"Script MT"])
        font2.setPointSize(12)
        self.pushButton_3.setFont(font2)

        self.horizontalLayout_5.addWidget(self.pushButton_3)


        self.verticalLayout_5.addLayout(self.horizontalLayout_5)


        self.gridLayout.addLayout(self.verticalLayout_5, 1, 0, 1, 1)


        self.verticalLayout_4.addLayout(self.gridLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 665, 33))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuFile.setGeometry(QRect(347, 183, 160, 126))
        self.menuRulesets = QMenu(self.menubar)
        self.menuRulesets.setObjectName(u"menuRulesets")
        self.menuRulesets.setGeometry(QRect(399, 183, 139, 126))
        self.menuRollback = QMenu(self.menubar)
        self.menuRollback.setObjectName(u"menuRollback")
        self.menuRollback.setGeometry(QRect(477, 183, 196, 102))
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        self.menuHelp.setGeometry(QRect(652, 183, 138, 102))
        # self.menuPreferences = QMenu(self.menubar)
        # self.menuPreferences.setObjectName(u"menuPreferences")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuRulesets.menuAction())
        self.menubar.addAction(self.menuRollback.menuAction())
        # self.menubar.addAction(self.menuPreferences.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionOpen_Folder)
        self.menuFile.addAction(self.actionCreate_New_Folder)
        self.menuFile.addAction(self.actionDelete_Folder)
        self.menuFile.addAction(self.actionExit)
        # self.menuRulesets.addAction(self.actionOpen_Rulesets)
        self.menuRulesets.addAction(self.actionRulesetImport)
        self.menuRulesets.addAction(self.actionExport_Ruleset)
        self.menuRollback.addAction(self.actionCreate_New_Restore_Point)
        self.menuRollback.addAction(self.actionRestore_Back_to_Restore_Point)
        self.menuRollback.addAction(self.actionUndo)
        self.menuHelp.addAction(self.actionTutorial)
        # self.menuHelp.addAction(self.actionUninstall)
        # self.menuPreferences.addAction(self.actionLight_Dark_Mode)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        # self.actionOpen_Rulesets.setText(QCoreApplication.translate("MainWindow", u"Open Rulesets", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow",u"&Exit",None))
        self.actionRulesetImport.setText(QCoreApplication.translate("MainWindow", u"Import Ruleset", None))
        self.actionExport_Ruleset.setText(QCoreApplication.translate("MainWindow", u"Export Ruleset", None))
        self.actionOpen_Folder.setText(QCoreApplication.translate("MainWindow", u"Open Folder", None))
#endif // QT_CONFIG(shortcut)
        self.actionCreate_New_Folder.setText(QCoreApplication.translate("MainWindow", u"Create New Folder", None))
#endif // QT_CONFIG(shortcut)
        self.actionDelete_Folder.setText(QCoreApplication.translate("MainWindow", u"Delete Folder", None))
        self.actionUndo.setText(QCoreApplication.translate("MainWindow", u"Undo", None))
        self.actionCreate_New_Restore_Point.setText(QCoreApplication.translate("MainWindow", u"Create New Restore Point", None))
        self.actionRestore_Back_to_Restore_Point.setText(QCoreApplication.translate("MainWindow", u"Revert to Restore Point", None))
        self.actionTutorial.setText(QCoreApplication.translate("MainWindow", u"Tutorial", None))
        # self.actionUninstall.setText(QCoreApplication.translate("MainWindow", u"Uninstall", None))
        self.actionLight_Dark_Mode.setText(QCoreApplication.translate("MainWindow", u"Light/Dark Mode", None))
        self.btnClear.setText(QCoreApplication.translate("MainWindow", u"Clear", None))
        self.btnPlus.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Rules", None))
        self.pushbttn_matchAll.setText(QCoreApplication.translate("MainWindow", u"Match All", None))
        self.pushbttn_matchOne.setText(QCoreApplication.translate("MainWindow", u"Match One", None))
        # self.pushButton_6.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        # self.pushButton_7.setText(QCoreApplication.translate("MainWindow", u"Load", None))
        # self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"Delete Files", None))
        self.pushButton_5.setText(QCoreApplication.translate("MainWindow", u"Sort", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Target Directory", None))
        self.pushbtn_Dir.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Files", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Sort?", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"<", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u">", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuRulesets.setTitle(QCoreApplication.translate("MainWindow", u"Rulesets", None))
        self.menuRollback.setTitle(QCoreApplication.translate("MainWindow", u"Rollback", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
        # self.menuPreferences.setTitle(QCoreApplication.translate("MainWindow", u"Preferences", None))
    # retranslateUi

