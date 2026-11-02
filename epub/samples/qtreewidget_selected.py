'''
PySide6 里给 QTreeWidget 设置选中状态，核心是用 QTreeWidgetItem 的 setSelected(True) 方法，这个方法会让该项以高亮形式选中（比如背景变蓝）。‌‌

python
'''
# 让某个 item 处于选中状态
item.setSelected(True)

# 判断某个 item 是否被选中
if item.isSelected():
    print("已选中")

'''
不过要注意，setSelected 控制的是“高亮选中”，不是“复选框勾选”。你如果用的是带复选框的树，要设置勾选状态得用 setCheckState：‌‌

python
'''
from PySide6.QtCore import Qt

# 勾选：未选中 / 选中 / 部分选中
item.setCheckState(0, Qt.Checked)           # 选中
item.setCheckState(0, Qt.Unchecked)         # 未选中
item.setCheckState(0, Qt.PartiallyChecked)  # 部分选中
'''
想让父项勾选时子项全部跟着勾选/取消，需要自己写联动逻辑。基本思路是监听 itemChanged 信号，然后递归设置子项的勾选状态：‌‌

python
'''
def on_item_changed(item, column):
    if item.checkState(column) == Qt.Checked:
        # 递归勾选所有子项
        def check_children(parent):
            for i in range(parent.childCount()):
                child = parent.child(i)
                child.setCheckState(column, Qt.Checked)
                check_children(child)
        check_children(item)
    elif item.checkState(column) == Qt.Unchecked:
        # 递归取消所有子项
        def uncheck_children(parent):
            for i in range(parent.childCount()):
                child = parent.child(i)
                child.setCheckState(column, Qt.Unchecked)
                uncheck_children(child)
        uncheck_children(item)

tree.itemChanged.connect(on_item_changed)
'''
📋 两种“选中”别搞混
‌高亮选中（setSelected）‌：整行背景变色，通常用于单选或多选操作，配合 setSelectionMode 控制选择模式。
‌复选框勾选（setCheckState）‌：显示一个小方框，适合做多层级的选择，比如权限分配。‌‌
如果你的需求是“选中父项，子项也全部选中”，指的是复选框勾选联动，不是高亮选中。 如果要让整棵树支持三态（未选中/选中/部分选中），记得给 item 设置 Qt.ItemIsUserCheckable | Qt.ItemIsAutoTristate 标志：‌‌

python
item.setFlags(item.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsAutoTristate)
性能提示：如果树里数据量很大（几万项），递归设置勾选状态会比较慢，实测可能需要几秒钟，建议在数据量大的场景下优化算法或批量处理。‌‌
'''