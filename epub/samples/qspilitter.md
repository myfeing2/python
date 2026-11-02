QSplitter 是 PySide6 里用来做‌可拖拽分割面板‌的容器控件，简单说就是让用户能拖动分隔条，自己调整几个区域的大小比例。‌‌

📦 基本用法
‌创建分割器‌：指定方向，Qt.Horizontal 是左右排列，Qt.Vertical 是上下排列。
‌添加子控件‌：用 addWidget() 把面板加进去，添加顺序就是显示顺序。
‌设置初始大小‌：用 setSizes([宽/高度列表]) 分配比例。‌‌
python
from PySide6.QtWidgets import QApplication, QSplitter, QTextEdit, QListWidget
from PySide6.QtCore import Qt

app = QApplication([])

splitter = QSplitter(Qt.Horizontal)  # 水平分割
left = QTextEdit("左侧面板")
right = QListWidget()
right.addItems(["项目1", "项目2", "项目3"])

splitter.addWidget(left)
splitter.addWidget(right)
splitter.setSizes([200, 400])  # 初始宽度比例

splitter.show()
app.exec()
⚙️ 常用配置
‌设置方向‌：setOrientation(Qt.Vertical) 改成垂直分割。
‌禁止折叠‌：setChildrenCollapsible(False) 防止用户把某个区域拖没。
‌调整分隔条宽度‌：setHandleWidth(5) 改粗细，太细了不好抓。
‌实时更新‌：setOpaqueResize(True) 拖动时实时缩放，False 则松手才更新。‌‌
🧩 嵌套组合
QSplitter 可以嵌套，用来做复杂布局，比如经典的“左侧列表 + 右侧上下两块”：

python
main_splitter = QSplitter(Qt.Horizontal)
left_list = QListWidget()
right_splitter = QSplitter(Qt.Vertical)  # 右侧再垂直分割
top_edit = QTextEdit("上方")
bottom_edit = QTextEdit("下方")

right_splitter.addWidget(top_edit)
right_splitter.addWidget(bottom_edit)

main_splitter.addWidget(left_list)
main_splitter.addWidget(right_splitter)
💾 状态保存与恢复
用 saveState() 保存所有分割条的位置，下次启动用 restoreState() 恢复，用户体验会好很多。‌‌

python
state = splitter.saveState()   # 保存
splitter.restoreState(state)   # 恢复
⚠️ 每个子控件最好设置合理的最小尺寸（setMinimumSize），防止用户把某个面板拖到看不见，影响使用。‌‌

更多细节可以看 PySide6 的官方文档，或者在 CSDN 搜“PySide6 QSplitter”有大量实战案例可以参考。‌‌
