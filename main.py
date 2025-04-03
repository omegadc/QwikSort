import sys
import os
from pathlib import Path
from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QMainWindow, QDialog, QFileSystemModel, QFileDialog, QLabel
from PySide6.QtWidgets import ( QCheckBox, QTreeWidgetItem, QTreeWidget, QDateTimeEdit, QCalendarWidget, QListWidgetItem )
from PySide6.QtCore import QDir, QModelIndex, Qt, QCalendar
# Front End Import
from Frontend.MainWindow import Ui_MainWindow
from Frontend.ruleset import Ui_Dialog
# Backend Import
# from Backend.action import *
# from Backend.sorting_job import *
# from Backend.sorting_rule import *
# from Backend.condition import *
# from Backend.ruleset import *
# from Backend.folder_info import *
# from Backend.file_info import *
# from Backend.rollback import *

# Subclass QMainWindow to customize your application's main window
  # need to create a custom widget in order to have checkbox next to label/text
        # for QTreeWidget
def create_item_widget(text, control_widget):
    """Creates a widget containing a label and a control"""
    widget = QWidget()
    layout = QHBoxLayout(widget)
    layout.setContentsMargins(0, 0, 0, 0)
    label = QLabel(text)
    layout.addWidget(label)
    layout.addWidget(control_widget)
    layout.addStretch()
    return widget

class RulesetWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setup_ruleset_widget()
        self.ui.listView.setHeaderHidden(True)

    def setup_ruleset_widget(self):
        data_ruleset = {"File":["png","jpg","pdf","txt"],
                        "Date":["Modified","Created"],
                        "Name":["Includes","Excludes"],
                        "Other":["Size", "Dimensions","Location"]}
        file_item = QTreeWidgetItem(["File"])
        self.ui.listView.addTopLevelItem(file_item)
        
        # CheckBox Item
        for values in data_ruleset["File"]:
            checkbox = QCheckBox()
            widget = create_item_widget(values,checkbox)
            checkbox_item = QTreeWidgetItem()
            file_item.addChild(checkbox_item)
            self.ui.listView.setItemWidget(checkbox_item,0,widget)
        # Date / DateTimeEdit
        date_item = QTreeWidgetItem(["Date"])
        self.ui.listView.addTopLevelItem(date_item)
        datetime_edit = QDateTimeEdit()
        datetime_edit.setCalendarPopup(True)
        datetime_edit.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        # have to do these for each entry with an input
        datetime_edit2 = QDateTimeEdit()
        datetime_edit2.setCalendarPopup(True)
        datetime_edit2.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        widget1 = create_item_widget("Modified", datetime_edit)
        widget2 = create_item_widget("Created", datetime_edit2)
        datetime_item = QTreeWidgetItem(["Modified"])
        datetime_item2 = QTreeWidgetItem(["Created"])
        date_item.addChild(datetime_item)
        date_item.addChild(datetime_item2)
        self.ui.listView.setItemWidget(datetime_item, 0, widget1)
        self.ui.listView.setItemWidget(datetime_item2, 0, widget2)

        # Name
        name_item = QTreeWidgetItem(["Name"])
        self.ui.listView.addTopLevelItem(name_item)
        # Other 
        other_item = QTreeWidgetItem(["Other"])
        self.ui.listView.addTopLevelItem(other_item)

        self.ui.listView.expandAll()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()  # Create an instance of the UI class
        self.ui.setupUi(self)  # Set up the UI
        self.ui.actionOpen_Folder.triggered.connect(self.change_directory)

        # Changing file directory
        self.ui.pushbtn_Dir.clicked.connect(self.change_directory)
        self.ui.pushbtn_Dir.pressed.connect(self.change_directory)
        self.ui.leTargetDirectory.returnPressed.connect(self.change_home)

        # Setting up List View
        self.model = QFileSystemModel()
        self.home_path = QDir.homePath()
        self.model.setRootPath(self.home_path)
        self.ui.listFiles.setModel(self.model)
        self.ui.listFiles.setRootIndex(self.model.index(QDir.homePath()))
        self.ui.label.setText("Target Directory: "+QDir.homePath())
        self.ui.leTargetDirectory.setText(f"{QDir.homePath()}")
        # Connect list view click to change directory
        self.ui.listFiles.doubleClicked.connect(self.on_list_view_click)
        ## Creating functionality for menuFile Options
        self.ui.actionExit.setShortcut('Ctrl+Q')
        self.ui.actionExit.setStatusTip('Exit application')
        self.ui.actionExit.triggered.connect(self.close)

        ## making ruleset menu bar exec qaction
        self.ui.actionOpen_Rulesets.triggered.connect(self.openingRuleset)
        # Back/Forward Button Functionality
        self.ui.pushButton_2.clicked.connect(self.backButtonDir)
        self.ui.pushButton_3.clicked.connect(self.forwardButtonDir)

        # lastDirectory should retain the last directory visited
        self.lastDirectory = QDir(self.model.filePath(self.ui.listFiles.rootIndex()))
        self.ui.listFiles.clicked
    
    def forwardButtonDir(self):
        lastDir = self.lastDirectory
        lastDir.canonicalPath
        self.ui.listFiles.setRootIndex(self.model.index(lastDir.canonicalPath))
        self.ui.leTargetDirectory.setText(lastDir.canonicalPath)

        item = QListWidgetItem()
        item.c


    def backButtonDir(self):
        path_index = self.ui.listFiles.rootIndex()
        path = self.model.filePath(path_index)
        directory = QDir(path)
        self.lastDirectory = directory
        if directory.cdUp():
            parent_dir = directory.absolutePath()
            self.ui.listFiles.setRootIndex(self.model.index(parent_dir))
            self.ui.leTargetDirectory.setText(parent_dir)
        else:
            print("Already at the top-level Directory")

    def change_home(self):
        """Updates the working directory based on the line edit value."""
        path = self.get_target_directory()
        if QDir(path).exists():
            os.chdir(path)
            self.ui.label.setText(f"Target Directory: {path}")
            self.model.setRootPath(path)
            self.ui.listFiles.setRootIndex(self.model.index(path))
        else:
            print(f"The directory '{path}' does not exist.")

    def change_directory(self):
        """Opens a directory selection dialog and updates the file list view."""
        dir_path = QFileDialog.getExistingDirectory(self, "Select Directory", QDir.homePath())
        if dir_path:
            os.chdir(dir_path)
            self.ui.label.setText(f"Target Directory: {dir_path}")
            self.ui.leTargetDirectory.setText(dir_path)
            self.model.setRootPath(dir_path)
            self.ui.listFiles.setRootIndex(self.model.index(dir_path))
    
    def openingRuleset(self):
        dialog = RulesetWindow()
        dialog.exec()

    def on_list_view_click(self, index: QModelIndex):
        if index.isValid():
            selected_path = self.model.filePath(index)
            if QDir(selected_path).exists():
                os.chdir(selected_path)
                self.update_directory_view(selected_path)

    def update_directory_view(self, path):
        """Updates the directory view after a change."""
        self.ui.label.setText(f"Target Directory: {path}")
        self.ui.leTargetDirectory.setText(path)
        self.model.setRootPath(path)
        self.ui.listFiles.setRootIndex(self.model.index(path))
        




app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
