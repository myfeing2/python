'''
🌐 场景一：在 QWebEngineView 中打开 DevTools
这是最常见的情况，PySide6 的 QWebEngineView 基于 Chromium，可以像浏览器一样调出开发者工具。

‌核心方法‌：用 page().setDevToolsPage() 把 DevTools 页面绑定到另一个 QWebEngineView 上。

python
'''

from PySide6.QtWidgets import QMainWindow, QApplication, QSplitter, QWidget
from PySide6.QtCore import Qt, QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 DevTools 示例")

        # 主视图和 DevTools 视图
        self.view = QWebEngineView()
        self.dev_view = QWebEngineView()

        # 用分割器把两个视图并排显示
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.view)
        splitter.addWidget(self.dev_view)
        splitter.setStretchFactor(0, 3)  # 主视图宽一点
        splitter.setStretchFactor(1, 2)  # DevTools 窄一点
        self.setCentralWidget(splitter)

        # 加载网页
        self.view.load(QUrl("https://www.baidu.com"))

        # 🔥 关键一步：把 DevTools 绑定到主视图的页面上
        self.view.page().setDevToolsPage(self.dev_view.page())

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())

'''
‌代码说明‌：

‌setDevToolsPage()‌ 是打开 DevTools 的核心，它把主视图的调试页面输出到 dev_view 上。
你可以用 QSplitter 控制主页面和 DevTools 的布局，也可以把 dev_view 放到独立窗口里（比如 QDialog 或 QMainWindow）。
加载的页面需要支持调试，一般本地页面或普通网页都可以。
如果 DevTools 没显示出来，先确认主视图是否已经加载了页面，再检查 dev_view 是否被添加到了可见的布局里。
'''

