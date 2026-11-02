'''
invisibleRootItem() 返回的是 QTreeWidget 的隐藏根节点，它是所有顶层节点的父节点，本身不显示在界面上。‌

常见用途
‌遍历所有顶层节点‌：用 root.childCount() 和 root.child(i) 递归访问整棵树，比从 topLevelItem 开始更方便。
‌删除选中节点‌：当选中项没有父节点时，通过 root.removeChild(item) 直接移除顶层节点。‌
示例代码
python
'''

# 获取隐藏根节点
root = tree.invisibleRootItem()

# 遍历所有顶层节点
for i in range(root.childCount()):
    item = root.child(i)
    print(item.text(0))

# 删除选中的节点（含顶层节点）
for item in tree.selectedItems():
    (item.parent() or root).removeChild(item)

'''
与其他“隐藏”概念区分
‌setHidden(True)‌：隐藏某个节点及其所有子节点，节点仍在数据中，只是不显示。
‌setItemHidden(item, True)‌：隐藏指定项，常用于搜索过滤功能。
‌invisibleRootItem()‌：不是隐藏某个节点，而是访问那个本就不可见的根节点本身，用于操作顶层节点的父子关系。‌
如果想做“搜索后隐藏不匹配项”这类功能，用 setItemHidden 配合递归遍历更合适；如果只是想操作顶层节点的增删，直接走 invisibleRootItem() 就行。
'''
