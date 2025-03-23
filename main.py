import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from MainWindow import Ui_MainWindow

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()  # Create an instance of the UI class
        self.ui.setupUi(self)  # Set up the UI



app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()