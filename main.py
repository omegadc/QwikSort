from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
import sys

def on_button_click():
    label.setText("Button Clicked!")

# Create application
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Simple PyQt GUI")
window.setGeometry(100, 100, 300, 200)

# Create a layout
layout = QVBoxLayout()

# Create a label
global label
label = QLabel("Hello, PyQt!", window)
layout.addWidget(label)

# Create a button
button = QPushButton("Click Me", window)
button.clicked.connect(on_button_click)
layout.addWidget(button)

# Set layout and show window
window.setLayout(layout)
window.show()

sys.exit(app.exec_())
