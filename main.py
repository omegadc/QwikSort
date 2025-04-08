# Frontend UI Imports
import sys
import os
from datetime import datetime
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QMainWindow, QDialog,
    QFileSystemModel, QFileDialog, QLabel, QTreeWidgetItem,
    QLineEdit, QStyleFactory, QCheckBox, QTreeWidget,
    QDateTimeEdit, QCalendarWidget, QListWidget, QListWidgetItem,
    QButtonGroup, QRadioButton, QMessageBox
)
from PySide6.QtCore import QDir, QModelIndex, QDateTime, Qt, QCalendar
from PySide6.QtGui import QPalette, QColor
from Frontend.MainWindow import Ui_MainWindow
from Frontend.ruleset import Ui_Dialog
from Frontend.newFolder import Ui_Form

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

class NewFolderWindow(QDialog):
    def __init__(self, state):
        super().__init__()
        self.ui = Ui_Form()
        self.state = state
        # self.ui.setupUi()
        self.ui.setupUi(self)
        self.setup_file_system_model()
        # self.ui.buttonEnter.clicked
        self.ui.lineEditFolderName.returnPressed.connect(self.createNewFolder)
        self.ui.buttonEnter.clicked.connect(self.createNewFolder)
    
    def createNewFolder(self):
        text = self.ui.lineEditFolderName.text().strip()
        if not text:
            return

        index = self.model.mkdir(self.model.index(self.state.target_directory), text)
        if not index.isValid():
            QMessageBox.warning(self, "Could not create folder",
                                f"Failed to create “{text}” in\n{self.state.target_directory}") # self.model.filePath(index)
        else:
            # MainWindow(self, self.state).ui.listFiles.currentIndex(index)
            # MainWindow(self, self.state).ui.listFiles.scrollTo(index)
            self.ui.lineEditFolderName.clear()
            self.close()
        
        


    def setup_file_system_model(self):
        """
        Sets up the file system model and initializes the target directory.
        """
        self.model = QFileSystemModel()
        self.home_path = self.state.target_directory
        self.model.setRootPath(self.home_path)

