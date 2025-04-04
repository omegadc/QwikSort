import sys
import os
from pathlib import Path
from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QMainWindow, QDialog, QFileSystemModel, QFileDialog, QLabel
from PySide6.QtWidgets import ( QLineEdit, QStyleFactory, QCheckBox, QTreeWidgetItem, QTreeWidget, QDateTimeEdit, QCalendarWidget, QListWidgetItem )
from PySide6.QtCore import QDir, QModelIndex, Qt, QCalendar
from PySide6.QtGui import QPalette, QColor
# Front End Import
from Frontend.MainWindow import Ui_MainWindow
from Frontend.ruleset import Ui_Dialog
from Frontend.ErrorMessageFolder import ErrorDialog
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

    widget = QWidget()
    layout = QHBoxLayout(widget)
    layout.setContentsMargins(0, 0, 0, 0)
    label = QLabel(text)
    layout.addWidget(label)
    layout.addWidget(control_widget)
    # Optionally add a stretch if you want the widget aligned to the left
    layout.addStretch()
    return widget

class ErrorMessage(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = ErrorDialog()
        self.ui.setupUi(self)
        self.ui.buttonBox.setCenterButtons(True)
        self.ui.buttonBox.rejected.connect(self.reject)

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
        datetime_item = QTreeWidgetItem()
        datetime_item2 = QTreeWidgetItem()
        date_item.addChild(datetime_item)
        date_item.addChild(datetime_item2)
        self.ui.listView.setItemWidget(datetime_item, 0, widget1)
        self.ui.listView.setItemWidget(datetime_item2, 0, widget2)

        # Name
        name_item = QTreeWidgetItem(["Name"])
        self.ui.listView.addTopLevelItem(name_item)
        self.regexInclude = QLineEdit(self)
        self.regexExclude = QLineEdit(self)
        # self.regexInclude.textChanged.connect(self.filter_files)
        widget_include = create_item_widget("Include",self.regexInclude)
        widget_exclude = create_item_widget("Exclude",self.regexExclude)
        name_item1 = QTreeWidgetItem()
        name_item2 = QTreeWidgetItem()
        name_item.addChild(name_item1)
        name_item.addChild(name_item2)
        self.ui.listView.setItemWidget(name_item1, 0, widget_include)
        self.ui.listView.setItemWidget(name_item2, 0, widget_exclude)
        

        # Other 
        other_item = QTreeWidgetItem(["Other"])
        self.ui.listView.addTopLevelItem(other_item)



        self.ui.listView.expandAll()

    def filter_files(self):
        keywords = [kw.strip().lower() for kw in self.regexInclude.text().split(",") if kw.strip()]
        self.ui.listView.clear()

        filtered_files = [
            file for file in self.ui.listView 
            if all(kw in file.lower() for kw in keywords)
        ]
        self.ui.listView.setItemWidget(filtered_files)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()  # Create an instance of the UI class
        self.ui.setupUi(self)  # Set up the UI
        self.ui.actionOpen_Folder.triggered.connect(self.change_directory)

        self.state = None
        self.filepath = None


        # Changing file directory
        self.ui.pushbtn_Dir.clicked.connect(self.change_directory)
        self.ui.pushbtn_Dir.pressed.connect(self.change_directory)
        self.ui.leTargetDirectory.returnPressed.connect(self.change_home)

        # Setting up List View
        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.homePath())
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

        # Clicked Item reveals forwardBttn directory when clicked
        self.ui.listFiles.clicked.connect(self.oneItemClicked)

        # Light/Dark Mode
        self.is_dark_mode = True
        self.set_dark_theme()
        # self.ui.actionLight_Dark_Mode.triggered.connect(self.toggle_theme)
    
    # Light/Dark mode Implementation
    # def toggle_theme(self):
    #     if self.is_dark_mode:
    #         self.set_light_theme()
    #     else:
    #         self.set_dark_theme()
    #     self.is_dark_mode = not self.is_dark_mode

    # def set_light_theme(self):
    #     app.setStyle(QStyleFactory.create("Fusion"))
    #     palette = QPalette()
    #     palette.setColor(QPalette.ColorRole.Window, QColor(240, 240, 240))
    #     palette.setColor(QPalette.ColorRole.WindowText, QColor(0,0,0))
    #     app.setPalette(palette)
    
    def set_dark_theme(self):
        app.setStyle(QStyleFactory.create("Fusion"))
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
        app.setPalette(palette)

    def oneItemClicked(self, index: QModelIndex):
        # self.filepath = self.model.filePath(index)
        if index.isValid():
            selected_path = self.model.filePath(index)
            if QDir(selected_path).exists():
                self.filepath = selected_path


    def forwardButtonDir(self, index: QModelIndex):
        if self.filepath == None:
            dialog = ErrorMessage()
            dialog.exec()
        else:
            selected_path = self.filepath
            if QDir(selected_path).exists():
                os.chdir(selected_path)
                self.update_directory_view(selected_path)

    def backButtonDir(self):
        path_index = self.ui.listFiles.rootIndex()
        path = self.model.filePath(path_index)
        directory = QDir(path)
        self.filepath = path
        if directory.cdUp():
            parent_dir = directory.absolutePath()
            self.update_directory_view(parent_dir)
        else:
            print("Already at the top-level Directory")

    def change_home(self):
        path = self.ui.leTargetDirectory.text()
        if QDir(path).exists():
            os.chdir(path)
            self.ui.label.setText(f"Target Directory: {path}")
            self.model.setRootPath(path)
            self.ui.listFiles.setRootIndex(self.model.index(path))
        else:
            print(f"The directory '{path}' does not exists.")

    def change_directory(self):
        #Opens a directory selection dialog and updates the file system view.
        dir_path = QFileDialog.getExistingDirectory(self, "Select Directory", QDir.homePath())
        if dir_path:
            os.chdir(dir_path)  # Change the working directory
            self.ui.label.setText(f"Target Directory: {dir_path}")
            self.ui.leTargetDirectory.setText(f"{dir_path}")
            self.model.setRootPath(dir_path)
            # self.tree_view.setRootIndex(self.model.index(dir_path))
            self.ui.listFiles.setRootIndex(self.model.index(dir_path))
    
    def openingRuleset(self):
        dialog = RulesetWindow()
        dialog.exec()

    def on_list_view_click(self, index: QModelIndex):
        self.filepath = index
        if index.isValid():
            selected_path = self.model.filePath(index)
            if QDir(selected_path).exists():
                os.chdir(selected_path)
                self.update_directory_view(selected_path)

    def update_directory_view(self, path):
        self.ui.label.setText(f"Target Directory: {path}")
        self.ui.leTargetDirectory.setText(f"{path}")
        self.model.setRootPath(path)
        self.ui.listFiles.setRootIndex(self.model.index(path))
        




app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()

### command line arg to run
# pyside6-uic {file.ui} -o {file.py} 
#
# for pyside6 designer run
#pyside6-designer