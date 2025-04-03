import sys
import os
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QMainWindow, QDialog,
    QFileSystemModel, QFileDialog, QLabel, QTreeWidgetItem,
    QCheckBox, QDateTimeEdit
)
from PySide6.QtCore import QDir, QModelIndex

# Frontend UI Imports
from Frontend.MainWindow import Ui_MainWindow
from Frontend.ruleset import Ui_Dialog

# Backend Functionality Imports (Assuming these modules are implemented)
from Backend.action import *
from Backend.sorting_job import *
from Backend.sorting_rule import *
from Backend.condition import *
from Backend.ruleset import *
from Backend.folder_info import *
from Backend.file_info import *
from Backend.rollback import *

# Backend variables
rulesets = []
targetDirectory = None
selectedFolder = None

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
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setup_ruleset_widget()

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
            checkbox = QCheckBox()
            widget = create_item_widget(ext, checkbox)
            checkbox_item = QTreeWidgetItem()
            file_item.addChild(checkbox_item)
            self.ui.listView.setItemWidget(checkbox_item, 0, widget)

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
        modified_item = QTreeWidgetItem(["Modified"])
        created_item = QTreeWidgetItem(["Created"])
        date_item.addChild(modified_item)
        date_item.addChild(created_item)
        self.ui.listView.setItemWidget(modified_item, 0, widget_modified)
        self.ui.listView.setItemWidget(created_item, 0, widget_created)

        # Name and Other rules (placeholders for future expansion)
        name_item = QTreeWidgetItem(["Name"])
        self.ui.listView.addTopLevelItem(name_item)
        other_item = QTreeWidgetItem(["Other"])
        self.ui.listView.addTopLevelItem(other_item)

        self.ui.listView.expandAll()


class MainWindow(QMainWindow):
    """
    The main application window that displays the file system and hooks up UI events.
    """
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_file_system_model()
        self.setup_connections()

        # Default backend hook for folder clicks (can be overridden by backend)
        self.folder_click_callback = None

    def setup_file_system_model(self):
        """
        Sets up the file system model and initializes the target directory.
        """
        self.model = QFileSystemModel()
        self.home_path = QDir.homePath()
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
        self.ui.actionOpen_Rulesets.triggered.connect(self.open_ruleset)

    def change_directory(self):
        """
        Opens a dialog for directory selection and updates the file view.
        """
        dir_path = QFileDialog.getExistingDirectory(self, "Select Directory", QDir.homePath())
        if dir_path:
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
        dialog = RulesetWindow()
        dialog.exec()

    def on_list_view_single_click(self, index: QModelIndex):
        """
        Handles single-clicks in the file system view.
        This will print the folder's path (or display its ruleset in the future) without navigating.
        """
        if index.isValid():
            path = self.model.filePath(index)
            # Call the folder click hook for single-click events.
            self.folder_clicked(path)

    def on_list_view_double_click(self, index: QModelIndex):
        """
        Handles double-clicks in the file system view.
        Double-clicking navigates into the folder and then calls the folder click hook.
        """
        if index.isValid():
            path = self.model.filePath(index)
            if QDir(path).exists():
                self.set_directory(path)
                self.folder_clicked(path)

    def folder_clicked(self, path):
        """
        Default hook for when a folder is clicked (single or double).
        This method can be overridden by backend code to perform custom actions.
        For now, it simply prints the clicked folder path.
        """
        if callable(self.folder_click_callback):
            self.folder_click_callback(path)
        else:
            print(f"Folder clicked: {path}")

    def set_folder_click_callback(self, callback):
        """
        Allows backend code to register a callback to be executed when a folder is clicked.
        """
        self.folder_click_callback = callback

    def get_clicked_folder_path(self):
        """
        Returns the path of the currently selected folder in the file view.
        """
        index = self.ui.listFiles.currentIndex()
        if index.isValid():
            return self.model.filePath(index)
        return None


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
