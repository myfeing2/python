'''
在 QTreeWidget 里获取下一个 item，最直接的方法是用 ‌itemBelow()‌，它会返回当前项在视觉顺序上的下一个兄弟节点或跨层级的下一项（按先序遍历顺序）。如果没有下一项，返回 None。

python
'''
current = tree.currentItem()  # 当前选中的项
next_item = tree.itemBelow(current)  # 下一个项
'''
如果 next_item 不是 None，就可以继续操作它；否则说明已经是最后一个节点。

⚠️ itemBelow() 是按树形控件的显示顺序（先序遍历）取的，不是只取同一父节点下的兄弟项。如果你想严格限制在‌同一个父节点下的下一个兄弟‌，需要用 item.parent().indexOfChild(item) 拿到当前索引，再 +1 去取。‌

按需求选择方法
‌取显示顺序的下一个‌：用 tree.itemBelow(item)，跨层级有效，适合“顺序浏览全部节点”的场景。
‌取同一父级的下一个兄弟‌：先取父项，再用 parent.child(index + 1)，适合只在同级内移动的场景。
‌遍历整棵树‌：如果是要循环处理所有节点，推荐用 QTreeWidgetItemIterator，它按先序遍历顺序访问每个节点，比自己写递归省事。‌
python
'''
from PySide6.QtWidgets import QTreeWidgetItemIterator

it = QTreeWidgetItemIterator(tree)
while it.value():
    item = it.value()
    # 处理 item
    it += 1
'''
边界情况
当前项是最后一个节点时，itemBelow() 返回 None，需要判空。
当前项没有父项（顶级项）时，item.parent() 返回 None，取兄弟前先判断。‌
'''

'''
在 PySide6（以及 PyQt）的 QTreeWidget 中，‌itemBelow() 是真实存在的方法，而 itemNext() 并不是 QTreeWidget 的标准 API‌。

通常用户提到的“下一个 item”可能混淆了以下概念：

‌itemBelow()‌：获取视觉顺序上的下一项。
‌QTreeWidgetItemIterator 中的迭代逻辑‌：有时被误称为“next”。
‌其他库或自定义方法‌：某些第三方封装或自定义类可能实现了 itemNext()。
下面详细解释 itemBelow() 的行为，并澄清常见的误解。

1. itemBelow() 的作用
QTreeWidget.itemBelow(item) 返回在当前项 ‌视觉显示顺序‌ 中的下一项。

‌遍历顺序‌：按树形控件的 ‌先序遍历（Pre-order）‌ 顺序，即：
当前项
当前项的第一个子项（如果展开）
当前项的下一个兄弟项
如果当前项是父项的最后一个子项，则返回父项的下一个兄弟项，依此类推。
‌跨层级‌：它可以跨越父子层级。例如，如果当前项是某个父项的最后一个子项，且该父项有下一个兄弟项，则 itemBelow() 会返回那个兄弟项。
‌返回值‌：如果没有下一项（即当前是最后一项），返回 None。
示例结构
text
A
├── B
│   ├── B1
│   └── B2
└── C
itemBelow(A) → B
itemBelow(B) → B1
itemBelow(B1) → B2
itemBelow(B2) → C
itemBelow(C) → None
2. 为什么没有 itemNext()？
QTreeWidget 类中 ‌没有‌ 名为 itemNext() 的方法。如果你在某些代码中看到 itemNext()，可能是以下情况之一：

情况一：混淆了 QTreeWidgetItemIterator
QTreeWidgetItemIterator 是一个用于遍历树中所有项的迭代器，它支持 ++ 操作（在 Python 中通过 next(iterator) 或手动推进）。但这不是 QTreeWidget 的直接方法。

python
from PySide6.QtWidgets import QTreeWidgetItemIterator

it = QTreeWidgetItemIterator(treeWidget)
while it.value():
    current_item = it.value()
    # 处理 current_item
    it += 1  # 移动到下一个项
情况二：自定义扩展方法
有些开发者可能为 QTreeWidget 或 QTreeWidgetItem 写了扩展方法，命名为 itemNext()，但这不是 Qt 官方 API。

情况三：与其他库混淆
某些其他 UI 库或数据结构（如链表）可能有 next() 方法，但 QTreeWidget 不使用这种命名。

3. 如何正确获取“下一个”项？
方法一：使用 itemBelow()（推荐用于视觉顺序）
python
current_item = treeWidget.currentItem()
if current_item:
    next_item = treeWidget.itemBelow(current_item)
    if next_item:
        print(f"下一个项: {next_item.text(0)}")
    else:
        print("已经是最后一项")
方法二：使用 QTreeWidgetItemIterator（推荐用于完整遍历）
如果你需要按顺序访问所有项，迭代器更可靠：

python
def get_next_item_via_iterator(current_item):
    it = QTreeWidgetItemIterator(treeWidget)
    found_current = False
    while it.value():
        item = it.value()
        if found_current:
            return item  # 返回当前项的下一项
        if item == current_item:
            found_current = True
        it += 1
    return None  # 当前项是最后一项或不存在
方法三：仅限同级兄弟项的“下一个”
如果你只想获取 ‌同一父节点下的下一个兄弟项‌，不要用 itemBelow()，而是：

python
parent = current_item.parent()
if parent:
    index = parent.indexOfChild(current_item)
    if index < parent.childCount() - 1:
        next_sibling = parent.child(index + 1)
    else:
        next_sibling = None  # 没有下一个兄弟
else:
    # 顶级项
    root = treeWidget.invisibleRootItem()
    index = root.indexOfChild(current_item)
    if index < root.childCount() - 1:
        next_sibling = root.child(index + 1)
    else:
        next_sibling = None
总结对比
表格
特性	itemBelow()	QTreeWidgetItemIterator	自定义“同级下一个”
‌是否存在‌	✅ 是官方 API	✅ 是官方类	❌ 需手动实现
‌遍历范围‌	视觉顺序（跨层级）	视觉顺序（跨层级）	仅限同级兄弟
‌用法复杂度‌	简单，一行代码	中等，需迭代	较复杂，需判断父节点
‌适用场景‌	快速获取下一项	完整遍历所有项	仅在同级内移动
建议
如果你只是想获取 ‌视觉上紧接着的下一项‌，直接使用 treeWidget.itemBelow(current_item)。
如果你需要 ‌遍历整棵树‌，使用 QTreeWidgetItemIterator。
如果你需要 ‌严格限制在同一父节点下‌，请手动计算子项索引。
itemNext() 不是标准方法，请避免使用，除非你确认它是自定义扩展。
'''
