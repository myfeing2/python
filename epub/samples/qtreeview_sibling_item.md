在PySide6的QTreeView里获取下一个item，最直接的方式是操作QModelIndex，通过行号和父节点来定位。下面给你一个通用的实现思路和代码。

获取下一个兄弟节点（同一父级下的下一个item）
这是最常见的需求，用index.sibling(row + 1, column)就能拿到同一父节点下的下一个项。

python
def get_next_sibling(index):
    """获取当前index的下一个兄弟节点，没有则返回无效QModelIndex"""
    if not index.isValid():
        return QModelIndex()
    next_row = index.row() + 1
    return index.sibling(next_row, index.column())
获取下一个节点（按先序遍历顺序）
如果你要的是‌整个树的下一个节点‌（比如当前节点的下一个子节点，没有子节点就找兄弟，没有兄弟就回溯找父级的兄弟），可以这样写：

python
def get_next_item(index, model):
    """
    获取树中当前index的下一个节点（深度优先先序遍历顺序）
    返回QModelIndex，找不到返回无效索引
    """
    if not index.isValid():
        return QModelIndex()
    
    # 1. 如果有子节点，返回第一个子节点
    if model.hasChildren(index):
        return model.index(0, 0, index)
    
    # 2. 否则找下一个兄弟，或回溯父级的兄弟
    while index.isValid():
        parent = index.parent()
        next_row = index.row() + 1
        if next_row < model.rowCount(parent):
            return model.index(next_row, 0, parent)
        # 没有兄弟了，回溯到父级继续找
        index = parent
    
    return QModelIndex()  # 已到末尾
用迭代器（更省事）
Qt提供了QTreeWidgetItemIterator，但那是给QTreeWidget用的。对于QTreeView，自己写个生成器也很简单：

python
def iter_tree(model, parent=QModelIndex()):
    """递归遍历树的所有节点，生成每个QModelIndex"""
    for row in range(model.rowCount(parent)):
        index = model.index(row, 0, parent)
        if index.isValid():
            yield index
            yield from iter_tree(model, index)

# 使用：找到当前项后面的所有项
def get_all_next_items(current_index, model):
    items = list(iter_tree(model))
    try:
        pos = items.index(current_index)
        return items[pos+1:]  # 返回后面所有节点
    except ValueError:
        return []
补充说明
如果是QTreeWidget，直接用QTreeWidgetItemIterator更简单，先序遍历就能拿到下一个节点。
获取当前选中项用tree_view.currentIndex()，注意检查isValid()再操作。
兄弟节点的获取不依赖是否展开，但‌遍历整棵树时需要自行处理递归‌，模型/视图架构本身不提供“下一个”的快捷接口。‌