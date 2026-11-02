
'''
PySide6 里用 ‌QtWebChannel‌ 主要是为了实现 Python 和前端 JavaScript 的双向通信，核心思路是把 Python 对象注册到 QWebChannel 上，让网页里的 JS 能直接调用 Python 方法，同时 Python 也能反向调用 JS 函数。‌‌

🛠️ 核心用法
‌安装依赖‌：pip install pyside6，通常会自带 QtWebEngineWidgets 和 QtWebChannel 模块。
‌创建可调用的 Python 对象‌：继承 QObject，用 @Slot 装饰器暴露方法给 JS 调用，用 Signal 定义信号向 JS 发送消息。
‌注册到通道‌：创建 QWebChannel，用 registerObject() 把 Python 对象挂载上去，再通过 page.setWebChannel() 关联到网页。
‌前端引入 qwebchannel.js‌：HTML 里需要引入这个 JS 库（PySide6 内置，可用 qrc:///qtwebchannel/qwebchannel.js 路径），然后通过 new QWebChannel(qt.webChannelTransport, callback) 初始化，之后就能调用 Python 对象的方法了。‌‌
📝 最小可运行示例
python
'''
import sys
from PySide6.QtCore import QObject, Slot
from PySide6.QtWidgets import QApplication
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtWebEngineWidgets import QWebEngineView

class Bridge(QObject):
    @Slot(str, result=str)
    def hello(self, message):
        return f"Python 收到: {message}"

js = """
function initWebChannel() {
    let script = document.createElement("script");
    script.src = "qrc:///qtwebchannel/qwebchannel.js";
    script.onload = function() {
        console.log('✅ 脚本加载成功');
        // 这里可以安全调用脚本里的函数
        if(typeof QWebChannel === 'undefined') {
            console.error('❌ QWebChannel 未定义');
            return;
        }
        if(typeof qt === 'undefined' || !qt.webChannelTransport) {
            console.error('❌ qt 或 qt.webChannelTransport 未定义');
            return;
        }
        new QWebChannel(qt.webChannelTransport, function(channel) {
            window.bridge = channel.objects.bridge;  // 这里才拿到对象
            console.log('bridge初始化成功', window.bridge);
            // 在这里调用，或者触发其他函数
            //bridge.from_js("Hello", function(response) {... });
        });
    };
    script.onerror = function() {
        console.log('❌ 脚本加载失败');
    };
    document.body.appendChild(script);
}

"""

def on_load_finishe():
    print("网页加载完成，可以在这里调用 JS 函数")
    view.page().runJavaScript(js + "initWebChannel();")

app = QApplication(sys.argv)

view = QWebEngineView()
channel = QWebChannel()
bridge = Bridge()
channel.registerObject("bridge", bridge)
view.page().setWebChannel(channel)
view.loadFinished.connect(on_load_finishe)

html = '''
<!DOCTYPE html>
<html>
<head>
</head>
<body>
<button onclick="sayHello()">调用 Python</button>
<script>
function sayHello() {
    window.bridge.hello("你好", function(res) {
        alert(res);
    });
}
</script>
</body>
</html>
'''
view.setHtml(html)
view.resize(600, 400)
view.show()
sys.exit(app.exec())
'''
💡 关键点说明
‌JS 调用 Python‌：通过 channel.objects.xxx 拿到注册的对象，直接调用其 @Slot 方法，返回值通过回调函数获取。
‌Python 调用 JS‌：用 view.page().runJavaScript("jsFunctionName()") 执行前端函数。
‌信号连接‌：Python 端定义 Signal，JS 端可以用 .connect() 接收，实现主动推送消息。
‌调试技巧‌：设置环境变量 QTWEBENGINE_REMOTE_DEBUGGING=5566，可以在 Chrome 里打开 http://localhost:5566 调试网页。‌‌
如果只是简单加载网页展示，不一定需要 QWebChannel；它主要解决的是“网页交互逻辑要回传给 Python 处理”的场景。‌‌

Qt 官方文档里有完整的 WebChannel 说明和示例，需要的话可以去看 Qt WebChannel 官方文档
关键点‌：

qwebchannel.js 文件可以从 PySide6 安装目录或 Qt 官方仓库获取，放在 HTML 同目录或子目录下。
JS 端通过 channel.objects.bridge 拿到 Python 端注册的对象，然后像调用普通 JS 对象一样调用其方法、连接信号。‌‌
⚠️ 常见坑与建议
‌qwebchannel.js 路径‌：开发时用相对路径引入，打包时也要确保该文件被正确打包，否则前端无法通信。
‌调试方式‌：可以设置环境变量 QTWEBENGINE_REMOTE_DEBUGGING=5566，然后用 Chrome 访问 localhost:5566 查看前端控制台报错。
‌模块化收益‌：把桥接类单独放一个文件，主窗口只负责创建视图和注册通道，代码结构清晰，也方便写单元测试。‌‌
'''