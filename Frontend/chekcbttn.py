from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QPushButton, QRadioButton, QButtonGroup, QLabel
)
import sys

class RadioDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dynamic Radio Buttons")
        self.setGeometry(100, 100, 300, 200)

        # Main layout
        self.layout = QVBoxLayout()

        # Button to switch options
        self.switch_button = QPushButton("Change Options")
        self.switch_button.clicked.connect(self.switch_radio_buttons)

        # Submit button
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.print_selected_option)

        # Label to display selection
        self.result_label = QLabel("Selected: None")

        # Radio button group
        self.button_group = QButtonGroup(self)
        self.radio_buttons = []  # To track and remove old buttons

        self.option_set = 0  # Toggle flag
        self.load_radio_buttons(["Option A1", "Option A2", "Option A3"])

        self.layout.addWidget(self.switch_button)
        self.layout.addWidget(self.submit_button)
        self.layout.addWidget(self.result_label)
        self.setLayout(self.layout)

    def load_radio_buttons(self, options):
        # Clear existing radio buttons
        for rb in self.radio_buttons:
            self.button_group.removeButton(rb)
            self.layout.removeWidget(rb)
            rb.deleteLater()
        self.radio_buttons.clear()

        # Create new radio buttons
        for option in options:
            rb = QRadioButton(option)
            self.button_group.addButton(rb)
            self.layout.insertWidget(0, rb)  # Add above buttons
            self.radio_buttons.append(rb)

    def switch_radio_buttons(self):
        if self.option_set == 0:
            self.load_radio_buttons(["Option B1", "Option B2"])
            self.option_set = 1
        else:
            self.load_radio_buttons(["Option A1", "Option A2", "Option A3"])
            self.option_set = 0

    def print_selected_option(self):
        selected_button = self.button_group.checkedButton()
        if selected_button:
            self.result_label.setText(f"Selected: {selected_button.text()}")
            print(f"Selected: {selected_button.text()}")
        else:
            self.result_label.setText("Selected: None")
            print("Selected: None")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RadioDemo()
    window.show()
    sys.exit(app.exec())
