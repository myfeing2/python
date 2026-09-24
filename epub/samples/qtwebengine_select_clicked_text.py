'''
要在 PySide6 的 QWebEngineView 里获取并响应“选中并点击”的文本，核心思路是‌通过 runJavaScript() 调用网页的 window.getSelection() 来拿到选中内容‌，然后通过 selectionchange 事件监听选中变化。‌‌

具体实现分两步：

1. 获取当前选中的文本
用 page().selectedText() 可以直接拿到选中文本，这是最简单的方式：‌‌
'''

# view 是 QWebEngineView 实例
page = view.page()
selected_text = page.selectedText()
print("选中的文本:", selected_text)

'''
2. 监听“选中”这个动作
selectedText() 只能在你主动去查的时候拿到值，要实现“用户一选中就自动响应”，得用 JavaScript 监听 selectionchange 事件：‌‌
'''

# 在页面加载完成后注入监听脚本
def on_load_finished(ok):
    if ok:
        js = """
        document.addEventListener('selectionchange', function() {
            var sel = window.getSelection();
            if (!sel.isCollapsed) {
                // 通过 QWebChannel 把选中文本传给 Python
                if (window.bridge) {
                    bridge.on_text_selected(sel.toString());
                }
            }
        });
        """
        view.page().runJavaScript(js)

view.page().loadFinished.connect(on_load_finished)

'''
3. 结合 QWebChannel 实现双向通信
上面 JS 里用到的 window.bridge 需要提前通过 QWebChannel 注册，这样选中文本才能实时传给 Python：‌‌
'''

from PySide6.QtCore import QObject, Slot
from PySide6.QtWebChannel import QWebChannel

class Bridge(QObject):
    @Slot(str)
    def on_text_selected(self, text):
        print("用户选中:", text)

bridge = Bridge()
channel = QWebChannel(view.page())
channel.registerObject("bridge", bridge)
view.page().setWebChannel(channel)

'''
补充：关于“点击”动作
如果要在用户‌点击选中文本时‌触发操作（比如弹出按钮），可以监听 mouseup 事件，再判断 getSelection() 是否为空：
如果只是要‌编程式地选中并高亮‌某段文本，用 page().findText("关键词") 就行，查找成功会自动选中。‌‌
⚠️ 注意：selectedText() 在用户没有选中任何内容时返回空字符串，记得做判空处理；另外，只有页面加载完成后再注入 JS 才有效，所以建议把监听脚本放在 loadFinished 信号里执行。‌‌
'''
