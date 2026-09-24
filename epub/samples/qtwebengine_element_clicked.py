from PySide6.QtCore import QEvent, QObject, pyqtSignal
from PySide6.QtWebEngineWidgets import QWebEngineView

class ClickableWebView(QWebEngineView):
    element_clicked = pyqtSignal(str)  # 自定义信号，把元素内容发给外部

    def __init__(self, parent=None):
        super().__init__(parent)
        # 加载页面后，QWebEngineView 内部会有子窗口接管鼠标事件，
        # 所以不能直接重写 mousePressEvent，要通过事件过滤器来捕获
        self._glwidget = None
        self.setMouseTracking(True)

    def event(self, event):
        # 截获子控件创建事件，给子控件安装事件过滤器
        if event.type() == QEvent.ChildAdded:
            child = event.child()
            if child and child.isWidgetType():
                child.installEventFilter(self)
                self._glwidget = child
        return super().event(event)

    def eventFilter(self, source, event):
        # 鼠标按下时，获取坐标并执行 JS 获取元素
        if event.type() == QEvent.MouseButtonPress:
            pos = event.pos()
            self._query_element(pos.x(), pos.y())
        return super().eventFilter(source, event)

    def _query_element(self, x, y):
        # 通过 elementFromPoint 获取点击位置的元素内容
        js = """
        (function() {
            var el = document.elementFromPoint(%d, %d);
            if (el) return el.textContent || el.tagName || '';
            return '';
        })();
        """ % (x, y)
        self.page().runJavaScript(js, self._on_js_result)

    def _on_js_result(self, result):
        if result:
            self.element_clicked.emit(str(result).strip())

'''
⚠️ 关键点
‌不能只重写 mousePressEvent‌，因为网页加载后内部 QOpenGLWidget 会吃掉鼠标事件，必须用事件过滤器。
elementFromPoint 返回的是‌最上层的元素‌，如果你想拿更具体的（比如链接的 而不是内部的），JS 里可以用 el.closest('a') 往上找。
runJavaScript 的回调是异步的，元素内容通过信号传出来，‌别想着同步返回值‌。‌‌
🧩 补充建议
如果只是想拿‌链接地址‌（比如 href），JS 改成 el.closest('a')?.href || '' 就行。
如果想拿‌图片地址‌，用 el.closest('img')?.src || ''。
元素内容可能包含换行或多余空格，建议 .trim() 处理下，上面代码已经做了。
另外，如果你需要‌右键点击‌的元素，把 MouseButtonPress 改成 MouseButtonRelease 并且判断 event.button() == Qt.RightButton 即可，不过更推荐用 contextMenuEvent 结合 JS 的方式处理。
'''
