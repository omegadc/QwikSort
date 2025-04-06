import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QTreeView, QLineEdit, QMessageBox
)
from PySide6.QtCore import QDir
from PySide6.QtGui import QKeyEvent
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFileSystemModel


class NewFolderWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # 1) set up your model & view
        self.model = QFileSystemModel(self)
        self.model.setRootPath(QDir.homePath())  # or wherever you like

        self.tree = QTreeView(self)
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(QDir.homePath()))

        # 2) line edit for new-folder name
        self.line = QLineEdit(self)
        self.line.setPlaceholderText("Type new folder name and press Enter")

        # 3) layout
        lay = QVBoxLayout(self)
        lay.addWidget(self.tree)
        lay.addWidget(self.line)
        self.setLayout(lay)

        # 4) connect Enter key on the line edit
        self.line.returnPressed.connect(self.create_folder)

    def create_folder(self):
        name = self.line.text().strip()
        if not name:
            return  # ignore empty

        # figure out parent directory index:
        idx = self.tree.currentIndex()
        if not idx.isValid():
            idx = self.tree.rootIndex()

        # attempt to create it via the model:
        new_idx = self.model.mkdir(idx, name)

        if not new_idx.isValid():
            QMessageBox.warning(self, "Could not create folder",
                                f"Failed to create “{name}” in\n{self.model.filePath(idx)}")
        else:
            # optionally select & scroll to the new folder:
            self.tree.setCurrentIndex(new_idx)
            self.tree.scrollTo(new_idx, QTreeView.PositionAtCenter)
            self.line.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = NewFolderWidget()
    w.resize(600, 400)
    w.show()
    sys.exit(app.exec())
