import sys
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QDialog, QFileSystemModel, QFileDialog,
    QLabel, QTreeWidgetItem, QTreeWidget, QCheckBox, QDateTimeEdit,
    QWidget, QHBoxLayout
)
from PySide6.QtCore import QDir, QModelIndex

# Frontend Imports
from Frontend.MainWindow import Ui_MainWindow
from Frontend.ruleset import Ui_Dialog

# Backend Imports
from Backend.action import Action
from Backend.sorting_job import runSortingJob
from Backend.sorting_rule import SortingRule
from Backend.condition import Condition
from Backend.ruleset import Ruleset
from Backend.folder_info import FolderInfo

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

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self._setup_ui()
        self._setup_connections()

    def _setup_ui(self):
        """Initializes UI components and default values."""
        # Setup file system model for the file list
        self.model = QFileSystemModel()
        self.home_path = QDir.homePath()
        self.model.setRootPath(self.home_path)
        self.ui.listFiles.setModel(self.model)
        self.ui.listFiles.setRootIndex(self.model.index(self.home_path))
        self.ui.label.setText(f"Target Directory: {self.home_path}")
        self.ui.leTargetDirectory.setText(self.home_path)
        # Setup the ruleset tree view
        self.ui.listRules.setHeaderLabels(["Ruleset Options"])
        self.setup_ruleset_widget()

    def _setup_connections(self):
        """Connects UI signals to their respective handlers."""
        self.ui.actionRulesetImport.triggered.connect(self.handle_ruleset_import)
        self.ui.actionOpen_Folder.triggered.connect(self.change_directory)
        self.ui.pushbtn_Dir.clicked.connect(self.change_directory)
        self.ui.leTargetDirectory.returnPressed.connect(self.change_home)
        self.ui.listFiles.doubleClicked.connect(self.on_list_view_double_click)
        self.ui.actionExit.triggered.connect(self.close)
        self.ui.actionOpen_Rulesets.triggered.connect(self.open_ruleset_dialog)
        self.ui.pushButton_5.clicked.connect(self.handle_sorting_job)
        self.ui.listFiles.clicked.connect(self.handle_file_selection)

    # ----------------------- Getters for UI Fields -----------------------

    def get_target_directory(self):
        """Returns the target directory as specified in the line edit."""
        return self.ui.leTargetDirectory.text()

    def get_selected_file_path(self):
        """Returns the currently selected file path from the file list."""
        indexes = self.ui.listFiles.selectionModel().selectedIndexes()
        if indexes:
            return self.model.filePath(indexes[0])
        return None

    # ----------------------- Event Handlers -----------------------

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

    def on_list_view_double_click(self, index: QModelIndex):
        """Handles double-clicks on the file list to navigate directories."""
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

    def handle_ruleset_import(self):
        """Hook for the ruleset import action."""
        print("Ruleset import triggered.")

    def open_ruleset_dialog(self):
        """Opens the ruleset dialog window."""
        dialog = QDialog(self)
        dialog_ui = Ui_Dialog()
        dialog_ui.setupUi(dialog)
        dialog.setWindowTitle("Ruleset")
        if dialog.exec() == QDialog.Accepted:
            print("Ruleset dialog accepted.")

    def handle_file_selection(self):
        """Hook to process file selection events."""
        selected_file = self.get_selected_file_path()
        if selected_file:
            print(f"Selected file: {selected_file}")

    def handle_sorting_job(self):
        """Creates and runs a sorting job using backend functions."""
        selected_folder = self.get_selected_file_path() or self.get_target_directory()
        if not selected_folder:
            print("No folder selected for sorting job.")
            return
        
        # Example backend usage
        move_action = Action("move", selected_folder)
        sorting_rules = Ruleset.fromRules(selected_folder, [
            SortingRule(Condition("extension", "==", ".png"), move_action),
            SortingRule(Condition("extension", "==", ".jpg"), move_action),
            SortingRule(Condition("name", "contains", "photo"), move_action)
        ])
        print(f"Created ruleset for folder: {selected_folder}")
        current_folder_info = FolderInfo.fromPath(QDir.currentPath(), True)
        runSortingJob(sorting_rules, current_folder_info)

    # ----------------------- UI Component Setup -----------------------

    def setup_ruleset_widget(self):
        """Populates the ruleset tree widget with categories and options."""
        data_ruleset = {
            "File": ["png", "jpg", "pdf", "txt"],
            "Date": ["Modified", "Created"],
            "Name": ["Includes", "Excludes"],
            "Other": ["Size", "Dimensions", "Location"]
        }
        # File rules category
        file_item = QTreeWidgetItem(["File"])
        self.ui.listRules.addTopLevelItem(file_item)
        for value in data_ruleset["File"]:
            checkbox = QCheckBox()
            widget = create_item_widget(value, checkbox)
            child_item = QTreeWidgetItem()
            file_item.addChild(child_item)
            self.ui.listRules.setItemWidget(child_item, 0, widget)

        # Date rules category with date pickers
        date_item = QTreeWidgetItem(["Date"])
        self.ui.listRules.addTopLevelItem(date_item)
        datetime_edit_modified = QDateTimeEdit()
        datetime_edit_modified.setCalendarPopup(True)
        datetime_edit_modified.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        datetime_edit_created = QDateTimeEdit()
        datetime_edit_created.setCalendarPopup(True)
        datetime_edit_created.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        modified_item = QTreeWidgetItem(["Modified"])
        created_item = QTreeWidgetItem(["Created"])
        date_item.addChild(modified_item)
        date_item.addChild(created_item)
        self.ui.listRules.setItemWidget(modified_item, 0, create_item_widget("Modified", datetime_edit_modified))
        self.ui.listRules.setItemWidget(created_item, 0, create_item_widget("Created", datetime_edit_created))

        # Name and Other categories
        name_item = QTreeWidgetItem(["Name"])
        self.ui.listRules.addTopLevelItem(name_item)
        other_item = QTreeWidgetItem(["Other"])
        self.ui.listRules.addTopLevelItem(other_item)
        self.ui.listRules.expandAll()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
