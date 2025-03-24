import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from MainWindow import Ui_MainWindow

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()  # Create an instance of the UI class
        self.ui.setupUi(self)  # Set up the UI
        self.ui.actionRulesetImport.triggered.connect(self.okay)
        self.ui.actionRulesetImport.hovered.connect(self.hover)
    ### example for QAction for RulesetImport 
    def okay(self):
        print("clicked")
    
    def hover(self):
        print("hovered")


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()

### command line arg to run
# pyside6-uic {file.ui} -o {file.py} 
#
# for pyside6 designer run
#pyside6-designer