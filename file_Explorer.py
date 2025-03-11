import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileSystemModel, QTreeView, QVBoxLayout, QWidget
from PyQt5.QtCore import QModelIndex
import sip

class FileExplorer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5 File Explorer")
        self.setGeometry(100, 100, 800, 600)

        self.model = QFileSystemModel()
        self.model.setRootPath('')

        self.tree_view = QTreeView()
        self.tree_view.setModel(self.model)
        self.tree_view.setRootIndex(QModelIndex())

        self.tree_view.doubleClicked.connect(self.on_double_click)

        layout = QVBoxLayout()
        layout.addWidget(self.tree_view)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def on_double_click(self, index):
        file_path = self.model.filePath(index)
        print(f"Selected: {file_path}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    sip.setdestroyonexit(False)
    explorer = FileExplorer()
    explorer.show()
    sys.exit(app.exec_())
