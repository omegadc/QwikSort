import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QTreeView, QTreeWidget, QTreeWidgetItem
)
from PySide6.QtGui import QStandardItemModel, QStandardItem

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QTreeView & QTreeWidget Demo")
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

        # --- QTreeView Section (Model/View Approach) ---
        self.tree_view = QTreeView()
        self.setup_tree_view()
        layout.addWidget(self.tree_view)

        # --- QTreeWidget Section (Widget-Based Approach) ---
        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabels(["Category"])
        self.setup_tree_widget()
        layout.addWidget(self.tree_widget)

    def setup_tree_view(self):
        """ Set up a QTreeView with QStandardItemModel to display hierarchical data. """
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["Name","Type"])
        root_item = model.invisibleRootItem()

        # Create a parent node "Settings"
        settings_item = QStandardItem("Settings")
        settings_item.setEditable(False)
        root_item.appendRow(settings_item)

        # Add a "Network" branch with children
        network_item = QStandardItem("Network")
        network_item.setEditable(False)
        settings_item.appendRow(network_item)
        network_item.appendRow(QStandardItem("Wi-Fi"))
        network_item.appendRow(QStandardItem("Ethernet"))

        # Add a "Display" branch with children
        display_item = QStandardItem("Display")
        display_item.setEditable(False)
        settings_item.appendRow(display_item)
        display_item.appendRow(QStandardItem("Brightness"))
        display_item.appendRow(QStandardItem("Resolution"))

        self.tree_view.setModel(model)
        self.tree_view.expandAll()  # Expand all nodes

    def setup_tree_widget(self):
        """ Set up a QTreeWidget using QTreeWidgetItem to create a static, collapsible menu. """
        # Top-level item "Settings"
        settings_item = QTreeWidgetItem(["Settings"])
        self.tree_widget.addTopLevelItem(settings_item)

        # "Network" branch with children
        network_item = QTreeWidgetItem(["Network"])
        settings_item.addChild(network_item)
        network_item.addChild(QTreeWidgetItem(["Wi-Fi"]))
        network_item.addChild(QTreeWidgetItem(["Ethernet"]))

        # "Display" branch with children
        display_item = QTreeWidgetItem(["Display"])
        settings_item.addChild(display_item)
        display_item.addChild(QTreeWidgetItem(["Brightness"]))
        display_item.addChild(QTreeWidgetItem(["Resolution"]))

        self.tree_widget.expandAll()  # Expand all nodes

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(500, 500)
    window.show()
    sys.exit(app.exec())
