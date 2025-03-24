import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QDialog, QFileSystemModel, QFileDialog
from PySide6.QtCore import QDir
from MainWindow import Ui_MainWindow
from ruleset import Ui_Dialog

# Subclass QMainWindow to customize your application's main window

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()  # Create an instance of the UI class
        self.ui.setupUi(self)  # Set up the UI
        self.ui.actionRulesetImport.triggered.connect(self.okay)

        # Changing file directory
        self.ui.pushbtn_Dir.clicked.connect(self.change_directory)

        # Setting up list view 
        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.currentPath())
        self.ui.listFiles.setModel(self.model)
        self.ui.listFiles.setRootIndex(self.model.index(QDir.currentPath()))
        # self.explorer_layout.addWidget(self.ui.listFiles)

        ## making ruleset menu bar exec qaction
        self.ui.actionOpen_Rulesets.triggered.connect(self.ruleset_action)
    ### example for QAction for RulesetImport 
    def okay(self):
        print("clicked")
    
    # def open_file_dialog(self):
    #     file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*);;Text Files (*.txt)")
    #     if file_path:
    #         self.label.setText(f"Selected File: {file_path}")

    def change_directory(self):
        """Opens a directory selection dialog and updates the file system view."""
        dir_path = QFileDialog.getExistingDirectory(self, "Select Directory", QDir.currentPath())
        if dir_path:
            os.chdir(dir_path)  # Change the working directory
            self.ui.leTargetDirectory.setText(f"Current Directory: {dir_path}")
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
        if dialog.exec() == QDialog.accepted:
            print("dialog accepted")



app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()

### command line arg to run
# pyside6-uic {file.ui} -o {file.py} 
#
# for pyside6 designer run
#pyside6-designer