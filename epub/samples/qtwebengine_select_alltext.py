from PySide6.QtWidgets import QApplication
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl

app = QApplication([])
view = QWebEngineView()
view.setHtml("""
<html>
<body>
    <p data-user-id='1'>这是一段<span class='highlight'>可选中的文本</span></p>
    <div id='content'>另一段内容</div>
</body>
</html>
""")

# 获取选中文本及其节点信息
js_code = """
(function() {
        const ele = document.querySelector('[data-user-id="1"]');
        return ele.innerText;
    }
)()
"""

def handle_result(result):
    print(result)

# 页面加载完成后才能执行
view.loadFinished.connect(lambda ok: view.page().runJavaScript(js_code, handle_result))
view.show()
app.exec()
