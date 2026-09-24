PySide6 的 QWebEngine 里设置 JS 全局变量，核心思路是等页面加载完成后再用 runJavaScript() 注入，而不是直接修改页面代码。‌

‌常用方法：‌

‌页面加载后注入‌：在 loadFinished 信号触发后调用 page().runJavaScript() 执行 JS 赋值语句。

python
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl‌

view = QWebEngineView()
view.load(QUrl("https://example.com"))

def on_load_finished(ok):
    if ok:
        view.page().runJavaScript("window.myGlobalVar = 'hello from Python';")
        view.page().runJavaScript("console.log(window.myGlobalVar);")

view.loadFinished.connect(on_load_finished)
‌通过 QWebChannel 暴露全局对象‌：如果你的目的是让 JS 端访问 Python 端的数据，更推荐用 QWebChannel，注册一个 QObject 对象到 window 上，JS 端可以像访问全局变量一样调用它的属性和方法。‌

🛠️ 具体操作步骤
‌创建通信桥接对象‌：定义一个继承自 QObject 的类，用 @Slot 装饰器标记需要暴露给 JS 的方法。
‌注册到 QWebChannel‌：创建 QWebChannel 实例，用 registerObject('名称', 对象) 注册，然后 page.setWebChannel(channel) 绑定到页面。
‌JS 端连接‌：在 HTML 中引入 qwebchannel.js，初始化连接后就能通过 window.名称 访问 Python 对象。‌
python
from PySide6.QtCore import QObject, Slot
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtWebEngineWidgets import QWebEngineView

class Bridge(QObject):
    @Slot(str, result=str)
    def process(self, text):
        return f"Python 收到: {text}"

view = QWebEngineView()
channel = QWebChannel()
bridge = Bridge()
channel.registerObject("bridge", bridge)
view.page().setWebChannel(channel)
view.load(QUrl("https://example.com"))
javascript
// 前端 JS
new QWebChannel(qt.webChannelTransport, function(channel) {
    window.bridge = channel.objects.bridge;
    // 现在可以调用 Python 方法
    let result = window.bridge.process("你好");
});
注意：runJavaScript() 注入的变量在每次页面加载/刷新后都会丢失，需要在 loadFinished 后重新注入。 如果你的全局变量是动态变化的，建议用 QWebChannel 方式，Python 端可以用信号实时推送更新到 JS 端。‌

