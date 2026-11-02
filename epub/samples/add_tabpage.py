'''
给 QTabWidget 新增 tab 最直接的方式是用 addTab() 方法，它会将新页面追加到所有标签的末尾。‌‌
'''

python
from PySide6.QtWidgets import QTabWidget, QWidget, QVBoxLayout, QPushButton

# 创建 QTabWidget
self.tab_widget = QTabWidget(self)

# 方式一：添加空白页面，后续再填充内容
new_page = QWidget()
self.tab_widget.addTab(new_page, "新标签")

# 方式二：创建页面时直接设置内容（推荐）
def create_page(title: str):
    page = QWidget()
    layout = QVBoxLayout(page)
    layout.addWidget(QPushButton("按钮"))
    page.setLayout(layout)
    self.tab_widget.addTab(page, title)
    return self.tab_widget.count() - 1  # 返回新标签的索引

# 示例：添加并自动切换到新标签
index = create_page("文档 1")
self.tab_widget.setCurrentIndex(index)

'''
核心要点：

‌创建页面控件‌：每个 tab 对应一个 QWidget，创建时不要指定父类（QWidget() 括号里留空）。
‌添加页面‌：调用 addTab(page, label)，返回值为新标签的索引，可用于后续 setCurrentIndex() 切换。
‌设置内容‌：在添加到 tab 前，先把子控件放进布局管理器，再 page.setLayout()，否则新页面可能显示空白。
‌插入到指定位置‌：如果需要控制标签顺序，用 insertTab(index, page, label) 在指定位置插入；index 超出范围时自动追加到末尾。‌‌
⚠️ 如果窗口已显示后再动态添加标签，布局系统可能调整组件层次导致闪烁。可以在修改前设置 self.setUpdatesEnabled(False)，完成后再恢复为 True。‌‌

其他常用操作：

‌移除标签‌：self.tab_widget.removeTab(index)，注意该方法只从标签栏移除，不会删除对应的 QWidget 对象。
‌设置可关闭‌：self.tab_widget.setTabsClosable(True)，再连接 tabCloseRequested 信号处理关闭逻辑。
‌启用拖拽排序‌：self.tab_widget.setMovable(True)。‌‌
'''