class RulesetWindow(QDialog):
    """
    The ruleset dialog window that shows various sorting rules.
    """
    def __init__(self, state, main_window):
        super().__init__()
        self.state = state
        self.main_window = main_window
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        # Radio Buttons
        self.button_group = QButtonGroup(self)
        self.setup_ruleset_widget()
        self.ui.listView.setHeaderHidden(True)
        self.ui.buttonBox.rejected.connect(self.close)
        self.ui.buttonBox.accepted.connect(self.apply_rule_to_ruleset)
        

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

        # Custom extension input
        custom_ext_label = QLabel("Other:")
        self.custom_ext_input = QLineEdit()
        self.custom_ext_input.setPlaceholderText("Enter extension (e.g., csv)")
        custom_widget = QWidget()
        custom_layout = QHBoxLayout(custom_widget)
        custom_layout.setContentsMargins(0, 0, 0, 0)
        custom_layout.addWidget(custom_ext_label)
        custom_layout.addWidget(self.custom_ext_input)

        # Preset extensions
        for ext in data_ruleset["File"]:
            rb = QRadioButton(ext)
            self.button_group.addButton(rb)
            rb.toggled.connect(lambda checked, line_edit=self.custom_ext_input: line_edit.clear() if checked else None)
            checkbox_item = QTreeWidgetItem([f"{ext}"])
            file_item.addChild(checkbox_item)
            self.ui.listView.setItemWidget(checkbox_item, 0, rb)

        custom_ext_item = QTreeWidgetItem(["Other"])
        file_item.addChild(custom_ext_item)
        self.ui.listView.setItemWidget(custom_ext_item, 0, custom_widget)

        # Date rules with QDateTimeEdits
        date_item = QTreeWidgetItem(["Date"])
        self.ui.listView.addTopLevelItem(date_item)
        datetime_edit_modified = QDateTimeEdit()
        datetime_edit_modified.setCalendarPopup(True)
        datetime_edit_modified.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        datetime_edit_created = QDateTimeEdit()
        datetime_edit_created.setCalendarPopup(True)
        datetime_edit_created.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        # set the default date to "2001-01-01 00:00:00"
        default_dt = QDateTime.fromString("2001-01-01 00:00:00", "yyyy-MM-dd HH:mm:ss")
        datetime_edit_modified.setDateTime(default_dt)
        datetime_edit_created.setDateTime(default_dt)
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
        # other_item = QTreeWidgetItem(["Other"])
        # self.ui.listView.addTopLevelItem(other_item)
        # Size Filter KB/MB/GB

        self.ui.listView.expandAll()

    def get_new_rule(self):
        """
        Builds and returns a SortingRule object based on the current UI inputs.
        Returns None if no valid rule is selected.
        """
        condition = None

        # Check extension radio buttons
        for btn in self.button_group.buttons():
            if btn.isChecked():
                ext = btn.text().lower()
                condition = Condition("extension", "==", f".{ext}")
                break
        
        # Check custom extension if no button selected
        if condition is None:
            custom_ext = self.custom_ext_input.text().strip().lower()
            if custom_ext:
                if not custom_ext.startswith('.'):
                    custom_ext = '.' + custom_ext
                condition = Condition("extension", "==", custom_ext)

        # Check date condition only if no extension rule selected
        if condition is None:
            mod_widget = self.ui.listView.itemWidget(self.ui.listView.topLevelItem(1).child(0), 0).layout().itemAt(1).widget()
            created_widget = self.ui.listView.itemWidget(self.ui.listView.topLevelItem(1).child(1), 0).layout().itemAt(1).widget()

            # The baseline "unset" value
            default_dt = QDateTime.fromString("2001-01-01 00:00:00", "yyyy-MM-dd HH:mm:ss")

            mod_dt = mod_widget.dateTime()
            created_dt = created_widget.dateTime()

            # Only create a date condition if it's not the default
            if mod_dt.toSecsSinceEpoch() != default_dt.toSecsSinceEpoch():
                dt = mod_dt.toPython()
                condition = Condition("dateModified", ">=", dt)
            elif created_dt.toSecsSinceEpoch() != default_dt.toSecsSinceEpoch():
                dt = created_dt.toPython()
                condition = Condition("dateCreated", ">=", dt)

        # Check name condition only if no extension or date rule selected
        if condition is None:
            name_includes = self.regexInclude.text().strip()
            name_excludes = self.regexExclude.text().strip()
            if name_includes:
                condition = Condition("name", "includes", name_includes)
            elif name_excludes:
                condition = Condition("name", "excludes", name_excludes)

        if condition is None:
            return None  # No rule selected

        # Default action - move to the folder where the rule is being created
        action = Action("move", self.state.selected_folder)
        return SortingRule(condition, action)
    
    def apply_rule_to_ruleset(self):
        new_rule = self.get_new_rule()
        if new_rule:
            path = self.state.selected_folder
            folder = FolderInfo.fromPath(path, False)

            if path in self.state.rulesets:
                self.state.rulesets[path].sortingRules.append(new_rule)
            else:
                self.state.rulesets[path] = Ruleset.fromRules(folder, [new_rule])
            
            # Update the rule viewer
            self.main_window.createRulesetWidget(self.state.rulesets[path])
        
        self.accept() # close dialog

        # Reselect folder
        self.main_window.folder_clicked(self.main_window.state.selected_folder)

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
        self.ui.pushbttn_matchAll.hide()
        self.ui.pushbttn_matchOne.hide()

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
        self.ui.actionCreate_New_Folder.triggered.connect(self.openNewFolder)
        self.ui.actionDelete_Folder.triggered.connect(self.deleteFolder)
        
        # Connect both single-click and double-click signals
        self.ui.listFiles.clicked.connect(self.on_list_view_single_click)
        self.ui.listFiles.doubleClicked.connect(self.on_list_view_double_click)

        # Menu actions
        self.ui.actionExit.triggered.connect(self.close)
        self.ui.actionExit.setShortcut('Ctrl+Q')
        self.ui.actionExit.setStatusTip('Exit application')
        self.ui.actionOpen_Folder.setShortcut('Ctrl+O')
        self.ui.actionOpen_Folder.setStatusTip('Open Folder')
        self.ui.actionCreate_New_Folder.setShortcut('Ctrl+N')
        self.ui.actionCreate_New_Folder.setStatusTip('New Folder')
        self.ui.actionDelete_Folder.setShortcut('Ctrl+X')
        self.ui.actionDelete_Folder.setStatusTip('Remove Folder')
        self.ui.actionUndo.triggered.connect(self.undo)
        self.ui.actionUndo.setShortcut('Ctrl+Z')
        self.ui.actionUndo.setStatusTip('Undo recent changes')
        self.ui.actionRulesetImport.triggered.connect(self.import_ruleset)
        self.ui.actionExport_Ruleset.triggered.connect(self.export_ruleset)
        self.ui.actionCreate_New_Restore_Point.triggered.connect(self.create_restore_point)
        self.ui.actionRestore_Back_to_Restore_Point.triggered.connect(self.rollback_to_restore_point)

        
        # Open rulesets button is not needed right now
        # self.ui.actionOpen_Rulesets.triggered.connect(self.open_ruleset)

        # UI actions
        self.ui.pushButton_5.clicked.connect(self.sort)
        self.ui.pushButton_2.clicked.connect(self.backButtonDir) # BackButton Folder
        self.ui.pushButton_3.clicked.connect(self.forwardButtonDir) # Forward Button
        self.ui.btnPlus.clicked.connect(self.open_ruleset) # Plus button
        self.ui.btnClear.clicked.connect(self.clear_ruleset) # Clear Button
        self.ui.pushbttn_matchAll.toggled.connect(self.update_match_mode)
        self.ui.pushbttn_matchOne.toggled.connect(self.update_match_mode)
        
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

    def deleteFolder(self):
        if self.filepath == None:
            QMessageBox.warning(self,
                                "File does not exist")
        else:
            selected_path = self.filepath
            if QDir(selected_path).exists():
                os.rmdir(selected_path)

    def forwardButtonDir(self):
        if self.filepath == None:
            QMessageBox.warning(self, "Could not go into folder",
                                "Folder does not exist")
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
    
    def openNewFolder(self):
        """
        Opens the ruleset dialog window.
        """
        dialog = NewFolderWindow(self.state)
        dialog.exec()

    def open_ruleset(self):
        """
        Opens the ruleset dialog window.
        """
        dialog = RulesetWindow(self.state, self)
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
    
    def createRulesetWidget(self, value: Ruleset):
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
            # print(rule)
            # print(rule.condition)
        self.ui.listRules.expandAll()

        # Enable match mode buttons if rules exist
        has_rules = len(value.sortingRules) > 0
        self.ui.pushbttn_matchAll.show()
        self.ui.pushbttn_matchOne.show()

        if has_rules:
            if value.match_all:
                self.set_match_mode(True)
            else:
                self.set_match_mode(False)


    def get_match_mode(self):
        """
        Returns True if 'Match All' is selected, False if 'Match One' is selected.
        """
        if self.ui.pushbttn_matchAll.isChecked():
            return True
        elif self.ui.pushbttn_matchOne.isChecked():
            return False
        else:
            return None
    
    def set_match_mode(self, match_all):
        """
        Sets the match mode radio button.
        mode: True for Match All, False for Match One
        """
        if match_all:
            self.ui.pushbttn_matchAll.setChecked(True)
        else:
            self.ui.pushbttn_matchOne.setChecked(True)
    
    def update_match_mode(self):
        if not self.ruleset:
            return

        sender = self.sender()
        if sender == self.ui.pushbttn_matchAll and sender.isChecked():
            self.ruleset.match_all = True
            print("User selected: Match All")
        elif sender == self.ui.pushbttn_matchOne and sender.isChecked():
            self.ruleset.match_all = False
            print("User selected: Match One")

    def folder_clicked(self, path):
        """
        Default hook for when a folder is clicked (single or double).
        This method can (and is) overridden by backend code to perform custom actions.
        """

        if not os.path.isdir(path):
            self.ui.listRules.clear()
            self.ui.btnPlus.setEnabled(False)
            self.ui.btnClear.setEnabled(False)

            self.ui.pushbttn_matchAll.hide()
            self.ui.pushbttn_matchOne.hide()
            return
        
        self.ui.btnPlus.setEnabled(True)
        self.ui.btnClear.setEnabled(True)
        self.state.selected_folder = os.path.normpath(path)
        
        value = self.state.rulesets.get(self.state.selected_folder)
        self.ruleset = value

        if value is not None:
            # print(value, type(value))
            self.createRulesetWidget(value)

            # Show match mode radio buttons
            self.ui.pushbttn_matchAll.show()
            self.ui.pushbttn_matchOne.show()

            # Set selected based on match_all flag
            if value.match_all:
                self.ui.pushbttn_matchAll.setChecked(True)
            else:
                self.ui.pushbttn_matchOne.setChecked(True)
        else:
            self.ui.listRules.clear()

            self.ui.pushbttn_matchAll.hide()
            self.ui.pushbttn_matchOne.hide()

    def sort(self):
        """
        Hook for sorting files when clicking the Sort button (pushButton_5)
        """
        target = FolderInfo.fromPath(self.state.target_directory, True) # Create a FolderInfo object for target
        runSortingJob(self.state.rulesets, target, description="User-initiated sort")
        print(f"Ran sorting job successfully on directory {self.state.target_directory}")
    
    def undo(self):
        """
        Undo the previous sorting operation using the Rollback module
        """
        print("Undo clicked")
        undoLast()
    
    def import_ruleset(self):
        print("Import Ruleset clicked")
        # TODO: Load ruleset from a file and apply it to the state

    def export_ruleset(self):
        print("Export Ruleset clicked")
        # TODO: Serialize current ruleset and save it to a file
    
    def create_restore_point(self):
        print("Create Restore Point clicked")
        folder = FolderInfo.fromPath(self.state.target_directory, True)
        saveRestorePoint(folder)

    def rollback_to_restore_point(self):
        print("Rollback to Restore Point clicked")
        rollbackToRestorePoint()
    
    def clear_ruleset(self):
        if self.state.selected_folder in self.state.rulesets:
            del self.state.rulesets[self.state.selected_folder]
            print(f"Cleared ruleset for {self.state.selected_folder}")
        else:
            print(f"No ruleset found for {self.state.selected_folder}")
        
        # Hide match radio buttons
        self.ui.pushbttn_matchOne.hide()
        self.ui.pushbttn_matchAll.hide()
        
        self.ui.listRules.clear()


def main():
    app = QApplication(sys.argv)
    app_state = AppState()

    window = MainWindow(app_state)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
