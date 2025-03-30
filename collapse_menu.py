import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QTreeWidget, QTreeWidgetItem, QCheckBox, QRadioButton, QDateTimeEdit
)
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tree with Input Widgets and Text")

        # Create a central widget and a vertical layout
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

        # Create QTreeWidget with two columns: one for the label and one for the widget
        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabels(["Option", "Control"])
        layout.addWidget(self.tree_widget)

        self.setup_tree_widget()

    def setup_tree_widget(self):
        # Create a top-level "Settings" item
        settings_item = QTreeWidgetItem(["Settings"])
        self.tree_widget.addTopLevelItem(settings_item)

        # --- Checkbox Item ---
        # Description in column 0 and embed a QCheckBox in column 1 with its own text.
        checkbox_item = QTreeWidgetItem(["Enable Feature", ""])
        settings_item.addChild(checkbox_item)
        checkbox = QCheckBox("Activate")
        # Optionally adjust alignment (if needed)
        checkbox.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.tree_widget.setItemWidget(checkbox_item, 1, checkbox)

        # --- Radio Button Item ---
        # Description in column 0 and embed a QRadioButton in column 1 with its text.
        radio_item = QTreeWidgetItem(["Select Option", ""])
        settings_item.addChild(radio_item)
        radio = QRadioButton("Option 1")
        self.tree_widget.setItemWidget(radio_item, 1, radio)

        # --- Date/Time Edit Item ---
        # Description in column 0 and embed a QDateTimeEdit in column 1.
        datetime_item = QTreeWidgetItem(["Pick Date/Time", ""])
        settings_item.addChild(datetime_item)
        datetime_edit = QDateTimeEdit()
        datetime_edit.setCalendarPopup(True)
        datetime_edit.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        self.tree_widget.setItemWidget(datetime_item, 1, datetime_edit)

        # Expand all items so the user can see the content
        self.tree_widget.expandAll()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(400, 300)
    window.show()
    sys.exit(app.exec())
