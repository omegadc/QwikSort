import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QTreeWidget, QTreeWidgetItem, QHBoxLayout, QLabel, QCheckBox, QRadioButton, QDateTimeEdit
)
from PySide6.QtCore import Qt

def create_item_widget(text, control_widget):
    """
    Create a composite widget with a label and a control widget arranged horizontally.
    """
    widget = QWidget()
    layout = QHBoxLayout(widget)
    layout.setContentsMargins(0, 0, 0, 0)
    label = QLabel(text)
    layout.addWidget(label)
    layout.addWidget(control_widget)
    # Optionally add a stretch if you want the widget aligned to the left
    layout.addStretch()
    return widget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("One-Column Tree with Embedded Widgets")

        # Create a central widget and a vertical layout
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

        # Create QTreeWidget with a single column
        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabel("Options")
        layout.addWidget(self.tree_widget)

        self.setup_tree_widget()

    def setup_tree_widget(self):
        # Create a top-level "Settings" item
        settings_item = QTreeWidgetItem(["Settings"])
        self.tree_widget.addTopLevelItem(settings_item)

        # --- Checkbox Item ---
        checkbox = QCheckBox("Activate")
        checkbox_widget = create_item_widget("Enable Feature", checkbox)
        checkbox_item = QTreeWidgetItem()  # Create an empty item
        settings_item.addChild(checkbox_item)
        self.tree_widget.setItemWidget(checkbox_item, 0, checkbox_widget)

        # --- Radio Button Item ---
        radio = QRadioButton("Option 1")
        radio_widget = create_item_widget("Select Option", radio)
        radio_item = QTreeWidgetItem()
        settings_item.addChild(radio_item)
        self.tree_widget.setItemWidget(radio_item, 0, radio_widget)

        # --- Date/Time Edit Item ---
        datetime_edit = QDateTimeEdit()
        datetime_edit.setCalendarPopup(True)
        datetime_edit.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        datetime_widget = create_item_widget("Pick Date/Time", datetime_edit)
        datetime_item = QTreeWidgetItem()
        settings_item.addChild(datetime_item)
        self.tree_widget.setItemWidget(datetime_item, 0, datetime_widget)

        # Expand all items so the user can see the content
        self.tree_widget.expandAll()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(400, 300)
    window.show()
    sys.exit(app.exec())
