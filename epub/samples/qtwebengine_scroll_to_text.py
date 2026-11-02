def scroll_to_text(self, target_text):
    # 转义目标文本，防止特殊字符破坏 JS 字符串
    escaped = target_text.replace("\\", "\\\\").replace("'", "\\'")
    js = f"""
    (function() {{
        // 在页面所有元素中查找包含目标文本的元素
        const walker = document.createTreeWalker(
            document.body, NodeFilter.SHOW_TEXT, {{
                acceptNode(node) {{
                    return node.textContent.includes('{escaped}')
                        ? NodeFilter.FILTER_ACCEPT
                        : NodeFilter.FILTER_REJECT;
                }}
            }}
        );
        const node = walker.nextNode();
        if (node) {{
            node.parentElement.scrollIntoView({{behavior: 'smooth', block: 'center'}});
        }}
    }})();
    """
    self.web_view.page().runJavaScript(js)

'''
‌确保页面加载完成再调用‌：如果 HTML 还没渲染完就执行 JS，很可能找不到目标。建议先连接 loadFinished 信号，再触发滚动。
‌滚动容器不一定是 window‌：有些页面的滚动条在某个 div 上而不是全局。上面的方案用 scrollIntoView() 会自动找到正确的滚动容器，比直接 window.scrollTo() 更稳。
‌如果滚动没生效‌：先确认目标文本确实存在于页面中（可以用 runJavaScript 打印 document.body.innerText 检查），再检查是不是有其他元素遮挡或滚动容器嵌套太深。‌‌

from PySide6.QtWebEngineWidgets import QWebEngineView

# 假设 web 是你的 QWebEngineView 实例
web.page().runJavaScript("""
    document.addEventListener('click', function(e) {
        // 判断点击的是文本元素（比如 、 等）
        const el = e.target.closest('p, span, div, h1, h2, h3, li');
        if (el) {
            el.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    });
""")

'''
