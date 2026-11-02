'''
你要的“选子项时父项也跟着选”这个效果，本质是‌父子节点复选框联动‌，需要监听状态变化后手动同步，QTreeWidget 不会自动帮你做。

给你一个可用的 PySide6 实现思路：

核心逻辑
‌连接 itemChanged 信号‌：只要树里任何一项的复选框状态变化，就触发处理函数。
‌向下同步‌：如果勾选的是父项，把它下面所有子项的状态设置成一样。
‌向上同步‌：如果勾选的是子项，检查它所有兄弟项的状态，来决定父项是选中、未选中还是半选中（部分子项被勾选）。
python
'''
from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem
from PySide6.QtCore import Qt

class TreeWidget(QTreeWidget):
    def __init__(self):
        super().__init__()
        self.itemChanged.connect(self.on_item_changed)

    def on_item_changed(self, item: QTreeWidgetItem, column: int):
        if column != 0:
            return

        state = item.checkState(0)

        # 如果当前不是半选状态，则同步所有子项
        if state != Qt.PartiallyChecked:
            self._set_children_state(item, state)

        # 向上更新父项状态
        self._update_parent_state(item)

    def _set_children_state(self, item: QTreeWidgetItem, state: Qt.CheckState):
        """递归设置所有子项的选中状态"""
        for i in range(item.childCount()):
            child = item.child(i)
            child.setCheckState(0, state)
            # 如果子项还有子项，继续递归
            if child.childCount() > 0:
                self._set_children_state(child, state)

    def _update_parent_state(self, item: QTreeWidgetItem):
        """根据子项状态，更新父项的状态（选中/未选中/半选中）"""
        parent = item.parent()
        if parent is None:
            return

        checked_count = 0
        total_count = parent.childCount()

        for i in range(total_count):
            if parent.child(i).checkState(0) == Qt.Checked:
                checked_count += 1

        if checked_count == total_count:
            parent.setCheckState(0, Qt.Checked)
        elif checked_count > 0:
            parent.setCheckState(0, Qt.PartiallyChecked)
        else:
            parent.setCheckState(0, Qt.Unchecked)

        # 递归更新更上层的父项
        self._update_parent_state(parent)
'''
使用要点
每个节点创建时记得加上 Qt.ItemIsUserCheckable 标志，才会显示复选框，例如：
python
item = QTreeWidgetItem(["节点名称"])
item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
item.setCheckState(0, Qt.Unchecked)
这段代码同时处理了‌多级嵌套‌，不管树有多深，父子状态都能正确联动。
如果你只想做简单的一层父子关系，不需要半选状态，可以去掉 PartiallyChecked 的判断，逻辑更简单。
如果你只是想要“父项选中，子项全选”
把上面代码里的 _update_parent_state 简化，只做向下同步即可：

python
'''
def on_item_changed(self, item, column):
    if column != 0:
        return
    if item.checkState(0) != Qt.PartiallyChecked:
        self._set_children_state(item, item.checkState(0))
#这样就只处理“父勾选→子全勾”这一个方向，选子项时父项不会自动变化。