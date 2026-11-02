'''
PySide6 的 ‌QTreeView‌ 是用于展示树形层级数据的控件，基于 Model/View 架构，本身不存数据，需要配合模型（如 QStandardItemModel、QFileSystemModel 或自定义模型）来使用。‌

🌳 基本用法
‌创建模型和视图‌：先创建模型并设置数据，再通过 setModel() 绑定到 QTreeView。
‌添加节点‌：用 invisibleRootItem() 获取根节点，通过 appendRow() 添加顶层项和子项。
‌展示文件系统‌：使用 QFileSystemModel 配合 setRootPath() 和 setRootIndex() 快速浏览目录。‌
'''

import sys
from PySide6.QtWidgets import QApplication, QTreeView, QVBoxLayout, QWidget
from PySide6.QtGui import QStandardItemModel, QStandardItem

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QTreeView 示例")

        # 1. 创建模型
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['名称'])

        # 2. 构建树形数据
        root_item = self.model.invisibleRootItem()  # 拿到不可见的根节点

        item1 = QStandardItem('项目 1')
        item1.appendRow(QStandardItem('子项目 1-1'))
        item1.appendRow(QStandardItem('子项目 1-2'))
        root_item.appendRow(item1)

        item2 = QStandardItem('项目 2')
        item2.appendRow(QStandardItem('子项目 2-1'))
        root_item.appendRow(item2)

        # 3. 创建视图并绑定模型
        self.tree_view = QTreeView()
        self.tree_view.setModel(self.model)

        # 4. 放入布局
        layout = QVBoxLayout()
        layout.addWidget(self.tree_view)
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

