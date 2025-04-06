# Frontend UI Imports
import sys
import os
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QMainWindow, QDialog,
    QFileSystemModel, QFileDialog, QLabel, QTreeWidgetItem,
    QLineEdit, QStyleFactory, QCheckBox, QTreeWidget,
    QDateTimeEdit, QCalendarWidget, QListWidgetItem,
    QButtonGroup, QRadioButton
)
from PySide6.QtCore import QDir, QModelIndex, Qt, QCalendar
from PySide6.QtGui import QPalette, QColor
from Frontend.MainWindow import Ui_MainWindow
from Frontend.ruleset import Ui_Dialog

# Backend Functionality Imports
from Backend.action import Action
from Backend.sorting_job import runSortingJob
from Backend.sorting_rule import SortingRule
from Backend.condition import Condition
from Backend.ruleset import Ruleset
from Backend.folder_info import FolderInfo
from Backend.file_info import FileInfo
from Backend.rollback import undoLast, saveRestorePoint, rollbackToRestorePoint
from Backend.app_state import AppState


def create_item_widget(text, control_widget):
    """
    Creates a widget containing a label and a control widget (e.g., checkbox, datetime).
    """
    widget = QWidget()
    layout = QHBoxLayout(widget)
    layout.setContentsMargins(0, 0, 0, 0)
    label = QLabel(text)
    layout.addWidget(label)
    layout.addWidget(control_widget)
    layout.addStretch()
    return widget

class RulesetWindow(QDialog):
    """
    The ruleset dialog window that shows various sorting rules.
    """
    def __init__(self, state):
        super().__init__()
        self.state = state
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        # Radio Buttons
        self.button_group = QButtonGroup(self)
        self.setup_ruleset_widget()
        self.ui.listView.setHeaderHidden(True)
        self.ui.buttonBox.rejected.connect(self.close)
        self.ui.buttonBox.accepted.connect(self.close)
        

        # Track Selected Text per Option Set
        self.selected_values = {
            "File": None
        }
        self.file_options = {
            "File": ["png", "jpg", "pdf", "txt"]
        }

        self.file_option = 0

    def setup_ruleset_widget(self):
        """
        Populates the ruleset tree widget with checkboxes and datetime edits.
        """
        data_ruleset = {
            "File": ["png", "jpg", "pdf", "txt"],
            "Date": ["Modified", "Created"],
            "Name": ["Includes", "Excludes"],
            "Other": ["Size", "Dimensions", "Location"]
        }

        # File type rules
        file_item = QTreeWidgetItem(["File"])
        self.ui.listView.addTopLevelItem(file_item)
        for ext in data_ruleset["File"]:
            rb = QRadioButton(ext)
            self.button_group.addButton(rb)
            checkbox_item = QTreeWidgetItem([f"{ext}"])
            file_item.addChild(checkbox_item)
            self.ui.listView.setItemWidget(checkbox_item, 0, rb)

        # Date rules with QDateTimeEdits
        date_item = QTreeWidgetItem(["Date"])
        self.ui.listView.addTopLevelItem(date_item)
        datetime_edit_modified = QDateTimeEdit()
        datetime_edit_modified.setCalendarPopup(True)
        datetime_edit_modified.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        datetime_edit_created = QDateTimeEdit()
        datetime_edit_created.setCalendarPopup(True)
        datetime_edit_created.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        widget_modified = create_item_widget("Modified", datetime_edit_modified)
        widget_created = create_item_widget("Created", datetime_edit_created)
        modified_item = QTreeWidgetItem()
        created_item = QTreeWidgetItem()
        date_item.addChild(modified_item)
        date_item.addChild(created_item)
        self.ui.listView.setItemWidget(modified_item, 0, widget_modified)
        self.ui.listView.setItemWidget(created_item, 0, widget_created)

        # Name and Other rules
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
        # Size Filter KB/MB/GB

        self.ui.listView.expandAll()

