from PySide6.QtWidgets import QApplication
from PySide6.QtWebEngineWidgets import QWebEngineView

app = QApplication([])
view = QWebEngineView()
view.setHtml("""
<html>
<body>
    <p>这是一段<span class='highlight'>可选中的文本</span></p>
    <div id='content'>另一段内容</div>
</body>
</html>
""")

page = view.page()

def on_selection_changed():
    text = page.selectedText()
    if text:
        print("用户选中：", text)

page.selectionChanged.connect(on_selection_changed)

view.show()
app.exec()
