from PySide6.QtWidgets import QApplication, QWidget, QLabel, QMessageBox
import sys


class Window(QWidget):
    def __init__(self):
        super().__init__()

        # Resize window
        self.resize(200, 150)

        # Set window title
        self.setWindowTitle('Message box')

        # Add label to window
        label = QLabel('Close this window to\nshow message box', self)
        label.move(5, 5)

    def closeEvent(self, event):
        # Show question dialogbox when closing window
        # https://doc.qt.io/qtforpython/PySide6/QtWidgets/QMessageBox.html
        answer = QMessageBox.question(self,
                                      'Message',
                                      "Are you sure to delete?",
                                      QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                      QMessageBox.StandardButton.No)

        if answer == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()


def main():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()