class MainWindow(QMainWindow):
    """
    The main application window that displays the file system and hooks up UI events.
    """
    def __init__(self, state):
        super().__init__()
        self.state = state
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_file_system_model()
        self.setup_connections()
        self.filepath = QDir(self.model.filePath(self.ui.listFiles.rootIndex()))
        self.ruleset = None
        self.ui.listRules.setHeaderHidden(True)

    def setup_file_system_model(self):
        """
        Sets up the file system model and initializes the target directory.
        """
        self.model = QFileSystemModel()
        self.home_path = QDir.homePath()
        self.state.target_directory = self.home_path
        self.model.setRootPath(self.home_path)
        self.ui.listFiles.setModel(self.model)
        self.ui.listFiles.setRootIndex(self.model.index(self.home_path))
        self.ui.label.setText("Target Directory: " + self.home_path)
        self.ui.leTargetDirectory.setText(self.home_path)

    def setup_connections(self):
        """
        Connects UI widgets to their respective handler methods.
        """
        # Directory selection actions
        self.ui.actionOpen_Folder.triggered.connect(self.change_directory)
        self.ui.pushbtn_Dir.clicked.connect(self.change_directory)
        self.ui.leTargetDirectory.returnPressed.connect(self.change_home)
        
        # Connect both single-click and double-click signals
        self.ui.listFiles.clicked.connect(self.on_list_view_single_click)
        self.ui.listFiles.doubleClicked.connect(self.on_list_view_double_click)

        # Menu actions
        self.ui.actionExit.triggered.connect(self.close)
        self.ui.actionExit.setShortcut('Ctrl+Q')
        self.ui.actionExit.setStatusTip('Exit application')
        
        self.ui.actionOpen_Rulesets.triggered.connect(self.open_ruleset)

        # UI actions
        self.ui.pushButton_5.clicked.connect(self.sort)
        self.ui.pushButton_2.clicked.connect(self.backButtonDir) # BackButton Folder
        self.ui.pushButton_3.clicked.connect(self.forwardButtonDir) # Forward Button
        self.ui.btnPlus.clicked.connect(self.open_ruleset)
        
        # Clicked Item reveals forwardBttn directory when clicked
        self.ui.listFiles.clicked.connect(self.oneItemClicked)

        # Light/Dark Mode
        self.is_dark_mode = True
        self.set_dark_theme()
    
    def set_dark_theme(self):
        self.setStyle(QStyleFactory.create("Fusion"))
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
        self.setPalette(palette)

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
                self.set_directory(selected_path)

    def backButtonDir(self):
        path_index = self.ui.listFiles.rootIndex()
        path = self.model.filePath(path_index)
        directory = QDir(path)
        self.filepath = path
        if directory.cdUp():
            parent_dir = directory.absolutePath()
            self.set_directory(parent_dir)
        # else:
        #        print("Already at the top-level Directory")
    
    def change_directory(self):
        # Opens a dialog for directory selection and updates the file view.
        if self.state.target_directory:
            dir_path = QFileDialog.getExistingDirectory(self, "Select Directory", self.state.target_directory)
            self.set_directory(dir_path)

    def change_home(self):
        """
        Changes the working directory based on the text input field.
        """
        path = self.get_target_directory()
        if QDir(path).exists():
            self.set_directory(path)
        else:
            print(f"The directory '{path}' does not exist.")


    def set_directory(self, path):
        """
        Sets the working directory and updates UI elements.
        """
        os.chdir(path)
        self.ui.label.setText(f"Target Directory: {path}")
        self.state.target_directory = path
        print(f"Target Directory: {path}")
        self.ui.leTargetDirectory.setText(path)
        self.model.setRootPath(path)
        self.ui.listFiles.setRootIndex(self.model.index(path))

    def get_target_directory(self):
        """
        Returns the target directory from the input field.
        """
        return self.ui.leTargetDirectory.text()

    def open_ruleset(self):
        """
        Opens the ruleset dialog window.
        """
        dialog = RulesetWindow(self.state)
        dialog.exec()

    def on_list_view_single_click(self, index: QModelIndex):
        # Handles single-clicks in the file system view.
        # This will print the folder's path (or display its ruleset in the future) without navigating.
        
        self.filepath = index
        if index.isValid():
            path = self.model.filePath(index)
            # Call the folder click hook for single-click events.
            self.folder_clicked(path)

    def on_list_view_double_click(self, index: QModelIndex):
        # Handles double-clicks in the file system view.
        # Double-clicking navigates into the folder and then calls the folder click hook.
        if index.isValid():
            path = self.model.filePath(index)
            if QDir(path).exists():
                self.set_directory(path)
                self.folder_clicked(path)
    
    def creatingRulesetWidget(self, value: Ruleset):
        # self.ruleset
        counter = 0
        self.ui.listRules.clear()
        for rule in value.sortingRules:
            # self.ui.listRules
            counter += 1
            rule_item = QTreeWidgetItem([f"Rule {counter}"])
            self.ui.listRules.addTopLevelItem(rule_item)
            blank = QWidget()
            widget = create_item_widget(str(rule), blank)
            rule_child = QTreeWidgetItem()
            rule_item.addChild(rule_child)
            self.ui.listRules.setItemWidget(rule_child, 0, widget)
            print(rule)
            print(rule.condition)
        self.ui.listRules.expandAll()


    def folder_clicked(self, path):
        """
        Default hook for when a folder is clicked (single or double).
        This method can (and is) overridden by backend code to perform custom actions.
        """

        self.state.selected_folder = os.path.normpath(path)
        print(f"Folder clicked: {self.state.selected_folder}")
        
        value = self.state.rulesets.get(self.state.selected_folder)
        self.ruleset = self.state.rulesets.get(self.state.selected_folder)
        # value = Class [Backend.ruleset.Ruleset]
        # Rules in value.sortingRules = Class [Backend.sorting_rule.SortingRule]
        # SortingRule's properties:
        #     self.condition = condition
        #     self.action = action
        if value is not None:
            print(value, type(value))
            self.creatingRulesetWidget(value)
        else:
            print(f"Could not find value for key {self.state.selected_folder}")
            self.ui.listRules.clear()


    def sort(self):
        """
        Hook for sorting files when clicking the Sort button (pushButton_5)
        """
        target = FolderInfo.fromPath(self.state.target_directory, True) # Create a FolderInfo object for target
        runSortingJob(self.state.rulesets, target, description="User-initiated sort")
        print(f"Ran sorting job successfully on directory {self.state.target_directory}")


def main():
    app = QApplication(sys.argv)
    app_state = AppState()

    # Debug test
    documents_path = os.path.join(os.path.expanduser("~"), "Documents")
    folder = FolderInfo.fromPath(documents_path, False)

    photosAction = Action("move", documents_path)
    app_state.rulesets[documents_path] = Ruleset.fromRules(folder, [ 
        SortingRule(Condition("extension", "==", ".png"), photosAction),
        SortingRule(Condition("extension", "==", ".jpg"), photosAction),
        SortingRule(Condition("name", "contains", "photo"), photosAction)
    ])

    window = MainWindow(app_state)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
