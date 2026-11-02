from PySide6.QtCore import QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView

view = QWebEngineView()
view.load(QUrl("https://example.com"))

# 等页面加载完成后再注入脚本
view.page().loadFinished.connect(lambda ok: highlight_text("keyword"))

def highlight_text(keyword):
    js_code = """
    (function() {
        // 遍历所有文本节点，找出包含关键词的
        const keyword = arguments;
        const walker = document.createTreeWalker(
            document.body, NodeFilter.SHOW_TEXT, null, false
        );
        const nodes = [];
        while (walker.nextNode()) {
            if (walker.currentNode.nodeValue.includes(keyword)) {
                nodes.push(walker.currentNode);
            }
        }
        // 用  替换匹配的文本
        nodes.forEach(node => {
            const span = document.createElement('mark');
            span.style.backgroundColor = 'yellow';
            span.textContent = node.nodeValue;
            node.parentNode.replaceChild(span, node);
        });
    })()
    """
    view.page().runJavaScript(js_code, keyword)
    
'''
- 想清除高亮，重新加载页面或者再注入一段移除 `` 标签的 JS 就行。
- 如果网页是动态渲染的（比如 Vue/React），要在页面内容变化后再执行一次，或者用 `QWebChannel` 监听内容变更。

### ⚠️ 注意事项
- 网页加载完之前执行 JS 会找不到 DOM，&zwnj;**一定要在 `loadFinished` 信号触发后再注入**&zwnj;，或者用 `setHtml()` 时同步注入。
- 如果页面有跨域或安全策略限制，注入脚本可能被拦截，本地 HTML 或自己控制的页面基本没问题。
- `runJavaScript()` 是异步的，结果通过回调函数拿，别指望同步返回。

简单说：&zwnj;**搜词用 `findText()`，自定义样式用 JS 注入**&zwnj;。你俩场景我都覆盖了，按需选就行。‌‌
'''
