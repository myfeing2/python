def check_scroll_needed(view):
    """判断 QWebEngineView 页面是否需要滚动，返回 (是否需要, 内容高度, 视口高度)"""
    js = """
    (function() {
        var contentHeight = document.documentElement.scrollHeight;
        var viewportHeight = window.innerHeight;
        var needScroll = contentHeight > viewportHeight;
        return JSON.stringify({need: needScroll, content: contentHeight, viewport: viewportHeight});
    })();
    """
    def callback(result):
        import json
        data = json.loads(result)
        need = data["need"]
        content_h = data["content"]
        viewport_h = data["viewport"]
        print(f"是否需要滚动: {need}, 内容高度: {content_h}, 视口高度: {viewport_h}")
        # 在这里处理你的业务逻辑
        if need:
            # 需要滚动，比如自动滚到底部
            view.page().runJavaScript("window.scrollTo(0, document.body.scrollHeight);")
    view.page().runJavaScript(js, callback)

'''
⚠️ 注意事项
‌等页面加载完成再判断‌：loadFinished 信号触发时，‌主文档解析完成，但 CSS 和 JS 可能还没执行完‌，此时高度可能不准确，容易出现误判。 建议在 loadFinished 后再加一个短暂延时（比如 200ms），或者用 setTimeout 在 JS 内部延迟执行。
‌scrollHeight 是只读属性‌：它始终返回内容的总高度（包括不可见部分），不会因为滚动条位置改变而变化。
‌动态内容‌：如果页面里有懒加载图片或动态渲染的内容，高度可能在滚动过程中变化，需要‌在关键时机（如每次内容更新后）重新判断‌。
‌判断滚动条是否可见‌：也可以用 document.documentElement.clientHeight < document.documentElement.scrollHeight 来判断，效果一样。[10]
🔄 其他相关操作
‌滚动到底部‌：window.scrollTo(0, document.body.scrollHeight) 即可。[10]
‌隐藏滚动条‌（如果只想滚动但不想看到滚动条）：view.page().settings().setAttribute(QWebEngineSettings.ShowScrollBars, False)。[7]
‌触屏滑动‌：如果你在做触屏设备，需要自己处理手势事件，参考资料里的做法是‌监听 mousedown 找到带滚动条的元素，然后在 mouseMoveEvent 里通过 JS 调用 scrollBy() 实现滑动‌。[2]‌‌
'''
