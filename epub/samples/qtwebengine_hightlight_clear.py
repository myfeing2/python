'''
方案一：清除文本选中高亮
这是浏览器默认的蓝色选中效果，用 window.getSelection() 清除：
'''
def clear_selection(self):
    self.webview.page().runJavaScript(
        "window.getSelection().removeAllRanges();"
    )

'''
方案二：清除自定义搜索/标记高亮
如果高亮是通过 JS 包裹 `` 标签（比如搜索结果标记）实现的，需要遍历 DOM 还原：
'''
def clear_custom_highlight(self):
    js = """
    (function() {
        const marks = document.querySelectorAll('mark,.highlight');
        marks.forEach(m => {
            const parent = m.parentNode;
            parent.replaceChild(document.createTextNode(m.textContent), m);
            parent.normalize();
        });
    })();
    """
    self.webview.page().runJavaScript(js)
'''
如果用的是其他类名或标签，把 'mark,.highlight' 换成实际使用的选择器即可。
'''
