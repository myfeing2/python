'''
在 PySide6 里，用 QTreeView 配合 QStandardItemModel 存自定义数据，核心就是给每个 QStandardItem 挂上额外的数据，通过 ‌角色（Role）‌ 来读写。‌

🧩 核心用法
python
'''
from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtCore import Qt

# 创建模型和视图
model = QStandardItemModel()
view = QTreeView()
view.setModel(model)

# 创建节点时，直接存自定义数据
item = QStandardItem("显示的文本")
item.setData("内部ID_123", Qt.UserRole)      # 存字符串
item.setData(42, Qt.UserRole + 1)            # 存数字，换个角色
item.setData({"key": "value"}, Qt.UserRole + 2)  # 甚至可以存字典

model.appendRow(item)

'''
setText() 等价于 setData(text, Qt.DisplayRole)，就是显示的文字。
setData(value, role) 可以存任意类型（字符串、数字、对象等），角色从 Qt.UserRole 开始往上加，互不冲突。‌
📌 实际场景：商品分类树
下面这个例子展示了完整用法，节点文本显示分类名，同时用 Qt.UserRole + 1 存分类 ID，方便后续增删改查。‌

python
'''
from PySide6.QtWidgets import QApplication, QTreeView
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt
import sys

app = QApplication(sys.argv)

model = QStandardItemModel()
model.setHorizontalHeaderLabels(["分类名称"])
tree = QTreeView()
tree.setModel(model)

# 添加一级分类，同时存 ID
electronics = QStandardItem("电子产品")
electronics.setData("cat_1", Qt.UserRole + 1)  # 存自定义ID
model.appendRow(electronics)

# 添加子分类
phone = QStandardItem("手机")
phone.setData("cat_1_1", Qt.UserRole + 1)
electronics.appendRow(phone)

# 取数据：通过索引拿到 item，再按角色取
index = tree.currentIndex()
item = model.itemFromIndex(index)
if item:
    print(item.text())              # 显示文本
    print(item.data(Qt.UserRole + 1))  # 自定义ID

tree.expandAll()
tree.show()
sys.exit(app.exec())

'''
⚠️ 注意几点
‌角色从 Qt.UserRole 开始‌：Qt.UserRole 本身的值是 0x0100，实际使用时一般从 Qt.UserRole 或 Qt.UserRole + 1 开始，避免和内置角色冲突。
‌setData 和 setText 不冲突‌：它们写的是不同角色，可以同时用。
‌大数据量慎用‌：QStandardItemModel 每个单元格都是一个对象，10 万条数据可能占几百 MB 内存。数据量很大或频繁更新时，建议继承 QAbstractItemModel 自定义模型。‌
🆚 什么时候选哪种
表格
场景	QStandardItemModel	自定义 QAbstractItemModel
数据量小、固定展示	✅ 推荐，代码简单	没必要
需要频繁更新数据	❌ 不推荐，更新慢	✅ 推荐
数据量大（万级以上）	❌ 内存爆炸	✅ 推荐
'''
