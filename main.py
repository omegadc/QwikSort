<<<<<<< HEAD
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
=======
import tkinter as tk
from tkinter import messagebox

def on_button_click():
    user_text = entry.get()
    messagebox.showinfo("Message", f"You entered: {user_text}")

# Create the main window
root = tk.Tk()
root.title("Simple Tkinter App")
root.geometry("300x150")

# Create a label
label = tk.Label(root, text="Enter something:")
label.pack(pady=5)

# Create an entry widget
entry = tk.Entry(root)
entry.pack(pady=5)

# Create a button
button = tk.Button(root, text="Submit", command=on_button_click)
button.pack(pady=5)

# Run the application
root.mainloop()
>>>>>>> 72c7b37b24f6990ede87e6f1076dae7b04dfbee2
