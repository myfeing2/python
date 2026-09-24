'''
PySide6 里用 QtWebEngine 获取选中文本对应的‌元素节点‌，核心思路是在 QWebEnginePage 里通过 runJavaScript() 执行 DOM 查询，拿到选中区域所在节点的信息。下面直接给你可用的代码路径。

✅ 核心实现思路
先通过 window.getSelection() 拿到选中的 Selection 对象，再用 getRangeAt(0) 获取第一个 Range，最后从 Range 上取 startContainer 和 endContainer，这两个就是文本对应的 DOM 节点。之后可以用 parentElement、tagName、className 等属性拿到节点详情。‌

代码示例
python
'''

from PySide6.QtWidgets import QApplication
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl

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

# 获取选中文本及其节点信息
js_code = """
(function() {
    var sel = window.getSelection();
    if (sel.rangeCount === 0) return null;
    var range = sel.getRangeAt(0);
    var startNode = range.startContainer;
    var endNode = range.endContainer;
    
    // 如果是文本节点，取它的父元素
    var startEl = startNode.nodeType === 3 ? startNode.parentElement : startNode;
    var endEl = endNode.nodeType === 3 ? endNode.parentElement : endNode;
    
    result = {
        text: sel.toString(),
        startTag: startEl ? startEl.tagName : null,
        startClass: startEl ? startEl.className : null,
        startId: startEl ? startEl.id : null,
        endTag: endEl ? endEl.tagName : null,
        endClass: endEl ? endEl.className : null,
        endId: endEl ? endEl.id : null,
        // 整个选中区域包含的节点列表
        allNodes: (function() {
            var nodes = [];
            var container = range.commonAncestorContainer;
            var el = container.nodeType === 3 ? container.parentElement : container;
            if (el) {
                el.querySelectorAll('*').forEach(function(n) {
                    if (range.intersectsNode(n)) nodes.push(n.tagName);
                });
            }
            return nodes;
        })()
    };
    JSON.stringify(result)
})()
"""

def handle_result(result):
    print(result)
    print("选中文本:", result.get("text"))
    print("起始节点标签:", result.get("startTag"), "类名:", result.get("startClass"), "ID:", result.get("startId"))
    print("结束节点标签:", result.get("endTag"), "类名:", result.get("endClass"), "ID:", result.get("endId"))
    print("选中区域涉及的标签:", result.get("allNodes"))

def on_finished(ok):
    if ok:
        print('loaded')
        view.page().runJavaScript(js_code, handle_result)

# 页面加载完成后才能执行
view.loadFinished.connect(lambda ok: view.page().runJavaScript(js_code, handle_result))
view.show()
app.exec()

'''
⚠️ 几个容易踩的坑
‌必须在页面加载完成后执行‌：用 loadFinished 信号或等 setHtml 完成后再调用 runJavaScript，否则拿不到 DOM。
‌文本节点 vs 元素节点‌：startContainer 通常是文本节点（nodeType === 3），需要判断后取 parentElement 才能拿到真正的元素节点。
‌跨节点选择‌：如果选中内容跨多个元素，startContainer 和 endContainer 会不同，用 commonAncestorContainer 可以拿到包裹所有选中内容的公共祖先节点。
‌range.intersectsNode()‌ 可以用来判断某个节点是否与选中区域相交，适合遍历找出所有被选中的元素。‌
如果你只需要选中文本本身
不用走 DOM 节点，PySide6 的 QWebEnginePage 有内置的 selectedText() 方法，直接返回纯文本内容，更轻量。‌
'''
