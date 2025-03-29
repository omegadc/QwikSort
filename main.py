import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QDialog, QFileSystemModel, QFileDialog, QCompleter
from PySide6.QtCore import QDir, QModelIndex, Qt
from mainwindow2 import Ui_MainWindow
from ruleset import Ui_Dialog

# Subclass QMainWindow to customize your application's main window

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()  # Create an instance of the UI class
        self.ui.setupUi(self)  # Set up the UI
        self.ui.actionRulesetImport.triggered.connect(self.okay)
        self.ui.actionOpen_Folder.triggered.connect(self.change_directory)

        # Changing file directory
        self.ui.pushbtn_Dir.clicked.connect(self.change_directory)
        self.ui.leTargetDirectory.returnPressed.connect(self.change_home)

        # Setting up list view 
        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.currentPath())
        self.ui.listFiles.setModel(self.model)
        self.ui.listFiles.setRootIndex(self.model.index(QDir.currentPath()))
        # Connect list view click to change directory
        self.ui.listFiles.doubleClicked.connect(self.on_list_view_click)
        ## Creating functionality for menuFile Options
        self.ui.actionExit.setShortcut('Ctrl+Q')
        self.ui.actionExit.setStatusTip('Exit application')
        self.ui.actionExit.triggered.connect(self.close)
        self.ui.pushButton_2.clicked.connect(self.navigate_up_directory())
        #
        ## making ruleset menu bar exec qaction
        self.ui.actionOpen_Rulesets.triggered.connect(self.ruleset_action)

    # navigate_up_directory
    def navigate_up_directory(self):
        current_dir = QDir.currentPath()
        if not QDir.isEmpty():
            parent_dir = current_dir.cdUp()
            parent_dir = current_dir.cd
    ### example for QAction for RulesetImport 
    def okay(self):
        print("clicked")
    
    # def open_file_dialog(self):
    #     file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*);;Text Files (*.txt)")
    #     if file_path:
    #         self.label.setText(f"Selected File: {file_path}")

    def change_home(self):
        """Opens a directory selection dialog and updates the file system view."""
        # QDir.absoluteFilePath()
        # QDir.homePath()
        # dir_path = QFileDialog.getExistingDirectory(self, "Select Direct") #(self, "Select Directory", QDir.currentPath())
        path = self.ui.leTargetDirectory.text()
        if QDir(path).exists():
            os.chdir(path)
            self.ui.label.setText(f"Target Directory: {path}")
            self.model.setRootPath(path)
            self.ui.listFiles.setRootIndex(self.model.index(path))
        else:
            print(f"The directory '{path}' does not exists.")

    def change_directory(self):

        """Opens a directory selection dialog and updates the file system view."""
        dir_path = QFileDialog.getExistingDirectory(self, "Select Directory", QDir.currentPath())
        if dir_path:
            os.chdir(dir_path)  # Change the working directory
            self.ui.label.setText(f"Target Directory: {dir_path}")
            self.ui.leTargetDirectory.setText(f"{dir_path}")
            self.model.setRootPath(dir_path)
            # self.tree_view.setRootIndex(self.model.index(dir_path))
            self.ui.listFiles.setRootIndex(self.model.index(dir_path))
    
    def directory_btn(self):
        print("directory changed")
    # def hover(self):
    #     print("hovered")
    def ruleset_action(self):
        dialog = QDialog()
        dialog_ruleset = Ui_Dialog()
        dialog_ruleset.setupUi(dialog)
        dialog.setWindowTitle("Ruleset")
        if dialog.exec() == QDialog.accepted:
            print("dialog accepted")

    def on_list_view_click(self, index: QModelIndex):
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