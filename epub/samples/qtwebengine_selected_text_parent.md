在 QtWebEngine 里拿选中文本的父元素，需要先用 runJavaScript 在页面里执行 DOM 操作，PySide6 没有直接给这个 API。可以这样做：

python
def get_selected_parent(self):
    js = """
    (function() {
        var sel = window.getSelection();
        if (!sel.rangeCount) return null;
        var node = sel.getRangeAt(0).commonAncestorContainer;
        // 如果落在文本节点上，取它的父元素
        if (node.nodeType === 3) node = node.parentElement;
        return node ? node.outerHTML : null;
    })();
    """
    self.web_view.page().runJavaScript(js, self.handle_result)
核心逻辑：

‌获取选中范围‌：window.getSelection() 拿到当前选区，getRangeAt(0) 取第一个范围。
‌找共同祖先‌：commonAncestorContainer 是包含所有选中文本的最近节点，可能是文本节点，也可能是元素节点。
‌转成元素节点‌：如果是文本节点（nodeType === 3），用 parentElement 拿到父元素；否则直接用。
‌回传结果‌：通过 runJavaScript 的第二个参数回调函数把 outerHTML 传回 Python。
需要注意几点：

⚠️ 如果选中的文本跨多个元素，commonAncestorContainer 返回的是它们的共同父节点，不一定是某个具体标签的父元素。
⚠️ 想要更精确地定位，可以先 sel.getRangeAt(0).startContainer.parentElement，拿到选中起点的父元素。
⚠️ 该操作只能在页面加载完成后执行，否则选区为空。
如果只是想在 Qt 层面拿选中文本（不关心 DOM 父元素），直接用 QWebEnginePage.selectedText() 就行，这个 API 返回选中的纯文本内容。‌