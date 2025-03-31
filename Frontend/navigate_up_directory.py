from PySide6.QtCore import QDir

def navigate_up_directory():
    current_dir = QDir.currentPath()
    if not current_dir.isNull():
        parent_dir = current_dir.cdUp()
        if parent_dir:
            QDir.setCurrent(parent_dir)
            print(f"Current directory changed to: {QDir.currentPath()}")
        else:
            print("Unable to navigate up one directory level.")