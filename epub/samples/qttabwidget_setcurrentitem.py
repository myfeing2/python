'''
PySide6 的 QTreeWidget 设置选中，核心就两个方法：‌setCurrentItem() 设置当前选中项，setItemSelected() 设置选中状态‌。代码很简单，直接看例子：
'''

python
from PySide6.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem
import sys

app = QApplication(sys.argv)
tree = QTreeWidget()
tree.setHeaderLabel("示例")

# 创建节点
root = QTreeWidgetItem(tree, ["根节点"])
child1 = QTreeWidgetItem(root, ["子节点1"])
child2 = QTreeWidgetItem(root, ["子节点2"])

# 方式1：设置当前选中项（高亮 + 视为当前项）
tree.setCurrentItem(child1)

# 方式2：仅设置选中状态（配合多选模式使用）
tree.setItemSelected(child2, True)

tree.show()
sys.exit(app.exec())

'''
🔧 关键点说明
‌setCurrentItem(item)‌：最常用，把某个节点设为“当前项”，会触发高亮，也是 currentItem() 拿到的那个。点击事件 itemClicked 关联的就是它。
‌setItemSelected(item, bool)‌：控制节点的选中状态，适合多选场景（setSelectionMode(QAbstractItemView.MultiSelection)）。
‌通过索引找节点再选中‌：如果节点是动态生成的，可以先遍历树找到目标节点再选中。‌
python
'''

# 按文本找节点并选中
def select_by_text(tree, text):
    for i in range(tree.topLevelItemCount()):
        item = tree.topLevelItem(i)
        if item.text(0) == text:
            tree.setCurrentItem(item)
            tree.scrollToItem(item)  # 滚动到可见位置
            return True
    return False

'''
⚠️ 常见坑
‌setCurrentItem 不会自动展开父节点‌：如果目标节点在折叠的父节点下，需要先手动 parent.setExpanded(True) 再选中，否则界面看不到。
‌选中父项联动子项‌：如果你想要“选中父项时子项也全部选中”的效果，需要自己写逻辑监听 itemChanged 信号，遍历子节点设置状态，QTreeWidget 默认不带这个行为。‌
python
'''

# 父项选中时联动子项
def on_item_changed(item, column):
    if item.checkState(column) == Qt.Checked:
        for i in range(item.childCount()):
            item.child(i).setCheckState(column, Qt.Checked)

tree.itemChanged.connect(on_item_changed)

'''
这个联动逻辑配合复选框（setCheckState）用，做多级菜单选择很实用，可以参考资料里的完整示例。‌
'''
