from PySide6.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem

app = QApplication([])

tree = QTreeWidget()
tree.setHeaderLabels(["名称"])

# 添加顶层节点
root1 = QTreeWidgetItem(["项目一"])
root2 = QTreeWidgetItem(["项目二"])
tree.addTopLevelItem(root1)
tree.addTopLevelItem(root2)

# 添加子节点
child = QTreeWidgetItem(["子项目1.1"])
root1.addChild(child)

# 连接信号
def on_item_clicked(item, column):
    print(f"点击了: {item.text(0)}")

tree.itemClicked.connect(on_item_clicked)

tree.show()
app.exec()

