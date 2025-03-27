from PySide6.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem, QPushButton, QVBoxLayout, QWidget

class CollapsibleList(QTreeWidget):
    def __init__(self):
        super().__init__()
        self.setHeaderHidden(True)
        self.itemClicked.connect(self.toggle_children)

    def add_item(self, parent, text, children=None):
         item = QTreeWidgetItem([text])
         if parent is None:
            self.addTopLevelItem(item)
         else:
            parent.addChild(item)
         if children:
             for child_text in children:
                self.add_item(item, child_text)
         return item

    def toggle_children(self, item, column):
        if item.childCount() > 0:
            collapsed = item.isExpanded()
            item.setExpanded(not collapsed)

if __name__ == '__main__':
    app = QApplication([])
    window = QWidget()
    layout = QVBoxLayout(window)

    collapsible_list = CollapsibleList()
    
    item1 = collapsible_list.add_item(None, "Section 1", ["Item 1.1", "Item 1.2"])
    collapsible_list.add_item(item1, "Item 1.3", ["Item 1.3.1","Item 1.3.2"])
    collapsible_list.add_item(None, "Section 2", ["Item 2.1", "Item 2.2", "Item 2.3"])
    collapsible_list.add_item(None, "Section 3")

    layout.addWidget(collapsible_list)
    window.show()
    app.exec()