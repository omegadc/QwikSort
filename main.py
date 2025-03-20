import sys
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QFileDialog, 
    QVBoxLayout, QWidget, QListView, QTreeView, QFileSystemModel, QHBoxLayout
)
from PySide6.QtCore import QDir

class FileExplorer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("File Explorer")
        self.setGeometry(100, 100, 800, 500)

        # Main layout
        self.central_widget = QWidget()
        self.main_layout = QVBoxLayout()

        # Label to display the current directory
        self.label = QLabel(f"Current Directory: {os.getcwd()}")
        self.main_layout.addWidget(self.label)

        # Button to open a file
        self.open_button = QPushButton("Open File")
        self.open_button.clicked.connect(self.open_file_dialog)
        self.main_layout.addWidget(self.open_button)

        # Button to change the working directory
        self.change_dir_button = QPushButton("Change Directory")
        self.change_dir_button.clicked.connect(self.change_directory)
        self.main_layout.addWidget(self.change_dir_button)

        # File system model
        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.currentPath())

        # Horizontal layout for tree and list views
        self.explorer_layout = QHBoxLayout()

        # Tree view for directory navigation
        self.tree_view = QTreeView()
        self.tree_view.setModel(self.model)
        self.tree_view.setRootIndex(self.model.index(QDir.currentPath()))
        self.tree_view.clicked.connect(self.on_tree_clicked)
        self.explorer_layout.addWidget(self.tree_view)

        # List view for displaying files in the selected directory
        self.file_view = QListView()
        self.file_view.setModel(self.model)
        self.file_view.setRootIndex(self.model.index(QDir.currentPath()))
        self.explorer_layout.addWidget(self.file_view)

        # Add the explorer layout to the main layout
        self.main_layout.addLayout(self.explorer_layout)

        # Set the main layout
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

    def open_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*);;Text Files (*.txt)")
        if file_path:
            self.label.setText(f"Selected File: {file_path}")

    def change_directory(self):
        """Opens a directory selection dialog and updates the file system view."""
        dir_path = QFileDialog.getExistingDirectory(self, "Select Directory", QDir.currentPath())
        if dir_path:
            os.chdir(dir_path)  # Change the working directory
            self.label.setText(f"Current Directory: {dir_path}")
            self.model.setRootPath(dir_path)
            self.tree_view.setRootIndex(self.model.index(dir_path))
            self.file_view.setRootIndex(self.model.index(dir_path))

    def on_tree_clicked(self, index):
        """Updates the file list view when a directory is clicked in the tree view."""
        selected_path = self.model.filePath(index)
        if os.path.isdir(selected_path):
            self.label.setText(f"Current Directory: {selected_path}")
            self.file_view.setRootIndex(self.model.index(selected_path))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileExplorer()
    window.show()
    sys.exit(app.exec())