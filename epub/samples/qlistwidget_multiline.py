from PySide6.QtWidgets import (
    QApplication, QListWidget, QListWidgetItem,
    QWidget, QVBoxLayout, QLabel,
)
from PySide6.QtCore import QSize

class MultiLineItem(QWidget):
    def __init__(self, title: str, subtitle: str):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("font-weight: bold;")
        subtitle_label = QLabel(subtitle)
        subtitle_label.setWordWrap(True)   # 允许自动换行
        
        layout.addWidget(title_label)
        layout.addWidget(subtitle_label)

app = QApplication([])

list_widget = QListWidget()

items_data = [
    ("设备 1", "这是第一行设备的详细描述，可以很长，会自动换行。"),
    ("设备 2", "另一个设备的描述，同样支持多行显示。"),
]

for title, subtitle in items_data:
    item = QListWidgetItem()
    item.setSizeHint(QSize(200, 60))   # 调整行高，留出足够空间
    list_widget.addItem(item)
    
    custom_widget = MultiLineItem(title, subtitle)
    list_widget.setItemWidget(item, custom_widget)

list_widget.show()
app.exec()

'''
PySide6 的 QListWidget 本身默认只支持单行文本，每项对应一个 QListWidgetItem。要在列表项里显示多行文本，一般通过‌自定义 QWidget 再配合 setItemWidget()‌ 来实现，这是最直接、最灵活的方式。

🛠️ 实现步骤
‌创建自定义 Widget‌：新建一个 QWidget，用 QVBoxLayout 或 QHBoxLayout 放多个 QLabel（或 QTextEdit）。
‌添加列表项‌：先创建 QListWidgetItem，用 setSizeHint() 设置行高，再调用 setItemWidget() 把自定义 Widget 放进该项。

==========================

⚠️ 关键点说明
‌setSizeHint() 必须设置‌，否则自定义 Widget 可能显示不全或布局异常。
如果只是希望文本在 QLabel 中自动换行，记得调用 setWordWrap(True)。
若需要纯文本且不想自定义 Widget，也可以直接用 QListWidgetItem 的文本加 \n 换行符，但这种方式‌不支持自动换行‌，且视觉上不如自定义 Widget 灵活。
如果目标是显示‌不可编辑的多行文本列表‌，自定义 Widget 是最推荐的方案；若需要‌可编辑的多行文本‌，应改用 QTextEdit 或 QPlainTextEdit 而不是 QListWidget。
'''
