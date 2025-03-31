import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit
from PyQt6.QtWidgets import QTextEdit, QVBoxLayout, QWidget
from PyQt6.QtGui import QIcon

class MyApp(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("QwikSort")
        self.setWindowIcon(QIcon('time_chart_business_calender_management_icon_263056.ico'))
        self.resize(500, 400) #width & height
        layout = QVBoxLayout()
        self.setLayout(layout)


        #widgets
        self.inputField = QLineEdit()
        button = QPushButton('&Say Hello :D', clicked=self.sayHello)
        # button.clicked.connect(self.sayHello)
        self.output = QTextEdit()

        layout.addWidget(self.inputField)
        layout.addWidget(button)
        layout.addWidget(self.output)

    def sayHello(self):
        inputText = self.inputField.text()
        self.output.setText('Hello {0}'.format(inputText))

# app = QApplication([])
app = QApplication(sys.argv)
app.setStyleSheet('''
    QWidget {
        font-size: 25px;
    }
    QPushButton {
        font-size: 20px;              
    }
''')

window = MyApp()
window.show()

app.exec()