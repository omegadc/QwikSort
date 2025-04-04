import sys
import os
from PySide6.QtWidgets import QApplication, QListView, QVBoxLayout, QWidget
from PySide6.QtCore import QStringListModel, QModelIndex


class FileListView(QWidget):
    def __init__(self, file_paths):
        super().__init__()

        self.list_view = QListView()
        self.model = QStringListModel(file_paths)
        self.list_view.setModel(self.model)

        self.last_clicked_item = None  # Store last clicked item
        self.last_clicked_path = None  # Store last clicked file path

        # Connect click signal
        self.list_view.clicked.connect(self.on_item_clicked)

        layout = QVBoxLayout()
        layout.addWidget(self.list_view)
        self.setLayout(layout)

    def on_item_clicked(self, index: QModelIndex):
        """Handles item click and stores clicked item's info"""
        item_text = self.model.data(index)  # Get clicked item's text
        self.last_clicked_item = item_text
        self.last_clicked_path = index.data()  # Alternative way to get item data

        print(f"Clicked item: {self.last_clicked_item}")

    def get_last_clicked(self):
        """Returns last clicked item's info"""
        return self.last_clicked_item, self.last_clicked_path


if __name__ == "__main__":
    app = QApplication(sys.argv)

    file_paths = [
        "/path/to/folder",
        "/path/to/file.txt"
    ]

    window = FileListView(file_paths)
    window.show()

    sys.exit(app.exec())
